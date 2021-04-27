import requests
import multiprocessing as mp
from retry import retry
import functools


API_URL = "https://public.api.openprocurement.org/api/2.5"

     
@retry(Exception, tries = 420, delay = 15, backoff=1.5, max_delay = 300)
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


@retry(Exception, tries = 420, delay = 15, backoff=1.5, max_delay = 300)
def _get_object(name, id):
    r = requests.get(f"{API_URL}/{name}/{id}", timeout=15)
    page = r.json()
    return page["data"]


def _get_obj_by_def(o, name):
    """
    Це функція, яка буде у багато потоків одночасно запускатись.
    """
    return _get_object(name, o["id"])


def get_objects_stream(name, start_offset, end_offset):
    pool = mp.Pool(8)

    id_stream = _get_objects_gen(name, start_offset, end_offset)
    task = functools.partial(_get_obj_by_def, name=name)
 
    yield from pool.imap(task, id_stream)


