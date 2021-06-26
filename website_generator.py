# import regex and datetime
import re
from datetime import datetime, timedelta
import sys
from app import app
# Open the log file
path=app.config["UPLOAD_FOLDER"]
filename=sys.argv[1]
filepath=path+"filename"
textfile = open(filepath, 'r')

firstLine = textfile.readline()
if re.match(r"Time Log:", firstLine):
    # Empty list for storing regex output
    time = []
    row_matches = []
    reg = re.compile(
        "\d{1,2}[:]\d{2}\w{2}\s{0,1}[-]\s{0,1}\d{1,2}[:]\d{2}\w{2}")    # Regex for capturing time with pattern 4:03pm - 6:57pm
    reg2 = re.compile("\d{1,2}[:]\d{2}\w{2}")                           # Regex for capturing start time and end time with pattern 4:03pm/am

    for i, line in enumerate(textfile,start=2):
        if (reg.findall(line)):
            row_matches = reg.findall(line)
            for li in row_matches:
                a = reg2.findall(li)
                a2 = datetime.strptime(a[0], '%I:%M%p').strftime('%H:%M:%S')
                a3 = datetime.strptime(a[1], '%I:%M%p').strftime('%H:%M:%S')
                max2 = datetime.strptime("11:59pm", '%I:%M%p').strftime('%H:%M:%S')
                if (a2 > a3):  # if hours in start-time >  hours in end-time
                    delta1 = datetime.strptime(max2, '%H:%M:%S') - datetime.strptime(a2, '%H:%M:%S')
                    delta = ((delta1 + datetime.strptime(a3, '%H:%M:%S')).strftime('%H:%M:%S'))
                    delta = datetime.strptime(delta, '%H:%M:%S')
                    time_change = timedelta(minutes=1)
                    delta = ((delta + time_change).strftime('%H:%M:%S'))
                    delta = datetime.strptime(delta, '%H:%M:%S')
                    exact = delta - datetime(1900, 1, 1)
                    delta = int(exact.total_seconds())
                    time.append(delta)
                    print("Start-time: " + a2, "| End-time: " + a3, "| Time spent: " + str(exact))
                elif (a3 > a2):  # if hours in start-time < hours in end-time
                    delta = datetime.strptime(a3, '%H:%M:%S') - datetime.strptime(a2, '%H:%M:%S')
                    time.append(int(delta.total_seconds()))
                    print("Start-time: " + a2, "| End-time: " + a3, "| Time spent: " + str(delta))
                else:  # if hours in start-time ==  hours in end-time
                    print("Start and End Times are same, so no work happened")
        else:
            print('{}=Time not found'.format(i, line.strip()))

    print("_________________________________________________________________________________________")
    print("Total Time spent: " + str(timedelta(seconds=sum(time))))
    textfile.close()
else:
    print("File is not as expected")
