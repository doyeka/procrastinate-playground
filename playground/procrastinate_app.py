from __future__ import annotations

import os
from pathlib import Path

import procrastinate
from procrastinate.contrib.django import DjangoConnector


# Initialize Procrastinate app with Django connector
app = procrastinate.App(connector=DjangoConnector())


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "periodic_logs"
LOG_DIR.mkdir(exist_ok=True)


def _write_line_safely(file_path: Path, line: str) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(line + "\n")


# Base task function receiving JobContext; we will configure it per periodic
@app.task(name="write_worker_info", pass_context=True)
def write_worker_info(context: procrastinate.JobContext, task_index: int) -> None:
    worker_id = getattr(context, "worker_id", "unknown")
    job_id = getattr(context, "job_id", "unknown")
    scheduled_at = getattr(context, "scheduled_at", None)
    # Compose a single-line log for easy grepping
    line = (
        f"task_index={task_index} worker_id={worker_id} job_id={job_id} scheduled_at={scheduled_at}"
    )
    _write_line_safely(LOG_DIR / f"task_{task_index}.log", line)


# Register 70 periodic tasks, each every 15 minutes
for i in range(1, 71):
    periodic_id = f"every15_task_{i}"
    # Configure the base task with a distinct task_index so each periodic is unique
    configured = write_worker_info.configure(task_kwargs={"task_index": i})
    app.periodic(cron="*/15 * * * *", periodic_id=periodic_id)(configured)

