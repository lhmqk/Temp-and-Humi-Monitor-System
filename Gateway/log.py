from datetime import datetime

def writelog(data):
    LOGFILE = open("log.txt", "a")
    LOGLINE = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ": " + data + "\n"
    LOGFILE.write(LOGLINE)
    LOGFILE.close()