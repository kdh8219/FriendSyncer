from typing import Union
from dataclasses import dataclass
import os
import json
from mojang import API as MojangAPI


@dataclass
class MinecraftAccount:
    id: str
    uuid: str


class HackClient():
    clientName: str
    readable: bool
    writeable: bool

    def __init__(self, minecraftDirectory: str) -> None:
        self.minecraftDirectory: str = minecraftDirectory

    def detect(self) -> bool: ...
    # input : None
    # output : bool (detected or not)

    def read(self) -> Union[list[MinecraftAccount], bool]: ...
    # input : None
    # output : list[minecraftAccount] or false (fail)

    def write(self, friendList: list[MinecraftAccount]) -> bool: ...
    # input : list[minecraftAccount]
    # output : bool (success or fail)


class LambdaClient(HackClient):
    clientName: str = "Lambda"
    readable: bool = True
    writeable: bool = True

    def __init__(self, minecraftDirectory: str) -> None:
        super().__init__(minecraftDirectory)

    def detect(self) -> bool:
        if not ("lambda" in os.listdir(path=self.minecraftDirectory)):
            return False
        try:
            json.load(open(f"{self.minecraftDirectory}/lambda/friends.json"))
            return True
        except:
            return False

    def read(self) -> Union[list[MinecraftAccount], bool]:
        friends: list[MinecraftAccount] = []
        try:
            with json.load(open(f"{self.minecraftDirectory}/lambda/friends.json")) as file:
                for friend in file["firends"]:
                    friends.append(MinecraftAccount(
                        id=friend["name"],
                        uuid=friend["uuid"]
                    ))
            return friends
        except:
            return False

    def write(self, friendList: list[MinecraftAccount]) -> bool:
        def makeDash(uuid: str) -> str:
            return f"{uuid[:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}"

        data = {"Enabled": True, "Friends": []}
        for friend in friendList:
            data["Friends"].append(
                {
                    "uuid": makeDash(friend.uuid),
                    "name": friend.id
                }
            )
        try:
            with open(f"{self.minecraftDirectory}/lambda/friends.json") as file:
                file.write(json.dumps(data, indent=2))
            return True
        except:
            return False


class RusherHack(HackClient):
    clientName: str = "Rusherhack"
    readable: bool = True
    writeable: bool = True

    def __init__(self, minecraftDirectory: str) -> None:
        super().__init__(minecraftDirectory)

    def detect(self) -> bool:
        if not ("rusherhack" in os.listdir(path=self.minecraftDirectory)):
            return False
        try:
            json.load(
                open(f"{self.minecraftDirectory}/rusherhack/friends.json"))
            return True
        except:
            return False

    def read(self) -> Union[list[MinecraftAccount], bool]:
        friends: list[MinecraftAccount] = []
        try:
            mojnagAPI = MojangAPI()
            with json.load(open(f"{self.minecraftDirectory}/rusherhack/friends.json")) as file:
                for friend in file:
                    uuid = mojnagAPI.get_uuid(friend['name'])
                    if uuid:
                        friends.append(MinecraftAccount(
                            id=friend['name'],
                            uuid=uuid
                        ))
                return friends
        except:
            return False

    def write(self, friendList: list[MinecraftAccount]) -> bool:
        try:
            with open(f"{self.minecraftDirectory}/rusherhack/friends.json") as file:
                data: list = []
                for friend in friendList:
                    data.append({
                        "name": friend.id
                    })
                file.write(json.dumps(data, indent=2))
            return True
        except:
            return False


# class FileData(HackClient):
#     clientName: str = "friends file"
#     readable: bool = True
#     writeable: bool = False
#     fileDirectory: str  # TODO: 파일 위치 어케받아옴;;
#
#     def __init__(self, minecraftDirectory: str) -> None:
#         super().__init__(minecraftDirectory)
#
#     def detect(self) -> bool:  # TODO
#         ...
#
#     def read(self) -> Union[list[MinecraftAccount], bool]:  # TODO
#         ...
#
#     def write(self, friendList: list[MinecraftAccount]) -> bool:
#         return False
