#!/usr/bin/env python3

print(
    """YT Production

make new PRODUCT=<slug> TITLE="Tên làm việc"
make task PRODUCT=<slug> OPERATION=research_plan
make task PRODUCT=<slug> OPERATION=research_workstream UNIT=WS01
make task PRODUCT=<slug> OPERATION=outline RUNTIME=dsh
make run PRODUCT=<slug> TASK=<task-id>
make task PRODUCT=<slug> OPERATION=draft_section SECTION=P04
make excerpt PRODUCT=<slug> SECTION=P04 POSITION=opening MIN_WORDS=300 MAX_WORDS=400 CLAIMS="CLM-0001" LOCAL_JOB="..." STOP="..."
make task PRODUCT=<slug> OPERATION=review_section SECTION=P04
make show PRODUCT=<slug>
make brief PRODUCT=<slug> TASK=<task-id>
make check PRODUCT=<slug>
make research-units PRODUCT=<slug>
make sections PRODUCT=<slug>
make impact PRODUCT=<slug> CLAIM=CLM-0001
make impact PRODUCT=<slug> SECTION=P04
make assemble PRODUCT=<slug>
make test

Current section lifecycle:
approve outline -> materialize sections -> draft_section -> review_section
Story-plan/design_section is legacy compatibility only.
Excerpt probes are read-only calibration packets outside this lifecycle.

Bounded writer evidence access:
python scripts/draft_evidence.py products/<slug> <task-id> scope
python scripts/draft_evidence.py products/<slug> <task-id> sources
python scripts/draft_evidence.py products/<slug> <task-id> source --id SRC-0001
python scripts/draft_evidence.py products/<slug> <task-id> search --query "term"
python scripts/draft_evidence.py products/<slug> <task-id> record --source-id SRC-0001 --parent-locator "..." --locator "..." --detail "..."

Task lifecycle:
python scripts/task.py list products/<slug>
python scripts/task.py submit products/<slug> <task-id>
python scripts/task.py brief products/<slug> <task-id>
python scripts/task.py state products/<slug> <task-id> closed

Human approval commands:
python scripts/approval.py approve-plan products/<slug>
python scripts/approval.py approve-outline products/<slug>
python scripts/approval.py approve-section products/<slug> P04
python scripts/approval.py request-changes products/<slug> P04 --request "..."
python scripts/approval.py start-new-cycle products/<slug> --request "..."
python scripts/approval.py human-amend-outline products/<slug> --request "..." --path outline.json
python scripts/approval.py human-amend-section products/<slug> P04 --request "..." --path draft.md
python scripts/materialize_sections.py products/<slug> --archive-previous-cycle
"""
)
