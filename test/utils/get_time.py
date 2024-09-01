from time import time
from datetime import datetime


def get_time(function, name: str):

    def wrapper(*args, **kwargs):
        start = time()
        function(*args, **kwargs)
        end = time()

        time_taken = end - start

        with open("test/time_taken.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().strftime("%d/%m/%Y")} :: {name} :: {time_taken} seconds\n")

    return wrapper
