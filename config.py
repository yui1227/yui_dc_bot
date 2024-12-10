import json


class Config:
    def __init__(self):
        with open("secret.json", mode='r', encoding='utf-8') as f:
            self._setting = json.load(f)

    @property
    def pc_mac(self) -> str:
        return self._setting["pc_mac"]

    @property
    def dc_token(self) -> str:
        return self._setting["dc_token"]

    @property
    def author(self) -> int:
        return self._setting["author"]

    @property
    def run_server(self) -> list[int]:
        return self._setting["run_server"]

    @property
    def repost_list(self) -> list[dict[str, int]]:
        return self._setting["repost_list"]
