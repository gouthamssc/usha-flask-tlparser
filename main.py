import os
from app import app
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

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
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File successfully uploaded')
        return render_template('upload.html', filename=filename)
    else:
        flash('Allowed file types are -> txt')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == "__main__":
    app.run()