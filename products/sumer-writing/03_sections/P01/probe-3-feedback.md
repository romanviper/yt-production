# Probe 3 feedback — P01

Status: `changes_requested_for_probe_3`

Reviewed branch: `codex/foc-editorial-probe2-feedback`

Reviewed Probe 2 commit: `4a1386506ff87341b5b041e840d08d4465522d09`

## Decision

Probe 2 is a **major architectural improvement but not yet production-quality prose**.

Do not revise it line by line into a final P01 passage. Preserve it as a diagnostic artifact and run one more controlled probe.

Probe 2 demonstrates that the previous thesis-priming problem was materially reduced:

- the Writer did not receive `earned_meaning`;
- rejected causal interpretations were exposed as red lines rather than positive story material;
- the material snapshot was bound immutably to the task;
- the draft no longer tells the old memory-failure → administrative-pressure → bulla-as-solution story;
- the draft explicitly preserves coexistence and avoids a simple token→tablet replacement ladder.

The remaining failure has changed form. The prose is no longer primarily an essay proving a thesis. It is now closer to a **museum/audio-guide explanation of artifact classes**.

That distinction matters because the next intervention should not reopen the same evidence-ontology work or add more style rules to the Writer prompt.

## Probe 2 outcome assessment

### 1. Am I following something that is happening or changing?

**Partial pass.**

The passage follows a real material transition: enclosed counters / exterior impressions → numerical information visible directly on clay surfaces → ruled proto-cuneiform surfaces.

This is much better than Probe 1's abstract causal argument.

However, the thing being followed is mostly a succession of **artifact types described by the narrator**, not a concrete historical/documentary instance unfolding under pressure.

The passage therefore feels like:

```text
look at object class A
→ explain its uncertainty
→ look at object class B
→ explain its function
→ look at object class C
→ summarize the material change
```

rather than a story the listener is compelled to continue following.

### 2. Do I want to know what happens next?

**Partial / weak pass.**

The opening has genuine curiosity:

> Một khối đất sét rỗng đã bị vỡ.

The concealed-inside / visible-outside relationship of a bulla is intrinsically interesting.

But the forward pressure declines quickly once the narration moves from that apparent object instance into category-level explanation of tokens, bullae and numerical tablets.

The listener is mainly waiting for the narrator's next explanation, not for the consequence of an unfolding historical situation or evidentiary discovery.

### 3. Does meaning emerge from what I followed?

**Partial fail.**

Probe 2 is less thesis-led than Probe 1, but it still repeatedly steps outside the material and explains the interpretation directly.

The clearest transition is:

> Không có một hàng rào thời gian sạch sẽ ngăn cách những vật này...
>
> Nhưng giữa chúng có một thay đổi mà đất sét còn giữ được.

The statement is accurate and useful, but structurally it is the narrator announcing the analytical takeaway before walking through it.

The final paragraphs then restate the from→to movement almost schematically.

The audience can understand the change, but it is still being **taught the change** more than discovering it through a sustained telling.

### 4. Can I retell the progression after one hearing?

**Pass.**

The progression is clear:

```text
tokens
→ tokens enclosed in bullae with exterior impressions
→ numerical marks directly on solid clay surfaces
→ ruled Uruk IV tablets combining numbers and other signs
```

The passage also correctly remembers that these practices overlap rather than forming a clean replacement ladder.

### 5. Did inference/reconstruction masquerade as documented fact?

**Partial fail.**

The epistemic architecture is much cleaner than in Probe 1, but two prose-level problems remain.

First, the opening creates what sounds like a particular documented incident/object:

> Một khối đất sét rỗng đã bị vỡ. Nhờ vậy, thứ từng được giấu kín bên trong nó mới lộ ra...

The current P01 material handoff contains a **generic bulla class**, not a bound specific archaeological object with inventory identity/find context showing that this exact broken object is the one being narrated.

The sentence therefore creates a pseudo-instance: rhetorically specific, evidentially generic.

Second, the passage states reconstructed manufacturing workflow as ordinary factual sequence:

> Khi đất còn ướt, những token được đặt vào trong rồi lớp vỏ được khép lại.

The material contract correctly classifies the full deposit/close/mark/seal workflow as `representative_reconstruction`, not a witnessed event. The prose should preserve that distinction naturally.

Do not solve these issues by adding disclaimers to every sentence. The deeper solution is to give Writer better instance-level evidence when available, and require reconstruction status to remain honest when it is not.

---

# Main diagnosis for Loop 3

## The new bottleneck: epistemically clean material is still mostly type-level material

The P01 material set now contains useful and well-qualified records, but they are mainly synthesized categories:

```text
Geometric clay tokens in Late Uruk administrative levels
Hollow clay bulla with enclosed tokens
Cylinder seals
Solid numerical tablets
Archaic proto-cuneiform administrative accounts
reed styluses
administrative sealing assemblages
ration-accounting process
```

These are real historical materials, but they are largely **type/class-level summaries assembled from scholarship**, not specific objects/documents/finds with their own bounded identity and context.

That explains an important feature of Probe 2.

The Writer correctly senses that a bulla could anchor a story, so it opens as though it has one concrete broken bulla in hand. But because the evidence broker actually gives it a generic material class, it cannot remain inside that specific object. It has to retreat into generalized exposition.

This is different from Probe 1's failure.

```text
Probe 1 failure:
upstream causal thesis → Writer proves thesis as essay

Probe 2 failure:
clean but class-level material → Writer performs a guided tour of artifact categories
```

This is a useful narrowing of the problem.

## Do not lower evidence standards to escape the museum-guide tone

Do not restore invented named clerks, invented transactions or unsupported warehouse scenes.

Do not tell Writer to "make it more novelistic" by manufacturing a specific event.

The correct next experiment is to ask whether the already approved sources contain **specific instance-level anchors** that Research/Evidence Resolution failed to preserve.

---

# Loop 3 intervention — single-variable experiment

For Probe 3, keep the following unchanged unless a correctness failure requires otherwise:

- `draft-section.md` Writer objective;
- creative boundaries;
- P01 mission;
- current P01 `historical_change`;
- current claim/source ceiling;
- epistemic-layer model;
- rejection/red-line model;
- 450–650 word contiguous-excerpt experiment form.

Do **not** change mission or Writer prompt yet.

The single content variable for Probe 3 is **evidence granularity**.

## Step 1 — Run bounded instance-resolution inside the already approved P01 sources

Run one evidence-resolution pass whose target is not "more story material" in the abstract.

Its target is:

> recover specific artifact/document instances already present in approved P01 sources when those sources provide enough identity/context to distinguish an individual object or bounded assemblage from a generic artifact class.

Useful instance-level fields may include, when actually available in the approved source:

- museum/catalogue/inventory/object number;
- excavation or find context;
- site + level/stratum/context;
- figure/plate/catalogue locator;
- exact object dimensions rather than class range;
- exact marks visible on that object;
- what physically survives versus what is reconstructed;
- current collection/location if relevant and supported;
- relationship between exterior marks and enclosed contents for that actual specimen;
- uncertainty specific to that instance.

Do not invent any field that the source does not support.

Do not assign opening, focal carrier, climax, scene role or narrative value.

The evidence layer only preserves the instance. Writer remains free to ignore it.

## Step 2 — Add instance records without replacing the class-level records

Class-level material is still useful for context and qualification.

A good P01 handoff can contain both:

```text
TYPE / SYNTHESIS
"Late Uruk bullae with enclosed tokens and exterior impressions"

INSTANCE
"Specific bulla/catalogue object X from context Y, preserving features Z"
```

The instance must have its own source locator and epistemic layers.

Do not convert a type-level scholarly reconstruction into a fake instance merely by using singular grammar.

## Step 3 — Human evidence checkpoint

Before creating Probe 3 Writer task, answer only:

1. Does P01 now contain at least one genuinely instance-level artifact/document anchor?
2. Is its identity/context supported rather than invented?
3. Does it preserve enough material detail that Writer could stay with that object for more than one paragraph if it chose to?
4. Are interpretation/reconstruction boundaries still visible?

If approved P01 sources contain no such instance, stop and record that result.

Then the owner chooses between:

```text
A. authorize one narrow source expansion for instance resolution
B. proceed with type-level evidence and explicitly test representative reconstruction
C. accept that this movement may be better told as analytical/documentary exposition
```

Do not silently invent an instance.

## Step 4 — Bind Probe 3 experiment instructions into task provenance

Probe 2 has a provenance defect unrelated to prose quality.

`T0059` context/work-order records the section forecast of 1050–1550 words, but does not contain the task-local instruction that this experiment is a contiguous 450–650 word passage. The task report nevertheless says the Writer followed that instruction.

That means part of the effective prompt came through an unbound channel.

Probe 3 must fix this.

Add a task-local experiment contract, either directly in the work order/packet or through a canonical task input, equivalent to:

```json
{
  "probe_id": "P01-PROBE-3",
  "form": "contiguous_section_excerpt",
  "target_words": {
    "min": 450,
    "max": 650
  },
  "completes_section": false,
  "instruction": "Write a contiguous passage from the larger P01 section. Do not compress or complete the whole P01 mission inside this excerpt."
}
```

The exact schema is flexible.

Requirements:

- it is hash-bound into the task packet;
- the Writer-facing context contains the relevant excerpt constraint;
- report/work-order/context cannot disagree about the effective task;
- comparison metadata and old Probe output do not need to be shown to Writer.

## Step 5 — Fresh snapshot and fresh Writer task

After any new instance materials are committed:

1. regenerate the immutable P01 material snapshot;
2. invalidate any task bound to the old snapshot;
3. create a fresh Writer task;
4. exclude Probe 1 and Probe 2 prose, reviews and feedback from Writer context;
5. keep the same mission, historical change and Writer operation for this experiment.

This isolates the effect of material granularity.

---

# Writer truth feedback for Probe 3

Do not give Writer a prose recipe.

The only binding correction from Probe 2 should be epistemic:

> Do not turn a type-level material record into a specific historical/artifact instance unless the evidence supplies that instance. Representative manufacturing/action sequences must remain naturally identifiable as reconstruction or inference rather than silently becoming witnessed events.

Do not instruct:

- start with the artifact;
- use a character;
- create a scene;
- use sensory details;
- avoid exposition by quota;
- add conflict every N words;
- imitate FoC or any competitor structure.

Those would contaminate the test.

---

# What should remain frozen

The Loop 2 authority corrections appear to have worked and should not be reopened in Loop 3:

1. Keep `earned_meaning` out of Writer-facing context.
2. Keep prohibited/rejected interpretations separate from usable epistemic material.
3. Keep top-level schema-v2 factual affordances from duplicating reconstructed workflows.
4. Keep unknown actors unknown/inferred.
5. Keep non-linear coexistence qualification.
6. Keep immutable material snapshot binding.
7. Keep the current observable historical change.
8. Keep the current Writer prompt unchanged.

The purpose of Probe 3 is not to find another way to describe the same architecture problem. It is to test whether the missing ingredient is **specific source material that can actually be followed**.

---

# Probe 3 evaluation

Use the same five questions so the experiments remain comparable:

1. Am I following something that is happening/changing rather than an argument being proved?
2. Do I want to know what happens next?
3. Does meaning emerge from what I followed rather than being announced by the narrator?
4. Can I retell the progression after one hearing?
5. Did any inference, reconstruction, generic class or source-distance issue masquerade as a documented specific fact?

Add one diagnostic question for this round:

6. **Can I identify the concrete thing/evidence thread I was following, or did the passage become a catalogue of artifact classes?**

This sixth question is diagnostic, not a permanent method rule.

---

# Interpretation of Probe 3 results

## If Probe 3 improves materially

If instance-level evidence allows Writer to sustain curiosity and progression without inventing a scene, then the architecture has identified a genuine research-handoff requirement:

> story-first drafting often needs not merely "concrete material", but sufficiently resolved source instances when the sources contain them.

At that point decide how narrowly to encode instance resolution into evidence readiness without requiring every historical section to have a hero artifact.

Do not introduce a narratability score.

## If Probe 3 remains museum-guide exposition

If Probe 3 receives genuinely specific, source-rich instance material and still produces the same guided-explanation shape, stop modifying evidence architecture.

The next suspect becomes Writer/task framing.

Loop 4 should then test **one** of the following, not all simultaneously:

- the causal/question-shaped section mission (`Điều gì khiến... trở nên hữu ích?`);
- the passive evidence-centric wording of the Writer-facing movement;
- the generic Writer objective/model behavior.

Prefer changing the task/mission framing before adding craft formulas.

## If approved sources contain no usable instance

Record that result as evidence, not failure.

P01 may simply be a movement where the truth ceiling supports material history at the type/assemblage level better than a document-led story.

The next controlled experiment should then be explicit representative reconstruction versus analytical telling, with owner approval—not a fake artifact instance.

---

# Exit criteria for Loop 3 setup

Do not create Probe 3 until:

- the instance-resolution pass over approved P01 sources is complete;
- any instance record is genuinely source-bound and epistemically classified;
- owner has seen whether specific instance material exists;
- effective 450–650 excerpt instructions are inside task provenance;
- material snapshot is regenerated after material changes;
- old probes/feedback are excluded from the new Writer context;
- mission, historical change and Writer prompt remain unchanged for this experiment.

Probe 2 should remain preserved as the baseline showing that thesis priming was reduced but class-level material still produced museum-guide exposition.
