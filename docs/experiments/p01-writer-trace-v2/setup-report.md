# Setup handoff — writer observability v2

The v1 FoC evidence loop improved comparison discipline but still treated Writer generation as a black box. v2 adds a frozen pre-prose writing plan, Writer execution report, Trace Auditor and first-class Writer provenance while preserving blind Product/Truth review.

Validation: `python -m unittest discover -s tests -p test_p01_writer_trace_v2.py -v` passes 5 focused tests covering listener-state plan validation, evidence binding, full beat coverage in Writer report and Writer provenance requirement.

No Planner or Writer has been dispatched. Start at `START.md`.