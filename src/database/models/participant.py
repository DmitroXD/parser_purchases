from tortoise import fields

from .abstract_base import AbstractBaseModel


class Participant(AbstractBaseModel):
    number = fields.CharField(max_length=20, null=False, unique=True)

    class Meta:
        table = "participants"
