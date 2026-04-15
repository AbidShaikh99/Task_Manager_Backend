from sqlalchemy.orm import Session
from app.db import models
from datetime import datetime

def seed_status(db: Session):
    statuses = ["todo", "in progress", "completed"]

    for s in statuses:
        exists = db.query(models.Status).filter(models.Status.name == s).first()
        if not exists:
            db.add(models.Status(name=s))

    db.commit()

def track_task_changes(db, task, updated_data: dict, user_name: str):

    for field, new_value in updated_data.items():
        old_value = getattr(task, field, None)

        if str(old_value) == str(new_value):
            continue


        history_data = {
            "task_id": task.id,
            "updated_by": user_name,
            "field_name": field,
            "old_value": str(old_value),
            "new_value": str(new_value),
            "updated_at": datetime.now()
        }

        if field == "time_estimate":
            history_data["old_time_estimate"] = str(old_value)
            history_data["new_time_estimate"] = str(new_value)

        history = models.TaskHistory(**history_data)
        db.add(history)