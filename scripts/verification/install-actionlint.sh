#!/usr/bin/env bash
set -euo pipefail
destination=$1
mkdir -p "$destination"
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT
archive=actionlint_1.7.7_linux_amd64.tar.gz
sha=023070a287cd8cccd71515fedc843f1985bf96c436b7effaecce67290e7e0757
curl --fail --silent --show-error --location --proto '=https' --max-time 120 \
  "https://github.com/rhysd/actionlint/releases/download/v1.7.7/$archive" --output "$work/$archive"
printf '%s  %s\n' "$sha" "$work/$archive" | sha256sum --check --strict
tar -xzf "$work/$archive" -C "$work" actionlint
install -m 0755 "$work/actionlint" "$destination/actionlint"
"$destination/actionlint" --version
