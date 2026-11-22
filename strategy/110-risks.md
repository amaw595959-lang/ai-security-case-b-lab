# AI Security Engineering — Full Final Prioritized Risk List (2026+)

**Inventory:** 110 proposed risk categories: 73 Case B AI-originated categories (`B-01`–`B-73`) and 37 original security categories (`R-01`–`R-37`).

**Ordering:** the nine-phase dependency-based **learning order** agreed in this conversation. It is not a universal likelihood or impact ranking. The original 37 titles are sourced from `AI_Security_37_Risks_to_160_Tools_Practice_Map.md`; the 73 Case B titles originate from the subsequent conversation and are a proposed taxonomy, not an official standard.

**Interpretation:** Some entries overlap or concern AI reliability, safety, privacy, governance, and ML behavior beyond narrow cybersecurity. A risk name does not prove the behavior exists in every AI model or that a vulnerability has been demonstrated.

## Phase 1 — AI Reliability, Truth & Independent Verification
**16 risks**

1. **B-01 — Factual Hallucination**
2. **B-02 — Evidence and Citation Fabrication**
3. **B-14 — False Execution or Capability Claims**
4. **B-63 — Circular Self-Verification and False Assurance**
5. **B-05 — Security Constraint Omission**
6. **B-04 — User-Intent Misunderstanding**
7. **B-03 — Logical and Computational Reasoning Failures**
8. **B-08 — Confidence Miscalibration**
9. **B-09 — Failure to Abstain or Escalate**
10. **B-06 — Entity and Identity Confusion**
11. **B-07 — Temporal Knowledge Failures**
12. **B-10 — Long-Context Information Loss**
13. **B-11 — Decision Instability**
14. **B-62 — AI Sycophancy and Truth Distortion**
15. **R-21 — Evaluation, benchmark, and model-judge manipulation**
16. **R-22 — Guardrail, detector, validator, and monitoring limitations**

## Phase 2 — Autonomous Agent Decisions, Identity, Authorization & Tools
**20 risks**

17. **R-01 — Workload identity, impersonation, and delegation abuse**
18. **R-02 — Tool misuse and unauthorized external actions**
19. **R-07 — Approval bypass and human-agent trust exploitation**
20. **R-10 — MCP server, tool, and transport security failures**
21. **R-05 — Indirect and multimodal prompt injection**
22. **R-12 — Direct prompt injection**
23. **R-06 — Agent goal hijacking, misalignment, and excessive autonomy**
24. **B-23 — Autonomous Goal Drift**
25. **B-24 — Reward Hacking and Proxy Optimization**
26. **B-25 — Unsafe Task Planning**
27. **B-26 — Unrequested Action Initiation**
28. **B-27 — Incorrect Tool Selection and Parameter Decisions**
29. **B-28 — Wrong-Target Operations**
30. **B-29 — Autonomous Authorization-Boundary Violations**
31. **B-30 — Human-Approval Omission**
32. **B-31 — Unsafe Irreversible Decisions**
33. **B-47 — Dangerous High-Impact Recommendations**
34. **B-34 — Unsafe Agent-to-Agent Delegation**
35. **R-20 — Inter-agent and A2A communication abuse**
36. **B-66 — Unsafe Composition of Individually Permitted Actions**

## Phase 3 — AI Data Confidentiality, Integrity & Privacy
**13 risks**

37. **B-40 — Sensitive Runtime-Context Disclosure**
38. **B-41 — Training-Data Memorization Disclosure**
39. **B-42 — Unauthorized Sensitive-Information Inference**
40. **B-43 — Sensitive-Data Redaction Failures**
41. **B-44 — Unintended External Data Transmission**
42. **B-45 — Excessive Autonomous Memory Retention**
43. **B-46 — Cross-User Context Contamination**
44. **B-67 — Unnecessary Sensitive-Data Acquisition and Aggregation**
45. **B-68 — Silent Semantic Data Corruption**
46. **R-03 — RAG and connector permission failures**
47. **R-04 — Sensitive information and hidden-context disclosure**
48. **R-13 — Retrieval, ranking, vector, and embedding manipulation**
49. **R-35 — Tenant and user isolation failures**

## Phase 4 — AI-Generated Code, Configuration & Infrastructure Security
**10 risks**

50. **R-36 — AI supply-chain and dependency compromise**
51. **B-18 — Insecure Code Generation**
52. **B-19 — Insecure Configuration and Policy Generation**
53. **B-20 — Unsafe Operational Command Generation**
54. **R-08 — Unsafe model-output handling**
55. **R-09 — Coding-agent, repository, and workspace compromise**
56. **R-14 — AI gateway, provider routing, and cache failures**
57. **R-15 — Model-serving and inference-runtime exposure**
58. **R-16 — Unsafe model loading, deserialization, and parser vulnerabilities**
59. **R-17 — File upload, document parsing, and preprocessing attacks**

## Phase 5 — Agent Memory, State, Execution & Operational Resilience
**13 risks**

60. **B-32 — Duplicate or Repeated Execution**
61. **B-33 — Unintended Action Side Effects**
62. **B-35 — Runaway Autonomous Execution**
63. **B-36 — Failure to Stop Under Abnormal Conditions**
64. **B-37 — Unauthorized Agent Self-Modification**
65. **B-38 — Unsafe Autonomous Recovery**
66. **B-39 — Multi-Agent Error Amplification**
67. **B-64 — Stale-State Execution and Time-of-Check/Time-of-Use Failures**
68. **B-71 — Benign-Memory Overgeneralization**
69. **B-72 — Self-Generated Memory Corruption**
70. **R-11 — Memory poisoning and context-management failures**
71. **R-18 — Denial of service, denial of wallet, and resource abuse**
72. **R-37 — Cascading failures and unsafe recovery**

## Phase 6 — AI Security Judgments, Defensive Evaluations & Model Robustness
**8 risks**

73. **B-15 — Security False Negatives**
74. **B-16 — Security False Positives**
75. **B-17 — Risk Severity Misjudgment**
76. **B-21 — Incorrect Security Incident Decisions**
77. **B-22 — AI Safety-Detector Judgment Failures**
78. **B-12 — Out-of-Distribution Generalization Failure**
79. **B-13 — Multimodal Perception Errors**
80. **R-23 — Jailbreaks, policy evasion, and harmful use**

## Phase 7 — High-Impact AI Decisions, Human Trust & Content Integrity
**7 risks**

81. **B-48 — Spontaneous Harmful or Abusive Content**
82. **B-49 — Biased and Discriminatory Decisions**
83. **B-50 — Misleading Decision Explanations**
84. **B-51 — Unjustified Refusal of Legitimate Tasks**
85. **B-52 — Inappropriate Human Persuasion or Manipulation**
86. **B-53 — Synthetic-Content Authenticity Misrepresentation**
87. **R-34 — Media provenance, watermarking, and deepfake risks**

## Phase 8 — Model Learning, Training, Privacy & Systemic Security
**12 risks**

88. **B-65 — Self-Generated Feedback Contamination**
89. **B-69 — Correlated AI Failures and Model Monoculture**
90. **B-70 — Unintentional Intellectual-Property and Licensing Violations**
91. **R-19 — Data-pipeline and decision-input integrity failures**
92. **R-24 — Privacy-control, synthetic-data, and unlearning assurance failures**
93. **R-25 — Machine-learning privacy attacks**
94. **R-26 — Training, fine-tuning, and feedback poisoning or integrity failures**
95. **R-27 — Backdoored models, adapters, and model components**
96. **R-28 — ML pipeline, experiment, and model-lifecycle integrity failures**
97. **R-29 — Model, intellectual-property, and artifact theft**
98. **R-30 — Adversarial evasion and robustness failures**
99. **R-33 — Federated and distributed-learning attacks**

## Phase 9 — Strategic AI Behavior, Emerging Autonomy & Specialist Infrastructure
**11 risks**

100. **B-54 — Deceptive Behavior and Concealment**
101. **B-55 — Autonomous Sabotage**
102. **B-56 — Deliberate Safeguard and Monitoring Circumvention**
103. **B-57 — Strategic Privilege Seeking and Scheming**
104. **B-58 — Evaluation Metagaming**
105. **B-59 — Deliberate Capability Concealment (Sandbagging)**
106. **B-60 — Autonomous Agent Collusion**
107. **B-61 — Agent-Originated Instruction Manipulation**
108. **B-73 — Unauthorized AI Self-Replication and Persistence**
109. **R-31 — Shared-hardware and accelerator isolation failures, including model fault injection**
110. **R-32 — Confidential-computing and attestation trust failures**

---

## Completeness and source record

- Unique entries: **110** (73 `B-*`, 37 `R-*`); **no missing or repeated identifiers**.
- The original risk inventory remains `R-01` through `R-37`; Case B is an additional 73-entry overlay, not an official extension of the original source.
- Do not claim 110 unique attack mechanisms or 100% real-world coverage; assess relevance and impact in the actual system.
- Match these risks to the companion 334-sub-sublayer checklist and 116 project inventory; treat unimplemented tests as proposed.

### Original sources

- `AI_Security_37_Risks_to_160_Tools_Practice_Map.md` — 37 original titles and project/tool practice links.
- `AI_Security_10_Layers_57_Sublayers_334_Case_B_Enhanced_Final_2026.md` — prior Case B proposed sublayer mapping.
- Current conversation — 73 Case B titles and the final nine-phase learning sequence.
