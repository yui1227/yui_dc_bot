import json


class Config:
    def __init__(self):
        with open("secret.json", mode='r', encoding='utf-8') as f:
            self.setting = json.load(f)

    def GetPCMAC(self) -> str:
        return self.setting["pc_mac"]

    def GetDcToken(self) -> str:
        return self.setting["dc_token"]

    def GetAuthorId(self) -> int:
        return self.setting["author"]

    def GetRunServerID(self) -> list[int]:
        return self.setting["run_server"]

    def GetRepostGuildChannelIdPair(self) -> list[list[dict[str, int]]]:
        return self.setting["repost_guild_channel_pair"]