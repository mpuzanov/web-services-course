from flask import Flask, request, jsonify, redirect, url_for, abort, render_template, send_file
import pandas as pd
import numpy as np
import sklearn.externals
import joblib
import os

app = Flask(__name__)

knn = joblib.load('knn.pkl')

@app.route('/')
def hello_world():
    # print('hi')
    return '<h1>Hello, my very best friend!</h1>'


@app.route('/user/<username>')
def show_user_profile(username):    
    return f'User {username}'


@app.route('/avg/<nums>')
def avg(nums):
    nums = nums.split(',')
    nums = [float(num) for num in nums]
    nums_mean = float(sum(nums)) / max(len(nums),1)
    print(nums_mean)
    return str(nums_mean)


@app.route('/iris/<param>')
def iris(param):
    param = param.split(',')
    param = [float(num) for num in param]
    print(param)

    param = np.array(param).reshape(1, -1)
    predict = knn.predict(param)

    return str(predict)

@app.route('/show_image')
def show_image():
    return '<img src="/static/setosa.jpg" alt="setosa">'

@app.route('/badrequest400')
def bad_request():
    return abort(400)

@app.route('/iris_post', methods=['POST'])
def add_message():

    try:
        content = request.get_json()

        param = content['flower'].split(',')
        param = [float(num) for num in param]
    
        param = np.array(param).reshape(1, -1)
        predict = knn.predict(param)

        predict = {'class':str(predict[0])}
    except:
        return redirect(url_for('bad_request'))    

    return jsonify(predict)

from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    file = FileField()


@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = form.name.data + '.csv'
        # f.save(os.path.join(filename))

        df = pd.read_csv(f, header=None)
        # print(df.head())
        predict = knn.predict(df)
        # print(predict)
        result = pd.DataFrame(predict)
        result.to_csv(filename, index=False)

        return send_file(filename,
            mimetype='text/csv',
            attachment_filename=filename,
            as_attachment=True)

    return render_template('submit.html', form=form)

from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'json', 'csv'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename + '_uploaded')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'file uploaded'
            
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
# рабочий код для тестирования через Postman
@app.route('/upload2', methods=['POST'])
def upload_file2():
    
    print(str(request.files))
    file = request.files['']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    def calculation(x,y):
        print('Horoshiy Den '+str(x+y))
    calculation(1,8)

    with open(filename) as f:
        data = json.load(f)
    print(data)

    json_out_filename = 'Test_Out.json'
    with open(json_out_filename, 'w') as json_file:
        json.dump(data, json_file)

    return send_file(json_out_filename, 
        mimetype='text/csv/json', 
        attachment_filename=json_out_filename, 
        as_attachment=True)
