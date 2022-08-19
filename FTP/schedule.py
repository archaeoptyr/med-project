from ftp import conn_exists, download_file
from datetime import datetime

#gets current date and time
date_time = datetime.now()

#format the date and time
date = date_time.strftime("%d-%m-%Y")
time = date_time.strftime("%H:%M:%S")

#if there is still a connection to the server
if(conn_exists(True)):
    #download the file with the current date and time
    download_file(date, time)



