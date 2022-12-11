# FriendSyncer.py
import os
import json
import sys
import time
from mojang import MojangAPI

minecraftdir = input(
    "Input .minecraft's directory. \nEx) C:\\Users\\meltd\\AppData\\Roaming\\.minecraft \nInput : ")
friendList = []
futuredir = ""
nameUUID = {}
detectedClient = {"Future": False, "Rusher": False, "Lambda": False}
userprofiledir = os.environ.get("USERPROFILE")
print("")
if (userprofiledir != ""):
    os.chdir(userprofiledir)
    if ("Future" in os.listdir()):
        try:
            with open("{0}/Future/friends.json".format(userprofiledir)) as futureFile:
                friendFJson = json.load(futureFile)
                print("Found Future Client folder : {0}\\Future, Grabbing Friends...".format(
                    userprofiledir))
                addcnt = 0
                for i in range(len(friendFJson)):
                    friendNick = friendFJson[i]['friend-label']
                    if (friendNick not in friendList):
                        friendList.append(friendNick)
                        addcnt += 1
                fname = "friend" if addcnt <= 1 else "friends"
                print("Added {0} {1} in FriendList from Future".format(
                    addcnt, fname), end="")
                detectedClient["Future"] = True
                if (addcnt == len(friendFJson)):
                    print(".")
                else:
                    print(", {0} overlapped.".format(len(friendFJson)-addcnt))
                print("")
        except Exception as e:
            print("Error : {0}\n".format(e))
try:
    os.chdir(minecraftdir)
except FileNotFoundError:
    print("Can't find Minecraft folder, Exiting Program...")
    end = input()
    sys.exit()
except OSError:
    print("Can't find Minecraft folder, Exiting Program...")
    end = input()
    sys.exit()
if (os.getcwd() == minecraftdir):
    if ("rusherhack" in os.listdir()):
        print("Found rusherhack Folder, grabbing friends...")
        try:
            with open("{0}/rusherhack/friends.json".format(minecraftdir)) as rusherFile:
                friendRJson = json.load(rusherFile)
                addcnt = 0
                for i in range(len(friendRJson)):
                    friendNick = friendRJson[i]['name']
                    if (friendNick not in friendList):
                        friendList.append(friendNick)
                        addcnt += 1
                fname = "friend" if addcnt <= 1 else "friends"
                print("Added {0} {1} in FriendList from Rusher".format(
                    addcnt, fname), end="")
                detectedClient["Rusher"] = True
                if (addcnt == len(friendRJson)):
                    print(".")
                else:
                    print(", {0} overlapped.".format(len(friendRJson)-addcnt))
                print("")
        except Exception as e:
            print("Error : {0}\n".format(e))
    if ("lambda" in os.listdir()):
        print("Found Lambda Client Folder, grabbing friends...")
        try:
            with open("{0}/lambda/friends.json".format(minecraftdir)) as lambdaFile:
                friendLJson = json.load(lambdaFile)
                addcnt = 0
                for i in range(len(friendLJson["Friends"])):
                    nameUUID[friendLJson["Friends"][i]['name']
                             ] = friendLJson["Friends"][i]['uuid']
                    friendNick = friendLJson["Friends"][i]['name']
                    if (friendNick not in friendList):
                        friendList.append(friendNick)
                        addcnt += 1
                fname = "friend" if addcnt <= 1 else "friends"
                print("Added {0} {1} in FriendList from Lambda".format(
                    addcnt, fname), end="")
                detectedClient["Lambda"] = True
                if (addcnt == len(friendLJson["Friends"])):
                    print(".")
                else:
                    print(", {0} overlapped.".format(
                        len(friendLJson["Friends"])-addcnt))
                print("")
        except Exception as e:
            print("Error : {0}\n".format(e))
print("Friends Count : {0}".format(len(friendList)))
print("Trying to add friends...\n")
if (detectedClient["Future"]):
    futureJsonBuilder = []
    for i in friendList:
        futureJsonBuilder.append({"friend-label": i, "friend-alias": i})
    with open("{0}/Future/friends.json".format(userprofiledir), "w") as futureFile:
        futureFile.write(json.dumps(futureJsonBuilder, indent=2))
    print("Future : Complete.\n")
if (detectedClient["Rusher"]):
    rusherJsonBuilder = []
    for i in friendList:
        rusherJsonBuilder.append({"name": i})
    with open("{0}/rusherhack/friends.json".format(minecraftdir), "w") as rusherFile:
        rusherFile.write(json.dumps(rusherJsonBuilder, indent=2))
    print("Rusher : Complete.\n")
if (detectedClient["Lambda"]):
    lambdaJsonBuilder = {"Enabled": True}
    cnt = 1
    chunks = [friendList[x:x+10] for x in range(0, len(friendList), 10)]
    for i in chunks:
        uuids = MojangAPI.get_uuids(i)
        for name, uuid in uuids.items():
            nameUUID[name] = uuid[:8]+"-"+uuid[8:12]+"-" + \
                uuid[12:16]+"-"+uuid[16:20]+"-"+uuid[20:]
        print(
            "Grabbing UUID from MojangAPI...({0}/{1})".format(cnt, len(chunks)))
        time.sleep(3)  # ratelimit
        cnt += 1
    lambdaFriendList = []
    addList = []
    errorList = []
    for i in friendList:
        try:
            lambdaFriendList.append({"uuid": nameUUID[i], "name": i})
            addList.append(i.lower())
        except KeyError:
            errorList.append(i)
    for i in errorList:
        if (i.lower() in addList):
            print(
                "Can't Find {0}'s UUID, but there are same nickname in FriendList with only lower/uppercase Difference, it seems like overlapped.".format(i))
        else:
            print(
                "Can't Find {0}'s UUID, Please update to Recent Nickname, this friend will be ignored in add List.".format(i))
    lambdaJsonBuilder["Friends"] = lambdaFriendList
    with open("{0}/lambda/friends.json".format(minecraftdir), "w") as lambdaFile:
        lambdaFile.write(json.dumps(lambdaJsonBuilder, indent=2))
    print("Lambda : Complete.")
end = input()
