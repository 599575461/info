import json


class Losder:
    def __init__(self):
        pass

    @staticmethod
    def read_json_file(file: str) -> dict:
        with open(file, "r", encoding="utf-8") as w:
            return json.load(w)

    @staticmethod
    def read_qss_file(file: str) -> str:
        with open(file, "r", encoding="utf-8") as w:
            return w.read()

    @staticmethod
    def write_json_file(file: str, obj: dict) -> None:
        with open(file, "w+", encoding="utf-8") as w:
            json.dump(obj, w)
