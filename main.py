"""
Author: T. van Es
Date: 10-10-2022

Description:
This file contains the basic webapp that student designers use to upload and split designs.
"""

import os
import ast
from flask_wtf import FlaskForm
from flask import Flask, session, render_template, redirect, url_for, request
from wtforms import FileField, SubmitField, StringField, TextAreaField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
from flask_session.__init__ import Session
import splitter
import creator

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkeyhere'
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['SESSION_TYPE'] = 'filesystem'
app.config.from_object(__name__)
Session(app)

"""
The UploadFileForm is a template that represents the form that handles the files uploads.
"""

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    titleDesign = StringField("Title Design", validators=[InputRequired()],render_kw={'placeholder':'Titel ontwerp'})
    nameDesigner = StringField("Name Designer", validators=[InputRequired()], render_kw={'placeholder':'Naam ontwerper'})
    designDescription = TextAreaField("Design Description", render_kw={'placeholder':'Omschrijving ontwerp'})
    submit = SubmitField("Upload File")

"""
This Proof of Concept has a couple of pages. It uses both session data as well as URL paths to use data between pages.
The homepage is where the upload form is located. This saves the location and filled in information into session storage.
The split page is where you land after uploading the file. It fetches the highest group to show, and has a list to keep
track of the parent-children-tree.
SplitFurther is used for all extra splitting after the original one. These still keep track of parent-children-tree ranking.
addComments and addedComments are created to handle when the user enters additional information that has to be stored for
later usage.
Finalize is the end step which finalizes the proces by creating the required Storybook file templates.
"""

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        session['location'] = app.config['UPLOAD_FOLDER'] + '/' + secure_filename(file.filename)
        session['formdata'] = [form.titleDesign.data, form.nameDesigner.data, form.designDescription.data]
        return redirect(url_for('split'))
    return render_template('index.html', form=form)

@app.route('/split')
def split():
    location = session.get('location', None)
    formData = session.get('formdata', None)
    orderedList = splitter.getOrdered(os.path.join(os.path.abspath(os.path.dirname(__file__)),location))
    highestGroup = splitter.getHighestGroup(os.path.join(os.path.abspath(os.path.dirname(__file__)),location), orderedList)
    session['originalList'] = highestGroup['children']
    return render_template('split.html', list=highestGroup, formData=formData, level='highest')

@app.route('/splitFurther/', methods=["POST"])
def splitFurther():
    originalGroup = []
    children = request.args.get('children')
    current = request.args.get('current')
    originalList = session.get('originalList', None)
    for child in ast.literal_eval(children):
        if child not in originalList:
            originalList += ast.literal_eval(children)
    if ast.literal_eval(current) in originalList:
        originalList.remove(ast.literal_eval(current))
    session['originalList'] = originalList
    location = session.get('location', None)
    formData = session.get('formdata', None)
    orderedList = splitter.getOrdered(os.path.join(os.path.abspath(os.path.dirname(__file__)), location))
    if str(originalList) != children:
        originalGroup = splitter.getChildren(os.path.join(os.path.abspath(os.path.dirname(__file__)), location), str(originalList), orderedList)
    highestGroups = splitter.getChildren(os.path.join(os.path.abspath(os.path.dirname(__file__)), location), children, orderedList)
    return render_template('split.html', original=originalGroup, list=highestGroups, formData=formData, level='sub')

@app.route('/addComments/', methods=["POST"])
def addComments():
    location = session.get('location', None)
    formData = session.get('formdata', None)
    orderedList = splitter.getOrdered(os.path.join(os.path.abspath(os.path.dirname(__file__)), location))
    list = session.get('originalList', None)
    list = splitter.getChildren(os.path.join(os.path.abspath(os.path.dirname(__file__)), location), str(list), orderedList)
    session['activeList'] = list
    return render_template('comment.html', list=list, formData=formData)

@app.route('/addedComments/', methods=["POST"])
def addedComments():
    formData = session.get('formdata', None)
    list = session.get('activeList', None)
    try:
        extraInfo = request.form['extraInfo']
        itemID = request.form['itemID']
        list = splitter.updateExtraInfo(list, itemID, extraInfo)
    except:
        print('no updated extra info')
    session['activeList'] = list
    try:
        description = request.form['description']
        itemID = request.form['itemID']
        list = splitter.updateDescription(list, itemID, description)
    except:
        print('no updated description')
    return render_template('comment.html', list=list, formData=formData)

@app.route('/finalize/', methods=["POST"])
def finalize():
    list = session.get('activeList', None)
    for item in list:
        creator.createComponent(item)
        creator.createStory(item)
    return render_template('finalize.html', list=list)


if __name__ == '__main__':
    app.run(debug=True)
