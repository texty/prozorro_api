import json
from tqdm import tqdm
import os
import pathlib
import prozorro_api as pr

# script directory
DIR = os.path.dirname(os.path.realpath(__file__))

edr = {"04328565", "04394616", "04412751", "04400883", "04378379", "04335186", "04358000", "34106981", "04344943",
       "25659941"}

print(f"Searching the following edrpou: {edr}")

# Створимо папку
DATA_DIR = "tenders"
pathlib.Path(os.path.join(DIR, DATA_DIR)).mkdir(parents=True, exist_ok=True)


"""
Основний цикл тут
"""

# get_objects_stream повертає генератор об'єктів (у даному випадку тендерів)
# До генератора треба ставитись як до звичайного списку (list).
# Тобто можна пройтись циклом по кожному об'єкту, який він містить
# Єдина різниця -- це те, що він підвантажує із бази прозорро нові об'єкти по мірі того, як ви їх просите у нього

# tqdm -- це просто ще одна обгортка для красивого progress bar у терміналі

iterator = tqdm(pr.get_objects_stream("tenders", "2019-01-01T00:00:00+03:00", "2020-04-01"))
match_counter = 0
    
for tender in iterator:
    iterator.set_description(f"Знайдено {match_counter}; {tender['dateModified']}")
    
    if tender['procuringEntity']['identifier']['id'] in edr:
        match_counter += 1

        with open(f"{DATA_DIR}/{id}.json", 'w') as outfile:
            json.dump(tender, outfile)


