import sys
from ftplib import FTP
import time
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
ftp = ""

# Automatically signs into FTP server
hostname = str(sys.argv[1])
username = str(sys.argv[2])
password = str(sys.argv[3])


def connect_ftp():
    try:
        global ftp

        # Creates a socket to connect to FTP server
        ftp = FTP(hostname)
        ftp.login(username, password)

        print("Connected to: " + hostname)

    except:
        print("Unable to connect")
        print("\nClosing in 5 seconds")
        time.sleep(5)
        quit()


def download_file(filename):

    # Downloads CSV File
    with open(dir_path + "\\" + filename, "wb") as f:
        ftp.retrbinary("RETR " + filename, f.write)


def main():
    connect_ftp()
    download_file(str(sys.argv[4]))


main()
