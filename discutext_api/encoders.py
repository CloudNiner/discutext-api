from datetime import datetime


def datetime_encoder(dt: datetime) -> str:
    return dt.isoformat()
