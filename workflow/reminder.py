from datetime import datetime, timedelta
 
 
def create_reminder(priority):
 
    if not priority:
        return "No reminder required"
 
    if priority.lower() == "high":
 
        reminder_date = (
            datetime.now()
            +
            timedelta(days=1)
        )
 
        return (
            "Reminder created for "
            + str(reminder_date)
        )
 
    return "No reminder required"
 