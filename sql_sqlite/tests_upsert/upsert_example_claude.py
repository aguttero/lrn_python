from sqlalchemy.orm import Session
from datetime import date


def upsert_groups(session: Session, api_response: list[dict]) -> dict:
    """
    Upsert Groups from an API response using group_id as the natural key.
    Uses session.merge() after resolving the internal PK via group_id lookup.

    Args:
        session:      Active SQLAlchemy Session.
        api_response: List of dicts from the API. Must include 'group_id'.

    Returns:
        Summary dict: {"inserted": int, "updated": int, "skipped": int, "errors": list}
    """
    if not api_response:
        return {"inserted": 0, "updated": 0, "skipped": 0, "errors": []}

    summary = {"inserted": 0, "updated": 0, "skipped": 0, "errors": []}
    today = date.today()

    # Single prefetch — map group_id → internal PK for the whole batch
    existing: dict[str, int] = {
        group_id: pk
        for pk, group_id in session.query(Group.id, Group.group_id).all()
    }

    for record in api_response:
        api_group_id = (record.get("group_id") or "").strip()

        if not api_group_id:
            summary["skipped"] += 1
            summary["errors"].append({"record": record, "reason": "Missing group_id"})
            continue

        try:
            internal_pk = existing.get(api_group_id)   # None → INSERT, int → UPDATE
            is_new = internal_pk is None

            group = Group(
                id             = internal_pk,           # None lets DB assign PK on insert
                group_id       = api_group_id,
                name           = record["name"],
                created_date   = record.get("created_date", today),
                admin_email    = record.get("admin_email"),
                is_default_grp = record.get("is_default_grp", False),
                last_sync      = today,
            )

            session.merge(group)                        # INSERT or UPDATE based on PK

            if is_new:
                existing[api_group_id] = ...            # guard intra-batch duplicates
                summary["inserted"] += 1
            else:
                summary["updated"] += 1

        except Exception as exc:
            session.rollback()
            summary["errors"].append({"record": record, "reason": str(exc)})
            summary["skipped"] += 1

    session.commit()
    return summary