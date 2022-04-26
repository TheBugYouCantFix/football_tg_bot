import pickle
import os

from pathlib import Path


class PickleObjectSaver:
    EXTENSION = '.pickle'

    @staticmethod
    def get_path(filename):
        path = os.path.relpath(f'../pickle_data/{filename}', './')
        return path

    def save_object(self, obj, name: str) -> None:
        filename = f'{name}.pickle'
        path = self.get_path(filename)

        if Path(path).exists():
            return

        dumped = pickle.dumps(obj)

        with open(path, 'wb') as f:
            f.write(dumped)

    def get_object(self, filename: str):
        path = self.get_path(filename)

        if not Path(path).exists():
            return

        with open(path, 'wb') as f:
            obj = pickle.loads(f.read())

        return obj
