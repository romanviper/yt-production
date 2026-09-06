from __future__ import annotations

# Compatibility entrypoint. The implementation lives in feedback_runtime so the
# prototype can evolve without duplicating the CLI/import surface used by tests
# and operator commands.
from .feedback_runtime import (  # noqa: F401
    FeedbackError,
    _replace_only_beat,
    build_feedback,
    ingest_measurement,
    load_json,
    main,
    prepare_case,
    resolve_single_sample_locator,
    resolve_source_ref,
    show_state,
    validate_guided_artifact,
    validate_instance,
    verify_case_bundle,
)


if __name__ == "__main__":
    raise SystemExit(main())
