# Frozen experimental contract v1

## Objective and scope

Improve a Vietnamese history podcast about writing, not a general Sumer history.
Use actual FoC text as a craft reference, never as historical authority or a
wording/cadence template. Round 1 tests one opening/investigation segment only;
it cannot establish 60–120 minute episode quality. There is no model-written
gold answer and no permanent evaluator certification in this route.

## Six observable craft dimensions

For each dimension, quote exact spans from BOTH samples and a relevant frozen
FoC reference. Explain the reader/listener consequence and one remaining gap.
No points for pronoun counts, adjective density, artifact IDs, confidence words,
or presence of named characters by themselves.

1. `continue`: what unresolved interest makes the listener want the next beat?
2. `movement`: what changes in understanding, situation or question between beats?
3. `specificity`: which details/actions do narrative work rather than decorate?
4. `connections`: are explanatory transitions present, without reviewer-added bridges?
5. `listenability`: one-pass comprehension, information load, rhythm and repetition;
   text-only assessments must be called predictions, not observed listening.
6. `payoff`: what earned understanding closes the segment, beyond summary/teaser?

Dimension verdicts: `A`, `B`, `TIE`, `UNCERTAIN`. Neither a compulsory character,
a cliffhanger nor a question mark is required. Exposition can be excellent;
judge its effect rather than punish its genre. Do not invent historical motives
to manufacture narrative motion. FoC itself is not infallible; emulate craft
functions, not unsupported historical claims in its transcript.

## Truth gate

Audit every sentence, split into atomic factual claims as needed. Every clause
with a factual relationship, motive, function, cause, sequence or scope must be
accounted for, including descriptive details. Bind to exact approved source
quotes and record locator; entity presence alone does not license a relationship.
Distinguish documented fact, explicitly qualified inference and permitted
representative reconstruction. An absent source means unresolved/unsupported,
not permission to use prior knowledge. New claims require the same scrutiny as
old known failures. Numerical tablets are not automatically allocation ledgers;
same site/period is not same stratum; physical affordance is not proven intent.

Truth outcomes: `SUPPORTED`, `QUALIFIED`, `RECONSTRUCTION`, `UNSUPPORTED`,
`NONFACTUAL`. The last means genuinely nonfactual narration, not an escape for
uncomfortable claims. The harness checks exact quotations and sentence coverage,
NOT semantic entailment/completeness. Commander must examine missing clauses and
wrong-record bindings before retaining output. A false quote, unresolved claim,
unqualified inference or fabricated event blocks retention, irrespective of votes.

## Comparison and decision

Freeze baseline extent, hypothesis, references, prompts and acceptance rule
before Writer starts. Reviewers see no hypothesis, changelog, intended winner,
mode labels or previous verdicts. Compare same-function old/new excerpts, not a
whole old chapter against a short polished opening. Absolute FoC gap and relative
old/new improvement are separate. Primary reference is material investigation;
mechanism and spatial-scale references are supplementary, not equally weighted
generic gold. English/Vietnamese comparisons are functional, not raw word counts.

Retain only provisionally when both reviewers prefer the new candidate overall,
both prefer it on the precommitted `movement` dimension, neither reports any
dimension worse or uncertain for the candidate, all dimensions have exact
supporting spans, Truth has no unresolved claims, and actual input-only run
evidence is available. Other outcomes: `REJECT_TRUTH`, `INCONCLUSIVE_PROCESS`,
`NO_DEMONSTRATED_GAIN`. Strictness here means conservative retention, not a
claim that subjective differences can be proven with 100% accuracy.

The mechanical decision is necessary but not sufficient: content-bearing fields
can still be wrong despite valid schemas and quotations. Keep an explicit
Commander semantic audit and listening checkpoint. No `CERTIFIED`, unconditional
PASS, or “FoC-equivalent” label can be emitted by the harness.

## Independence and anti-overfitting

Reference examples are public learning examples. Do not call them holdouts or
score matching labels as evaluator accuracy. Real transcripts are not synthetic
positive examples. Future hidden tests require an independently controlled pool
and input enforcement outside the shared repo; without those, leave reliability
unproven. Freeze new test samples before exposure; once used to tune prompts,
retire them into training. Preserve disagreements and failed runs. Hashes show
content identity, not privacy, historical correctness or independent judgment.

## Roles and allowed outputs

Commander owns packets, dispatch, audit and decisions in the run directory only.
Writer returns candidate prose only. Truth returns claim-level JSON only.
Product reviewers return comparative JSON only, cannot certify history.
No specialist changes a prompt, benchmark, evidence ceiling or peer output.
No production paths, approval states or canonical router artifacts may change.
The owner authorized setup and internal bounded trials, not automatic publication.
