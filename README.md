# FriendSyncer

Syncs the Friend list with other Client.  
Supported Client : Future, Rusher, Lambda  
Made it because [FriendSync Mod](https://github.com/ttRMS/Friend-Sync) didn't work for me.  
(Use that mod if that works)

## Requirements

1. Python
2. MojangAPI

## How to Use

1. open the python file.
2. input the .minecraft directory.
3. Ta-da, done!

## Warning

Lambda Client need UUID for adding friends, so I used MojangAPI to get player's uuid.  
However, the MojangAPI only supports Recent Username's UUID, it means the friend added in old past(and nickname changed) won't be added in lambda Friend.  
The program will notice this case of friend's name, add it on your own with that information.
