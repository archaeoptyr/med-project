#test functions taking the same user input as the real things,
#with a way to throw exceptions to test the GUI's functionality
"""
def connect_ftp(hostname, username, password):

    try:
        assert hostname == "localhost"
        assert username == "user"
        assert password == "password"
        print("logged in")
        
    except:
        print("shit's bonked")

"""
from genericpath import isfile
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
        
    except:
        print("Unable to connect")


def download_file(date, time):
    #reformats date and time to match csv files
    final = date + " " + time
    final = datetime.datetime.strptime(final, "%d-%m-%Y %H:%M:%S").strftime("%Y%m%d%H%M%S")
    filename = "MED_DATA_" + final + ".csv"

    #Downloads File    
    with open(filename, "wb") as f:
        ftp.retrbinary("RETR " + filename, f.write)
        print("Successfully downloaded " + filename)

def download_file_today(datestring):
    #reformat datestring
    #tests
    print("wheeeeee")
    
