#!/usr/bin/env python3

print(
    """YT Production

make new PRODUCT=<slug> TITLE="Tên làm việc"
make task PRODUCT=<slug> OPERATION=research_plan
make task PRODUCT=<slug> OPERATION=research_workstream UNIT=WS01
make task PRODUCT=<slug> OPERATION=design_section SECTION=P04
make task PRODUCT=<slug> OPERATION=draft_section SECTION=P04
make show PRODUCT=<slug>
make brief PRODUCT=<slug> TASK=<task-id>
make check PRODUCT=<slug>
make research-units PRODUCT=<slug>
make sections PRODUCT=<slug>
make impact PRODUCT=<slug> CLAIM=CLM-0001
make impact PRODUCT=<slug> SECTION=P04
make assemble PRODUCT=<slug>
make test

Task lifecycle:
python scripts/task.py list products/<slug>
python scripts/task.py submit products/<slug> <task-id>
python scripts/task.py brief products/<slug> <task-id>
python scripts/task.py state products/<slug> <task-id> closed

Human approval commands:
python scripts/approval.py approve-plan products/<slug>
python scripts/approval.py approve-outline products/<slug>
python scripts/approval.py approve-story-plan products/<slug> P04
python scripts/approval.py approve-section products/<slug> P04
python scripts/approval.py request-changes products/<slug> P04 --request "..."
"""
)
