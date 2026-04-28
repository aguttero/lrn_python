from sqlalchemy.orm import Session
from sqlalchemy.dialects.sqlite import insert
from datetime import date


def upsert_groups(session: Session, api_response: list[dict]) -> dict:
    """
    Upsert Groups using SQLite's native INSERT ... ON CONFLICT DO UPDATE.
    Matches on group_id (unique natural key). Never touches the internal PK.

    Args:
        session:      Active SQLAlchemy Session.
        api_response: List of dicts from the API. Must include 'group_id'.

    Returns:
        Summary dict: {"inserted": int, "updated": int, "skipped": int, "errors": list}
    """
    if not api_response:
        return {"inserted": 0, "updated": 0, "skipped": 0, "errors": []}

    summary  = {"inserted": 0, "updated": 0, "skipped": 0, "errors": []}
    today    = date.today()
    seen     = set()   # intra-batch duplicate guard
    rows     = []

    # --- 1. Validate and normalize the batch into plain dicts ---
    for record in api_response:
        group_id = (record.get("group_id") or "").strip()

        if not group_id:
            summary["skipped"] += 1
            summary["errors"].append({"record": record, "reason": "Missing group_id"})
            continue

        if group_id in seen:
            summary["skipped"] += 1
            summary["errors"].append({"record": record, "reason": "Duplicate group_id in batch"})
            continue

        seen.add(group_id)
        rows.append({
            "group_id"      : group_id,
            "name"          : record["name"],
            "created_date"  : record.get("created_date", today),
            "admin_email"   : record.get("admin_email"),
            "is_default_grp": record.get("is_default_grp", False),
            "last_sync"     : today,
        })

    if not rows:
        return summary

    # --- 2. Build the INSERT ... ON CONFLICT DO UPDATE statement ---
    try:
        stmt = insert(Group).values(rows)

        stmt = stmt.on_conflict_do_update(
            index_elements=["group_id"],    # the unique column to match on
            set_={                          # columns to overwrite on conflict
                "name"          : stmt.excluded.name,
                "admin_email"   : stmt.excluded.admin_email,
                "is_default_grp": stmt.excluded.is_default_grp,
                "last_sync"     : stmt.excluded.last_sync,
                # created_date intentionally excluded — never overwrite on update
                # id (PK) intentionally excluded — never touch the internal PK
            }
        )

        result = session.execute(stmt)
        session.commit()

        # rowcount reflects total rows touched (inserted + updated)
        total          = result.rowcount
        pre_existing   = session.query(Group.group_id)\
                                .filter(Group.group_id.in_(seen))\
                                .count()
        summary["updated"]  = pre_existing
        summary["inserted"] = total - pre_existing

    except Exception as exc:
        session.rollback()
        summary["errors"].append({"reason": str(exc)})
        summary["skipped"] += len(rows)

    return summary