# Guided Owner Review Sessions

These artifacts support `GUIDED_TARGET_DIAGNOSTIC` review only.

They are deliberately separate from blind benchmark-valid owner preference packets.

Rules:

- review one micro-unit at a time;
- use source locators plus short excerpts rather than duplicating the full probe;
- show only the most relevant 3-5 feature comparisons;
- allow the owner to mark the candidate gap or the target itself (`WRONG_TARGET`);
- never aggregate guided labels into a scalar score;
- never count guided labels as blind calibration evidence;
- preserve `root_cause` as unknown until later white-box tracing.
