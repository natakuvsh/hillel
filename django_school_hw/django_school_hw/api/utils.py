from datetime import datetime, timezone

def create_date(today):
    d, m, y = int(today.strftime("%d")), int(today.strftime("%m")), int(today.strftime("%Y"))
    return datetime(y, m, d, 00, 00, 00, tzinfo=timezone.utc)