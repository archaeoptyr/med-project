from ftplib import FTP
import time

ftp = ""
hostname = input("Enter Hostname: ")
username = input("Enter Username: ")
password = input("Enter Password: ")

def connect_ftp(hostname, username, password):
    try:
        global ftp
        ftp = FTP(hostname)
        ftp.login(username, password)
    
        print("Connected to: " + hostname)
        
    except:
        print("Unable to connect")
        print("\nClosing in 5 seconds")
        time.sleep(5)
        quit()

def list_files():
    print()
    ftp.retrlines('LIST')


def download_file(filename):
    with open(filename, "wb") as f:
        ftp.retrbinary("RETR " + filename, f.write)
        print("Successfully downloaded " + filename)

def print_directory():
    return ftp.pwd()
    

def change_directory(new_directory):
    ftp.cwd(new_directory)

    print("Changed to " + print_directory())



connect_ftp(hostname, username, password)

while True:
    user_input = input("\n" + username + "@" + hostname + "> ")

    try:
        command = user_input.split()[0]
        try:
            parameter = user_input.split()[1]
            
            if command == "download":
                download_file(parameter)

            elif command == "cd":
                change_directory(parameter)
         
        except:
            print()
            

        if command == "pwd":
            print(print_directory())

        elif command == "ls":
            list_files()
 
        elif command == "exit":
            ftp.quit()
            print("Server disconnected")
            print()
            break

        
       
        
    except:
        print("Please provide a command")
