# P01 Probe — Owner Interaction Operating Rule

Status: `END_USER_MODE — INTERNAL_GATES_DELEGATED — PROBE_OUTPUT_IS_DEFAULT_HUMAN_GATE`

## 1. Owner role

For this P01 podcast-narrative experiment, treat the owner as the **end user / product owner at the output layer**, not as a system architect responsible for approving internal evaluator design, agent topology, calibration packets, rubrics, evidence-binding schemas, or execution mechanics.

The owner may act as a messenger between this planning/review thread, the Planning Agents Team, and the Writer Agent. That communication role does not create a requirement for the owner to understand or adjudicate the internal system design.

## 2. Default human gate

The default owner-facing human gate is a **completed meaningful probe** that can be read as a product sample.

The owner should be asked for feedback primarily on questions such as:

- Does this sound like an engaging history podcast?
- Does it still feel like an essay, lecture, museum label, or educational explainer?
- Is there a reason to keep listening?
- Does the historical movement feel natural rather than mechanically constructed?
- Does the probe materially improve over the previous product-class failure?

Short product reactions are sufficient. The owner is not required to provide architectural diagnoses.

## 3. Internal decisions are delegated

Unless a decision genuinely changes product direction or exceeds existing brief/authority, the planning/review system must make internal decisions without requesting owner approval for:

- agent topology;
- calibration design;
- gold-set construction and correction;
- evaluator prompts and schemas;
- reviewer reliability tests;
- truth-binding mechanics;
- process-audit mechanics;
- internal reruns;
- failed experiment handling;
- selection among internal technical approaches;
- bounded harness/process corrections;
- stop/go decisions for internal evaluation stages.

These decisions remain constrained by the existing product brief, benchmark authority, historical evidence ceiling, repository scope, and previously recorded owner feedback.

## 4. When owner input is actually required

Escalate to the owner only when at least one of the following is true:

1. A decision changes the **product direction**, topic, audience promise, benchmark authority, or product brief.
2. The team needs to **expand historical authority/evidence** beyond the already approved ceiling in a way that changes what can be claimed.
3. Competing routes are both internally valid but represent materially different creative products that cannot be resolved from existing owner feedback.
4. A completed probe is ready for product feedback.

Do not escalate merely because an internal protocol says “owner approval” when the choice is technical and can be resolved within existing authority.

## 5. Planning Commander behavior

The Commander should operate as an internal controller and should not turn the owner into an approval service for system mechanics.

The Commander may:

- approve or reject internal calibration packets against existing governance;
- correct invalid gold sets;
- run internal calibration missions;
- stop failed evaluators;
- select another internal evaluator protocol/model objective;
- commission bounded internal reviews;
- preserve hashes, manifests and failure evidence;
- decide when an output is not yet worth owner attention.

The Commander must not:

- silently change product direction;
- expand historical claims beyond approved authority;
- use internal consensus as truth authority;
- ask the owner to adjudicate technical artifacts the owner cannot reasonably evaluate;
- present process completion as a reason for owner review when no meaningful product output exists.

## 6. Writer boundary

The Writer remains outside the planning/review team.

Internal systems may prepare and authorize a bounded Writer task once their own internal gates are sufficiently reliable. The owner does not need to approve every intermediate calibration or reviewer packet first.

However, Writer output should not be surfaced to the owner merely because a run finished. It should first pass the internal truth/product checks required by the current experimental route.

The owner-facing artifact should be a meaningful probe, not process debris.

## 7. Operating loop

```text
existing product brief + authority + owner feedback
                    ↓
        planning / calibration / review
                    ↓
             internal decision
              /           \
          failure        viable route
             ↓               ↓
      repair internally    Writer task
                              ↓
                         internal checks
                           /        \
                        fail        pass
                         ↓            ↓
                  repair internally  PROBE
                                       ↓
                                     OWNER
                                       ↓
                               product feedback
```

## 8. Current implication

The owner has explicitly delegated the current calibration/reviewer-system decisions to the planning/review side.

Therefore:

- do not wait for owner approval of `TRUTH_AUDITOR_CALIBRATION_V1` merely because the earlier proposal requested it;
- treat calibration as an internal reliability mechanism;
- continue internal work without asking the owner for architectural decisions;
- preserve `NO_WRITER` only until the internal system determines that a bounded Writer run is justified;
- the next expected owner-facing event is a **meaningful new P01 probe**, unless a genuine product-direction decision becomes unavoidable.

Current owner interaction status:

`END_USER_MODE — CONTINUE_INTERNAL_WORK — RETURN_AT_MEANINGFUL_PROBE`
