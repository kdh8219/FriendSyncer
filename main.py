from dataclasses import dataclass
import json
from mojang import API as MojangAPI
import os
from typing import Union


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

    # input : None
    # output : bool (detected or not)
    def detect(self) -> bool: ...

    # input : None
    # output : list[minecraftAccount] or false (fail)
    def read(self) -> Union[list[MinecraftAccount], bool]: ...

    # input : list[minecraftAccount]
    # output : bool (success or fail)
    def write(self, friendList: list[MinecraftAccount]) -> bool: ...


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
        def removeDash(uuid: str):
            return uuid.replace("-", "")
        friends: list[MinecraftAccount] = []
        try:
            with json.load(open(f"{self.minecraftDirectory}/lambda/friends.json")) as file:
                for friend in file["firends"]:
                    friends.append(MinecraftAccount(
                        id=friend["name"],
                        uuid=removeDash(friend["uuid"])
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


# TODO: @kdh8219 in 퓨쳐 없는 사람 == True; 이거 버그날 가능성 농후...
class Future(HackClient):
    clientName: str = "Future"
    readable: bool = True
    writeable: bool = True

    def __init__(self, minecraftDirectory: str) -> None:
        super().__init__(minecraftDirectory)

    def detect(self) -> bool:
        userprofile = os.environ.get("USERPROFILE")
        if not userprofile:
            return False
        if not os.listdir(userprofile):
            return False
        try:
            json.load(open(f"{userprofile}/Future/friends.json"))
            return True
        except:
            return False

    def read(self) -> Union[list[MinecraftAccount], bool]:
        friends: list[MinecraftAccount] = []
        userprofile = os.environ.get("USERPROFILE")
        if not userprofile:
            return False
        try:
            mojnagAPI = MojangAPI()
            with json.load(open(f"{userprofile}/Future/friends.json")) as file:
                for _ in file:
                    for friend in _:
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
        return super().write(friendList)  # TODO


class Abyss(HackClient):
    clientName: str = "Abyss"
    readable: bool = True
    writeable: bool = True

    def __init__(self, minecraftDirectory: str) -> None:
        super().__init__(minecraftDirectory)

    def detect(self) -> bool:
        if not ("Abyss" in os.listdir(path=self.minecraftDirectory)):
            return False
        try:
            json.load(
                open(f"{self.minecraftDirectory}/Abyss/FriendList.json"))
            return True
        except:
            return False

    def read(self) -> Union[list[MinecraftAccount], bool]:
        def removeDash(uuid: str) -> str:
            return uuid.replace("-", "")
        friends: list[MinecraftAccount] = []
        try:
            with json.load(open(f"{self.minecraftDirectory}/Abyss/FriendList.json")) as file:
                for friend_id in file.keys:
                    friends.append(MinecraftAccount(
                        id=friend_id,
                        uuid=removeDash(file[friend_id])
                    ))
                return friends
        except:
            return False

    def write(self, friendList: list[MinecraftAccount]) -> bool:
        def makeDash(uuid: str) -> str:
            return f"{uuid[:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}"
        try:
            with open(f"{self.minecraftDirectory}/Abyss/FriendList.json") as file:
                data: dict = {}
                for friend in friendList:
                    data[friend.id] = makeDash(friend.uuid)
                file.write(json.dumps(data, indent=2))
            return True
        except:
            return False


class Impact(HackClient):
    clientName: str = "Impact"
    readable: bool = True
    writeable: bool = True

    def __init__(self, minecraftDirectory: str) -> None:
        super().__init__(minecraftDirectory)

    def detect(self) -> bool:
        if not ("Impact" in os.listdir(path=self.minecraftDirectory)):
            return False
        try:
            open(f"{self.minecraftDirectory}/Impact/Friends.cfg")
            return True
        except:
            return False

    def read(self) -> Union[list[MinecraftAccount], bool]:
        friends: list[MinecraftAccount] = []
        try:
            mojnagAPI = MojangAPI()
            with open(f"{self.minecraftDirectory}/Impact/Friends.cfg") as file:
                for friend in file.readlines():
                    uuid = mojnagAPI.get_uuid(friend[0:friend.find(':')])
                    if uuid:
                        friends.append(MinecraftAccount(
                            id=friend[0:friend.find(':')],
                            uuid=uuid
                        ))
                return friends
        except:
            return False

    def write(self, friendList: list[MinecraftAccount]) -> bool:
        try:
            with open(f"{self.minecraftDirectory}/Impact/Friends.cfg") as file:
                data: str = ""
                for friend in friendList:
                    data = f"{data}{friend.id}:{friend.id}\n"
                file.write(data)
            return True
        except:
            return False
