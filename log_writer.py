from datetime import datetime

def write_to_log(event):
    dateTimeObj = datetime.now()
    f = open("resources/log_history.txt", "a")
    f.write("\n" + str(dateTimeObj) + " - " + event)
    f.close()

# write_to_log("Test log file")
