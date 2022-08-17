import argparse
from genericpath import isfile
import pickle
from ftplib import FTP
import time
import os
import datetime

ftp = None

def connect_ftp(hostname, username, password):
    try:
        global ftp
        
        #Creates a socket to connect to FTP server
        ftp = FTP(hostname)
        ftp.login(username, password)

        print("Connected")
        keep_conn(args)

    
    except:
        print("Unable to connect")
        print("\nClosing in 5 seconds")
        time.sleep(5)
        quit()
    

def keep_conn(cred):
    #creates pickle file to store ftp creds
    file_conn = open('ftp_conn.obj', 'wb')
    pickle.dump(cred, file_conn)

def conn_exists():
    #Checks if the pickle file exists 
    if os.path.isfile("/Users/arangill/Desktop/ftp_conn.obj"):
        if os.path.getsize("/Users/arangill/Desktop/ftp_conn.obj") > 0:      
            open_conn = open('/Users/arangill/Desktop/ftp_conn.obj', 'rb') 
            conn = pickle.load(open_conn)

            #Connects to FTP using creds from pickle
            connect_ftp(conn.hostname[0], conn.username[0], conn.password[0])
            #Stores creds for next time
            keep_conn(conn)

            return True

    #If file does not exist
    return False

def download_file(date, time):
    #reformats date and time to match csv files
    final = date + " " + time
    final = datetime.datetime.strptime(final, "%d-%m-%Y %H:%M:%S").strftime("%Y%m%d%H%M%S")
    filename = "MED_DATA_" + final + ".csv"

    #Downloads File    
    with open(filename, "wb") as f:
        ftp.retrbinary("RETR " + filename, f.write)
        print("Successfully downloaded " + filename)
    
    
def main():
        global args
        parser = argparse.ArgumentParser(description="A CLI FTP Client")

        parser.add_argument("-hn", "--hostname", 
                            type = str, 
                            nargs = 1,  
                            metavar = "hostname", 
                            help = "Hostname of FTP server")

        parser.add_argument("-u", "--username", 
                            type = str, 
                            nargs = 1,  
                            metavar = "username", 
                            help = "Username to connect to FTP")

        parser.add_argument("-p,", "--password", 
                            type = str, 
                            nargs = 1,  
                            metavar = "password", 
                            help = "Password to connect to FTP")

        parser.add_argument("-s,", "--schedule", 
                            type = str, 
                            nargs = 2,  
                            metavar = "date_time", 
                            help = "Specify the date and time to download the file as DD-MM-YYYY HH:MM:SS")


        args = parser.parse_args()

        #Checks if pickle exists from previous session
        if conn_exists():
            pass

        #If user is starting a new session
        if args.hostname != None and args.username != None and args.password != None:
            connect_ftp(args.hostname[0], args.username[0], args.password[0])
        
        #If user has entered data for schedule
        if args.schedule != None:
            download_file(args.schedule[0], args.schedule[1])


if __name__ == "__main__":
    main()