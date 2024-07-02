from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils import timezone


def real_date(value: datetime) -> None:
    # print(value.astimezone().date())
    # print(timezone.now().date())
    if value.astimezone().date() < timezone.now().date():
        raise ValidationError(
            'Ожидается текущая дата или дата отложенной публикации'
        ) 