from datetime import datetime

dateTimeObj = datetime.now()


def write_to_log(event):
    f = open("resources/log_history.txt", "a")
    f.write("\n" + str(dateTimeObj) + " - " + event)
    f.close()

# write_to_log("Test log file")
