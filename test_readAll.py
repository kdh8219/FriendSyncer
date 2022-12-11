import Clients

clients = [Clients.Abyss, Clients.Future, Clients.Impact,
           Clients.LambdaClient, Clients.RusherHack]
clients = map(lambda it: it(input("dot minecraft file location:")), clients)

print(list(map(lambda it: it.read(), clients)))
