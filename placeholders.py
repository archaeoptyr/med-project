#test functions taking the same user input as the real things,
#with a way to throw exceptions to test the GUI's functionality
import argparse

def connect_ftp(hostname, username, password):

    try:
        assert hostname == "localhost"
        assert username == "user"
        assert password == "password"
        print("logged in")
        
    except:
        print("shit's bonked")

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


if __name__ == "__main__":
    main()
