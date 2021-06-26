import os
from app import app
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import subprocess
import re
from datetime import datetime, timedelta
import sys

ALLOWED_EXTENSIONS = set(['txt'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No file selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # file.save("C:\Users\0008EI744\Desktop\\usha-flask-tlparser\\"+filename)
        # print(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File successfully uploaded')
        parser(filename)
        return render_template('upload.html', filename=filename)
    else:
        flash('Allowed file types are -> txt')
        return redirect(request.url)

# def output_result():
#     path=app.config['UPLOAD_FOLDER']+"output.txt"
#     cmd = "python3 website_generator.py " +ali +" >>"+path
#     subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

# @app.route('/print')
# def printMsg():
#     output=output_result()
#     return output
        
@app.route('/display/output')
def display_image():
    return redirect(url_for('static', filename='uploads/' + "output.txt"), code=301)


def parser(filename):
    path=app.config["UPLOAD_FOLDER"]
    filepath=path+filename
    dest=path+"output.txt"
    sys.stdout = open(dest, 'w')
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
                        # f.write(str(value))
                        # print >>f, value
                    elif (a3 > a2):  # if hours in start-time < hours in end-time
                        delta = datetime.strptime(a3, '%H:%M:%S') - datetime.strptime(a2, '%H:%M:%S')
                        time.append(int(delta.total_seconds()))
                        print("Start-time: " + a2, "| End-time: " + a3, "| Time spent: " + str(delta))
                        # print >>f, value
                        # f.write(str(value))
                    else:  # if hours in start-time ==  hours in end-time
                        print("Start and End Times are same, so no work happened")
            else:
                print('{}=Time not found'.format(i, line.strip()))
                # f.write(str(value))
                # print >>f, value

        print("_________________________________________________________________________________________")
        print("Total Time spent: " + str(timedelta(seconds=sum(time))))
        # f.write(str(value))
        # print >>f, value
        textfile.close()
    else:
        print("File is not as expected")
    sys.stdout.close()


if __name__ == "__main__":
    app.run()