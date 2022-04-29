import pickle
import os

from pathlib import Path


class PickleObjectSaver:
    EXTENSION = '.pickle'

    @staticmethod
    def save_object(obj, name: str, update=False) -> None:
        filename = f'{name}.pickle'
        path = os.path.relpath(f'../pickle_data/{filename}', './')

        if Path(path).exists() and not update:
            return

        dumped = pickle.dumps(obj)

        with open(path, 'wb') as f:
            f.write(dumped)

    @staticmethod
    def get_object(filename: str):
        path = os.path.relpath(f'./pickle_data/{filename}', './')
        print(os.path.abspath(path))

        if not Path(path).exists():
            return

        with open(path, 'rb') as f:
            obj = pickle.loads(f.read())

        return obj
