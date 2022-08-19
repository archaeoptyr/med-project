import argparse
from asyncio import subprocess
import pickle
from ftplib import FTP
import os
from datetime import datetime
from subprocess import Popen
import sys
from main import windows_file_download

ftp = None

def connect_ftp(hostname, username, password, cron):
    try:
        global ftp
        
        #Creates a socket to connect to FTP server
        ftp = FTP(hostname)
        ftp.login(username, password)

        print("Connected")

        if not cron:
            keep_conn(args)
    
    except:
    
        print("Unable to connect")
        quit()

def rm_conn():
    #if pickle object exists
    if os.path.isfile("ftp_conn.obj"):
        #delete pickle file
        os.remove("ftp_conn.obj")

def keep_conn(cred):
    #creates pickle file to store ftp creds
    file_conn = open('ftp_conn.obj', 'wb')
    pickle.dump(cred, file_conn)
    

def conn_exists(cron):
    #Checks if the pickle file exists 
    if os.path.isfile("ftp_conn.obj"):
        
        if os.path.getsize("ftp_conn.obj") > 0:     
            open_conn = open("ftp_conn.obj", 'rb') 
            conn = pickle.load(open_conn)
            
            #Connects to FTP using creds from pickle
            connect_ftp(conn.hostname[0], conn.username[0], conn.password[0], cron)
            #Stores creds for next time
            keep_conn(conn)
            
            return True

    #If file does not exist
    return False

def format_datetime(date, time):
    #formats date and time
    date_time = date + " " + time
    date_time = datetime.strptime(date_time, "%d-%m-%Y %H:%M:%S")
    return date_time

def format_date(date):
    #Only formats the date
    format_date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y%m%d")
    return format_date

def download_file(date, time):
    try:
        
        #reformats date and time to match csv files
        date_time = format_datetime(date, time)
        date_time = date_time.strftime("%Y%m%d%H%M%S")
        
        file_list = list_files()
        file_needed = "MED_DATA_" + date_time[:-2]
       
        for name in file_list:
            #if the file in the server matches today's date
            if file_needed in name:  

                #Downloads File    
                with open(name, "wb") as f:
                    ftp.retrbinary("RETR " + str(name), f.write)
        
                    print("Successfully downloaded " + name)

    except AttributeError:
        print("There is no such file")


def download_file_default(date_now):
    try:
        #downloads files from the current day if specific date is not specified
        date = format_date(date_now)
        file_list = list_files()
        file_needed = "MED_DATA_" + date
        exists = False
        for name in file_list:
            #if the file in the server matches today's date
            if file_needed in name:  
                with open(name, "wb") as f:
                    ftp.retrbinary("RETR " + name, f.write)
                    exists = True
                    print("Successfully downloaded " + name)
    
    except AttributeError:
        print("There is no file with the current date")


def list_files():
    #returns an array of files in the server
    list_of_files = ftp.nlst()
   
    return list_of_files

def os_check(filename):
    platform = sys.platform
    # Checks users operating system and calls methods depending on said OS
    if platform == "win32":
        subprocess.call(["python", "main.py"])


def mac_osx(date, time):
    date_time = format_datetime(date, time)

    #Applescript to create a cron
    create_cron = ('''tell application "Terminal"
                    if not (exists window 1) then reopen
                    activate
                    tell application "System Events" to keystroke "crontab -r"
                    tell application "System Events" to keystroke return
                    tell application "System Events" to keystroke "crontab -e"
                    tell application "System Events" to keystroke return
                    tell application "System Events" to keystroke "i"
                    tell application "System Events" to keystroke "{minute} {hour} {day} {month} * cd /Users/arangill/Desktop/med-project/FTP && /usr/bin/python3 schedule.py"
                    tell application "System Events" to keystroke (key code 53)
                    tell application "System Events" to keystroke ";" using shift down
                    tell application "System Events" to keystroke "wq"
                    tell application "System Events" to keystroke return
                    delay 10
                    quit
                    end tell'''.format(minute = date_time.strftime("%M"),
                                        hour = date_time.strftime("%H"),
                                        day = date_time.strftime("%d"),
                                        month = date_time.strftime("%m")))

    #execute the applescript
    p = Popen(['osascript', '-e', create_cron])

    


def main():
        global args
        #Description of the CLI
        parser = argparse.ArgumentParser(description="A CLI FTP Client")

        #Specify the hostname of the server
        parser.add_argument("-hn", "--hostname", 
                            type = str, 
                            nargs = 1,  
                            metavar = "hostname", 
                            help = "Hostname of FTP server")

        #Specify the username to access server
        parser.add_argument("-u", "--username", 
                            type = str, 
                            nargs = 1,  
                            metavar = "username", 
                            help = "Username to connect to FTP")

        #Specify the password to access server
        parser.add_argument("-p", "--password", 
                            type = str, 
                            nargs = 1,  
                            metavar = "password", 
                            help = "Password to connect to FTP")

        #Schedule a download for a specific date and time
        parser.add_argument("-s", "--schedule", 
                            type = str, 
                            nargs = "*",  
                            metavar = "date", 
                            help = "Specify the date and time to download the file as DD-MM-YYYY HH:MM:SS")
        
        #Download the specified file
        parser.add_argument("-d", "--download", 
                            type = str, 
                            nargs = "*",  
                            metavar = "date", 
                            help = "Specify the date and time of the file you wish to download")
        
        #Disconnect from the server (i.e. delete credentials) 
        parser.add_argument("-dc", "--disconnect", 
                            type = str, 
                            nargs = '*',  
                            metavar = "disconnect", 
                            help = "Disconnect from FTP server")
         

        args = parser.parse_args()
        
        try:
            if args.disconnect != None:
                rm_conn()
                print("Disconnected")

            #Checks if pickle exists from previous session
            if conn_exists(False):
                pass

            #If user is starting a new session
            if args.hostname != None and args.username != None and args.password != None:
                connect_ftp(args.hostname[0], args.username[0], args.password[0], False)
            
            #If user has entered data for schedule
            if args.download != None and len(args.download) == 2:
                download_file(args.download[0], args.download[1])
            
            if args.schedule != None and len(args.schedule) == 0:
                current_date_time = str(datetime.now())
                current_date_time = current_date_time[:10]

                download_file_default(current_date_time)
            
            if args.schedule != None and len(args.schedule) == 2:
                mac_osx(args.schedule[0], args.schedule[1])

            if args.schedule != None and len(args.schedule) == 1:
                os_check(args.schedule[0])
            
        
        except AttributeError:
            print("Please specify your credentials")
        

if __name__ == "__main__":
    main()