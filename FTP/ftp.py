import argparse
from genericpath import isfile
import pickle
from ftplib import FTP
import time
import os
from datetime import datetime

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
    if os.path.isfile("ftp_conn.obj"):
        if os.path.getsize("ftp_conn.obj") > 0:      
            open_conn = open("ftp_conn.obj", 'rb') 
            conn = pickle.load(open_conn)

            #Connects to FTP using creds from pickle
            connect_ftp(conn.hostname[0], conn.username[0], conn.password[0])
            #Stores creds for next time
            keep_conn(conn)

            return True

    #If file does not exist
    return False

def format_datetime(date, time):
    date_time = date + " " + time
    date_time = datetime.strptime(date_time, "%d-%m-%Y %H:%M:%S").strftime("%Y%m%d%H%M%S")
    return date_time

def format_date(date):
    format_date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y%m%d")
    return format_date

def download_file(date, time):
    #reformats date and time to match csv files
    date_time = format_datetime(date, time)
    filename = "MED_DATA_" + date_time + ".csv"

    #Downloads File    
    with open(filename, "wb") as f:
        ftp.retrbinary("RETR " + filename, f.write)
        print("Successfully downloaded " + filename)
    
def download_file_default(date_now):
    date = format_date(date_now)
    print(date)
    
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
                            nargs = "*",  
                            metavar = "date", 
                            help = "Specify the date and time to download the file as DD-MM-YYYY HH:MM:SS")
        """
        parser.add_argument("-s,", "--schedule", 
                            type = str, 
                            nargs = '',  
                            metavar = "date_time", 
                            help = "Specify the date and time to download the file as DD-MM-YYYY HH:MM:SS")
        """

        args = parser.parse_args()

        #Checks if pickle exists from previous session
        if conn_exists():
            pass

        #If user is starting a new session
        if args.hostname != None and args.username != None and args.password != None:
            connect_ftp(args.hostname[0], args.username[0], args.password[0])
        
        #If user has entered data for schedule
        if args.schedule != None and len(args.schedule) == 2:
            download_file(args.schedule[0], args.schedule[1])

        elif args.schedule != None and len(args.schedule) == 0:
            current_date_time = str(datetime.now())
            current_date_time = current_date_time[:10]

            download_file_default(current_date_time)
            


if __name__ == "__main__":
    main()