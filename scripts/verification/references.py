"""Verify Markdown links and pinned Git source references."""

import json
import re
import subprocess
from collections import Counter
from functools import lru_cache
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt

from repository import PIN, git, relative, sha256


MARKDOWN = MarkdownIt("commonmark", {"html": True}).enable("table")
SELF = "amaw595959-lang/ai-security-case-b-lab"
UPSTREAM = "open-webui/open-webui"


class NamedAnchors(HTMLParser):
    def __init__(self):
        super().__init__()
        self.names = set()

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.names.update(value for key, value in attrs if key in {"id", "name"} and value)


@lru_cache(maxsize=128)
def parse(markdown):
    return MARKDOWN.parse(markdown)


def headings(markdown):
    used = set()
    named = NamedAnchors()
    next_suffix = Counter()
    tokens = parse(markdown)
    for index, token in enumerate(tokens):
        if token.type == "html_block":
            named.feed(token.content)
        for child in token.children or []:
            if child.type == "html_inline":
                named.feed(child.content)
        if token.type != "heading_open":
            continue
        children = tokens[index + 1].children or []
        title = "".join(child.content for child in children if child.type in {"text", "code_inline", "image"})
        slug = re.sub(r"[^\w -]", "", title.lower()).replace(" ", "-")
        anchor = slug
        while anchor in used:
            next_suffix[slug] += 1
            anchor = f"{slug}-{next_suffix[slug]}"
        used.add(anchor)
    return used | named.names


def links(markdown):
    for token in parse(markdown):
        for child in token.children or []:
            attribute = {"link_open": "href", "image": "src"}.get(child.type)
            if attribute and child.attrGet(attribute):
                yield (token.map[0] + 1 if token.map else 1, child.attrGet(attribute))


def valid_lines(fragment, count):
    match = re.fullmatch(r"L(\d+)(?:-L(\d+))?", fragment)
    return match is not None and 1 <= int(match[1]) <= int(match[2] or match[1]) <= count


def check_anchor(path, fragment, content):
    if path.lower().endswith(".md"):
        return fragment in headings(content.decode("utf-8"))
    return valid_lines(fragment, len(content.splitlines()))


def local_link(repo, name, path, fragment):
    if path:
        base = "" if path.startswith("/") else name.rpartition("/")[0]
        target = relative(base, path.lstrip("/"))
    else:
        target = name
    item = repo.path(target, directory=not fragment)
    return not fragment or check_anchor(target, fragment, item.read_bytes())


def check_links(repo, lock):
    errors = []
    unavailable = set()
    counts = Counter()
    revisions = {}

    for name in sorted(repo.names):
        if not name.lower().endswith(".md"):
            continue
        counts["documents"] += 1
        try:
            document = repo.text(name)
        except (OSError, ValueError):
            errors.append(f"{name}: unreadable Markdown")
            continue
        for line, link in links(document):
            location = f"{name}:{line}"
            url = urlsplit(link)
            path, fragment = unquote(url.path), unquote(url.fragment)
            try:
                if not url.scheme and not url.netloc:
                    counts["local_links"] += 1
                    if not local_link(repo, name, path, fragment):
                        errors.append(f"{location}: missing local heading or invalid line anchor")
                    continue
                parts = path.strip("/").split("/", 4)
                if url.netloc != "github.com" or len(parts) < 4 or parts[2] not in {"blob", "tree", "commit", "commits"}:
                    counts["external_links_not_checked"] += 1
                    continue
                project, kind, revision = "/".join(parts[:2]), parts[2], parts[3]
                target = parts[4] if len(parts) == 5 else ""
                if project == UPSTREAM:
                    counts["pinned_source_links"] += 1
                    record = lock["files"].get(target)
                    if revision != PIN or lock["revision"] != PIN:
                        errors.append(f"{location}: Open WebUI revision differs from the pin")
                    elif kind == "blob" and (not record or (fragment and not valid_lines(fragment, record["lines"]))):
                        errors.append(f"{location}: source path or line range absent from the verified lock")
                    elif kind == "tree" and target:
                        if not any(filename.startswith(f"{target}/") for filename in lock["files"]):
                            errors.append(f"{location}: source directory absent from the verified lock")
                elif project == SELF and re.fullmatch(r"[0-9a-f]{40}", revision):
                    counts["pinned_repository_links"] += 1
                    if revision not in revisions:
                        try:
                            git(repo.root, "cat-file", "-e", f"{revision}^{{commit}}")
                        except subprocess.CalledProcessError:
                            revisions[revision] = False
                        else:
                            revisions[revision] = True
                    if not revisions[revision]:
                        unavailable.add(revision)
                    elif target:
                        content = git(repo.root, "show", f"{revision}:{relative('', target)}")
                        if fragment and not check_anchor(target, fragment, content):
                            errors.append(f"{location}: missing heading or invalid pinned line anchor")
                else:
                    counts["external_links_not_checked"] += 1
            except (OSError, ValueError, subprocess.CalledProcessError):
                errors.append(f"{location}: link target is missing or outside the repository")

    return dict(counts), errors, sorted(unavailable)


def check_upstream(upstream, lock):
    errors = []
    if git(upstream, "rev-parse", "HEAD").decode().strip() != PIN:
        return ["Open WebUI checkout HEAD does not match the pin"]
    for name, expected in lock["files"].items():
        try:
            data = git(upstream, "show", f"{PIN}:{relative('', name)}")
        except (ValueError, subprocess.CalledProcessError):
            errors.append(f"{name}: pinned blob missing")
            continue
        if expected != {"lines": len(data.splitlines()), "sha256": sha256(data)}:
            errors.append(f"{name}: pinned blob differs from source lock")
    return errors


def source_lock(repo):
    return json.loads(repo.text("scripts/verification/source-lock.json"))
