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
