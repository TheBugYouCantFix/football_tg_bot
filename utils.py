from aiojobs import Scheduler
import pycountry as pc


def get_scheduler(dp) -> Scheduler:
    """
    Не совсем честная helper функция, получающая планировщик задач из глобальной переменной.

    Да, почти никогда так нельзя и лучше уж использовать `contextvars`, но данный пример учебный,
    поэтому тут льзя (да и на самом деле, с глобальными объектами для ботов так можно делать)
    :return:
    """
    return dp.storage.scheduler


def has_year(text: str) -> bool:
    text = text.split()

    for i in text:
        if i.isdigit() and int(i) > 1000:
            return True

    return False