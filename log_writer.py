from datetime import datetime


# write to log_history.txt
def write_to_log(event):
    dateTimeObj = datetime.now()
    f = open("resources/log_history.txt", "a")
    f.write("\n" + str(dateTimeObj) + " - " + event)
    f.close()

# write_to_log("Test log file")
