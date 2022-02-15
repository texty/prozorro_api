import requests
import multiprocessing as mp
from retry import retry
import functools
import logging
from .utils import chunks

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.WARNING,
    datefmt='%Y-%m-%d %H:%M:%S')


API_URL = "https://public.api.openprocurement.org/api/2.5"


@retry(Exception, delay=15, backoff=1.2, max_delay=600)
def _get_objects_page(name, offset):
    """
    Витягти одну сторінку планів (100 штук)
    """

    r = requests.get(f"{API_URL}/{name}?offset={offset}", timeout=15)
    page = r.json()

    next_page = page["next_page"]
    items = page["data"]

    return next_page, items


def _get_objects_gen(name, start_offset, end_offset):
    """
    Повертає генератор із айдішками планів закупівель
    """

    next_offset = start_offset

    while next_offset < end_offset:
        next_page, items = _get_objects_page(name, next_offset)
        yield from items

        next_offset = next_page["offset"]


@retry(Exception, delay=15, backoff=1.2, max_delay=600)
def _get_object(name, id):
    r = requests.get(f"{API_URL}/{name}/{id}", timeout=15)
    page = r.json()

    # Будемо повертати None, якщо 404.
    # В такому випадку там повідомлення про те, що об'єкт не знайдено, і робити retry не має сенсу
    if r.status_code == 404:
        return None

    return page["data"]


def _get_obj_by_def(o, name):
    """
    Це функція, яка буде у багато потоків одночасно запускатись.
    """
    return _get_object(name, o["id"])


def get_objects_stream(name, start_offset, end_offset, concurrency=8):
    pool = mp.Pool(concurrency)

    id_stream = _get_objects_gen(name, start_offset, end_offset)
    task = functools.partial(_get_obj_by_def, name=name)

    """
    «Споживайте відповідально»:
    
    Тут ми додатково розіб'ємо потік айдішок на досить великі куски, щоб уникнути накопичення в оперативній 
    пам'яті даних, які ніхто не споживає
    
    Коли один воркер забився (напр. в постійному ретраї), а інші побігли вперед і забивають оперативну пам'ять,
    то їх результати накомичують в пам'яті і не можуть бути спожитими
    
    2000 - розмір чанку, він обмежує одночасну кількість результатів від воркерів у пам'яті (виходить ~~ 200Мб)
    """
    the_chunks = chunks(id_stream, 2000)

    for chunk in the_chunks:
        yield from pool.imap(task, list(chunk))

