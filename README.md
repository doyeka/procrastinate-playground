# procrastinate-playground

Minimal Django + Procrastinate setup that registers 70 periodic tasks scheduled every 15 minutes.

## What it does

- Registers 70 periodic tasks using `@app.periodic(cron="*/15 * * * *")`.
- Each run writes a single line with `JobContext` details to per-task log files in `periodic_logs/`.

## Where tasks are defined

- Procrastinate app and periodic registrations: `playground/procrastinate_app.py`
- Django setting pointing to the app: `PROCRASTINATE_APP = 'playground.procrastinate_app.app'` in `playground/settings.py`.

## How to run (example)

Below are example commands you can adapt to your environment. You'll need a Postgres database accessible via Django's settings (the Django connector uses your default DB). This repo ships with SQLite for Django itself, but Procrastinate requires Postgres. Configure your Django `DATABASES` accordingly before running.

```bash
# Install deps (Python 3.11)
poetry install --no-root

# Apply Procrastinate schema to your Postgres DB
poetry run procrastinate --app=playground.procrastinate_app.app schema --apply

# Start the scheduler (defers periodic jobs)
poetry run procrastinate --app=playground.procrastinate_app.app scheduler --defer-periodic

# In another terminal, run a worker to execute jobs
poetry run procrastinate --app=playground.procrastinate_app.app worker
```

Logs will be written under `periodic_logs/task_<n>.log`.

## Notes

- Each periodic registration uses a distinct `periodic_id` (e.g., `every15_task_1` … `every15_task_70`).
- The task receives `JobContext` (`worker_id`, `job_id`, `scheduled_at`), which is appended to the corresponding log file.
