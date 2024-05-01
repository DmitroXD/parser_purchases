from tortoise import fields

from .abstract_base import AbstractBaseModel

"""
    Модель администраторов в боте. 
    Если включен мидлварь, то бот будет регировать только на людей из этой модели
"""


class Admin(AbstractBaseModel):
    id_tg = fields.BigIntField(null=False, unique=True)

    class Meta:
        table = 'admins'
