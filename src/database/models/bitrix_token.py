from tortoise import fields

from .abstract_base import AbstractBaseModel

"""
    Модель ключей битрикса. 
"""


class BitrixToken(AbstractBaseModel):
    value = fields.CharField(max_length=100, null=False, unique=True)

    class Meta:
        table = "bitrix_tokens"
