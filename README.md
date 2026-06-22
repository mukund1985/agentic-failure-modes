---
license: apache-2.0
language:
- en
tags:
- agentic-ai
- evaluation
- failure-modes
- llm-evaluation
- production-ai
- RLHF
- reward-hacking
- explainability
pretty_name: Agentic AI Failure Modes (PAEF)
size_categories:
- n<1K
task_categories:
- text-classification
- question-answering
---

# Agentic AI Failure Modes Dataset

This dataset accompanies the paper:

> **Evaluating Agentic AI in the Wild: Failure Modes, Drift Patterns, and a Production Evaluation Framework**
> Mukund Pandey, 2025. [arXiv:2605.01604](https://arxiv.org/abs/2605.01604)

It provides structured, reusable representations of the seven failure modes identified in the paper, along with empirical trace data from the experiments showing where standard metrics fail to detect them.

## Why This Dataset Exists

Standard evaluation metrics — ROUGE, BERTScore, Accuracy/AUC, AgentBench, MT-Bench — collectively fail to detect **any** of these seven failure modes reliably within a single evaluation cycle. This dataset makes the failure mode taxonomy and the empirical evidence machine-readable so other researchers can:

- Build detection benchmarks for production agentic systems
- Test evaluation frameworks against known blind spots
- Extend the taxonomy with new failure modes from their own systems

## Dataset Files

| File | Description | Rows |
|------|-------------|------|
| `data/failure_modes.jsonl` | Full taxonomy: 7 failure modes with definitions, production observations, detection notes, and PAEF dimension mapping | 7 |
| `data/metric_coverage.jsonl` | Table 1 from paper: detection coverage of 5 standard metrics + PAEF across all 7 failure modes | 7 |
| `data/distribution_collapse_traces.jsonl` | Table 2: FM-3 — 5 weekly windows showing accuracy flat while diversity collapses | 5 |
| `data/tool_degradation_traces.jsonl` | Table 3: FM-2 — 4 stages of tool partial response degradation; total accuracy drop only 0.03 while PAEF score drops to 0.11 | 4 |

## The Seven Failure Modes

| ID | Name | Alias | PAEF Dimension |
|----|------|-------|----------------|
| FM-1 | Cascading Decision Error | Coherence Illusion | Cascade Uncertainty |
| FM-2 | Silent Degradation via Availability-Truth Decoupling | Tool Cascade Failure | Tool Reliability |
| FM-3 | Distribution Collapse Under Metric Optimisation | Output Diversity Collapse | Distribution Health |
| FM-4 | Consistency Collapse Across Entry Points | Cross-Surface Inconsistency | Cross-Surface Consistency |
| FM-5 | Explanation-Decision Decoupling | Attribution Failure | Explanation Validity |
| FM-6 | Silent Correctness Erosion Under Latency Pressure | Latency-Correctness Tradeoff Failure | Tool Reliability |
| FM-7 | Proxy Goal Convergence | Reward Hacking at System Scale | Distribution Health |

## Key Finding

No standard metric detects more than 2 of the 7 failure modes — and none detects any within a single evaluation cycle. PAEF detects all 7.

The most dangerous property: **failure modes FM-1, FM-2, and FM-6 actively look like success** to standard monitoring. FM-2 (tool degradation) produced a total external accuracy drop of only 0.03 across all four degradation stages, while PAEF score dropped from 0.94 to 0.11.

## The PAEF Framework (5 Dimensions)

The Production Agentic Evaluation Framework measures:

1. **Cascade Uncertainty** — uncertainty propagation across pipeline steps; flags steps that receive low-confidence input and emit high-confidence output (FM-1)
2. **Tool Reliability** — tracks tool call state as success / partial / failed; rising partial rate + stable accuracy is the FM-2 signature (FM-2, FM-6)
3. **Distribution Health** — intra-session diversity score, output entropy, and repeat rate over a sliding window (FM-3, FM-7)
4. **Explanation Validity** — perturbation consistency check: attributed features are nullified and prediction stability is measured; low correlation = FM-5 (FM-5)
5. **Cross-Surface Consistency** — decision agreement rate across semantically equivalent requests arriving via different surfaces (FM-4)

Reference implementation: [mukund1985/llm-eval-toolkit](https://github.com/mukund1985/llm-eval-toolkit)

## Data Schema

### failure_modes.jsonl
```json
{
  "id": "FM-1",
  "name": "string",
  "alias": "string",
  "description": "string",
  "production_observation": "string",
  "why_standard_metrics_miss": "string",
  "key_property": "string",
  "paef_dimension": "string",
  "detectable_by": ["PAEF"],
  "tags": ["string"]
}
```

### metric_coverage.jsonl
```json
{
  "failure_mode_id": "FM-1",
  "failure_mode_name": "string",
  "ROUGE": "detected | partial_with_lag | not_detected",
  "BERTScore": "detected | partial_with_lag | not_detected",
  "Accuracy_AUC": "detected | partial_with_lag | not_detected",
  "AgentBench": "detected | partial_with_lag | not_detected",
  "MT_Bench": "detected | partial_with_lag | not_detected",
  "PAEF": "detected | partial_with_lag | not_detected",
  "notes": "string"
}
```

### distribution_collapse_traces.jsonl
```json
{
  "failure_mode_id": "FM-3",
  "window": "W1",
  "window_label": "healthy | stable | narrowing | collapsed | fully_collapsed",
  "unique_output_categories": 20,
  "accuracy": 0.88,
  "output_entropy": 0.965,
  "intra_session_diversity": 0.200,
  "repeat_rate": 0.225,
  "paef_flagged": false,
  "notes": "string"
}
```

### tool_degradation_traces.jsonl
```json
{
  "failure_mode_id": "FM-2",
  "stage": 1,
  "stage_label": "baseline | early_degradation | moderate_degradation | severe_degradation",
  "external_accuracy": 0.87,
  "tool_partial_response_rate": 0.04,
  "paef_score": 0.94,
  "silent_degradation_detected": false,
  "notes": "string"
}
```

## Usage

```python
from datasets import load_dataset

# Load failure mode taxonomy
failure_modes = load_dataset("mukund1985/agentic-failure-modes", data_files="data/failure_modes.jsonl", split="train")

# Load metric coverage table
coverage = load_dataset("mukund1985/agentic-failure-modes", data_files="data/metric_coverage.jsonl", split="train")

# Load empirical traces
dist_traces = load_dataset("mukund1985/agentic-failure-modes", data_files="data/distribution_collapse_traces.jsonl", split="train")
tool_traces = load_dataset("mukund1985/agentic-failure-modes", data_files="data/tool_degradation_traces.jsonl", split="train")
```

## Citation

```bibtex
@article{pandey2025evaluating,
  title={Evaluating Agentic AI in the Wild: Failure Modes, Drift Patterns, and a Production Evaluation Framework},
  author={Pandey, Mukund},
  journal={arXiv preprint arXiv:2605.01604},
  year={2025}
}
```

## License

Apache 2.0
