import sys
from ftplib import FTP
import time
import subprocess
import os
from datetime import datetime

# Sets dir_path to current directory
dir_path = os.path.dirname(os.path.realpath(__file__))
ftp = ""
hostname = input("Enter Hostname: ")
username = input("Enter Username: ")
password = input("Enter Password: ")


def connect_ftp(hostname, username, password):
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


def date_time():
    print("-Enter date and time of CSV file in the format: YYYY-MM-DD HH:MM:SS")

    # Formats user input into datetime
    date = str(input("\n" + username + "@" + hostname + "> "))
    date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d%H%M%S")

    # sets variable to name of CSV file from user input
    filename_with_date = "MED_DATA_" + date + ".csv"

    return filename_with_date


def windows_file_download(filename):
    filename_param = filename
    print(
        "-Enter <time>(12hr) <AM/PM> <day> <month> for the scheduled download")
    schedule_command = input("\n" + username + "@" + hostname + "> ")

    try:
        time_param = schedule_command.split()[0]
        AMPM_param = schedule_command.split()[1]
        day_param = schedule_command.split()[2]
        month_param = schedule_command.split()[3]

        # Creates a subprocess which runs a powershell.exe and calls a script that creates a task Schedular for the scheduled_Download.py
        p = subprocess.Popen([
            "powershell.exe",
            "$Action = (New-ScheduledTaskAction -Execute 'powershell.exe' "
            "-Argument 'python " + dir_path + "\scheduled_Download.py " + hostname + " " + username + " " +
            password + " " + filename_param + "')\n "
            "$Trigger = New-ScheduledTaskTrigger -Once -At \"" + month_param.strip() + "/" + day_param.strip() + "/" + "2022" + " " + time_param.strip() + " " + AMPM_param.strip() + "\"\n"
            "Register-ScheduledTask -TaskName \"Scheduled CSV Download " + day_param + month_param + "\" -Trigger $Trigger -Action $Action -RunLevel Highest –Force"],
                             stdout=sys.stdout)
        p.communicate()

    except:
        print("Error")


def run_commands():
    # List of commands available
    print("\nAvailable commands:\n\n-ls\n-set_download\n-exit")

    while True:
        command = input("\n" + username + "@" + hostname + "> ")

        try:
            if command == "set_download":
                filename_param = date_time()
                windows_file_download(filename_param)

            elif command == "ls":
                list_files()

            elif command == "exit":
                ftp.quit()
                print("Server disconnected")
                print()
                break

        except:
            print("Please provide a command")


connect_ftp(hostname, username, password)
run_commands()
