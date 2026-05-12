from typing import Any, Dict, Iterable, Mapping


def _get_bool(value: Any) -> bool:
    """Coerces a value to bool safely."""
    return bool(value)


def _get_number(value: Any) -> float:
    """Returns numeric value or 0.0."""
    try:
        if value is None:
            return 0.0
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def calculate_task_metrics(tasks: Iterable[Mapping[str, Any]]) -> Dict[str, float]:
    """Compute aggregate task metrics."""
    tasks_list = list(tasks)
    total = len(tasks_list)

    completed = sum(1 for t in tasks_list if _get_bool(t.get("done", False)))
    pending = total - completed

    estimated_hours = sum(_get_number(t.get("estimate")) for t in tasks_list)
    remaining_hours = sum(
        _get_number(t.get("estimate"))
        for t in tasks_list
        if not _get_bool(t.get("done", False))
    )

    completion_percent = round((completed / total * 100.0), 2) if total else 0.0

    return {
        "total": float(total),
        "completed": float(completed),
        "pending": float(pending),
        "completion_percent": float(completion_percent),
        "estimated_hours": float(estimated_hours),
        "remaining_hours": float(remaining_hours),
    }
