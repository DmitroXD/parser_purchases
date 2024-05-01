from tortoise import Tortoise


__base_path = "database.models"


async def async_database_init(db_url: str) -> None:
    await Tortoise.init(
        db_url=db_url,
        modules={'models': [
            f"{__base_path}.admin",
            f"{__base_path}.bitrix_token",
            f"{__base_path}.participant",
        ]}
    )
    await Tortoise.generate_schemas()
