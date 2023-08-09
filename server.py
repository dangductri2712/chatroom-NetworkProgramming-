import threading  #thread is a sequence of instruction within a program. => Running multiple thread = running multiple program
import socket
host='127.0.0.1'   #warning: There will be some preserved host. To find out, go on "Command Prompt" and type "netstat"
port = 59000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
aliases = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message=client.recv(1024)  #only accept 1024 bytes
            broadcast(message)
        except:  #in case of error, find the index of the client and aliases that is causing the erorr and delete it
            index = clients.index(client)
            client.remove(index)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room'.encode('utf-8'))
            aliases.remove(alias)
            break

def receive():
    while True:
        print('Server is running and listening...')
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        print(f'The alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias} has connected to the chat room'.encode('utf-8'))
        client.send('you are now conneted'.encode('utf-8'))
        thread = threading.Thread(target = handle_client, args= (client,))
        thread.start()

if(__name__ == "__main__"):
    receive()
    #not check yet