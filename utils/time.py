from datetime import datetime, timezone


class Time:
    def currently_date_utcnow():
        return datetime.now(timezone.utc)
