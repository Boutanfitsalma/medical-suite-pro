from datetime import datetime, timedelta

def generate_time_slots():
    slots = []
    start_times = [("09:00", "12:00"), ("14:00", "18:00")]
    days_ahead = 7  # une semaine

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    for day_offset in range(days_ahead):
        day = today + timedelta(days=day_offset)
        if day.weekday() < 6:  # Lundi (0) à Samedi (5)
            for start_str, end_str in start_times:
                start = datetime.strptime(start_str, "%H:%M")
                end = datetime.strptime(end_str, "%H:%M")
                current = start
                while current < end:
                    slot_time = day.replace(hour=current.hour, minute=current.minute)
                    slots.append({
                        "datetime": slot_time.strftime("%Y-%m-%d %H:%M"),
                        "status": "available"
                    })
                    current += timedelta(minutes=30)
    return slots
