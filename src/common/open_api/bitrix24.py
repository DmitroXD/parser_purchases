from bitrix24 import Bitrix24


class Bitrix:

    def __init__(self, url: str) -> None:
        self.__bt24 = Bitrix24(url)

    def add_lead(self, **data):
        """
        Это лишь пример, вы сами можете указать необходимые данные
        """
        self.__bt24.callMethod(
            "crm.lead.add",
            fields={
                "TITLE": data['Полное наименование'],
                "NAME": data["ФИО"][1],
                "SECOND_NAME": data["ФИО"][2],
                "LAST_NAME": data["ФИО"][0],
                "STATUS_ID": "NEW",
                "ADDRESS_CITY": data['Почтовый адрес'],
                "COMMENTS": "Инн: " + data["ИНН"],
                "UTM_SOURCE": "Список площадок: " + ", ".join(data["Электронная площадка"]),
                "OPENED": "Y",
                "PHONE": [{"VALUE": data['Контактный телефон'], "VALUE_TYPE": "WORK"}],
                "EMAIL": [{"VALUE": data['Адрес электронной почты'], "VALUE_TYPE": "WORK"}],
                "WEB": [{"VALUE": data['Адрес сайта в сети интернет'], "VALUE_TYPE": "WORK"}],
            },
            params={"REGISTER_SONET_EVENT": "Y"})
