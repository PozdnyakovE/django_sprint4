from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils import timezone


def real_date(value: datetime) -> None:
    # """Проверка корректной даты при создании публикации."""
    # if value.astimezone() < timezone.now():
    #     raise ValidationError(
    #         'Ожидается текущая дата или дата отложенной публикации'
    #     )
    pass
