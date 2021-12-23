from flask import Blueprint, render_template, request, flash, jsonify, session, url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from .models import ContactEmail, Note, Contact, Task, PhoneNumber, ContactEmail, Iqtest
from . import db
import json
import os
import secrets
from werkzeug.utils import secure_filename



# from flask_wtf.file import FileField 
views = Blueprint('views', __name__)


AVATAR_FOLDER = 'static/images/avatars/'

# ---Avatar upload---


UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join('static/images/avatars', picture_fn)
    form_picture.save(picture_path)
    return picture_fn


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


  

# --- Home page
@views.route('/')
def home():

    return render_template("home.html", user=current_user)



# --- show Notes and new note
@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    # count_row = session.query(Note).count()
    
    if request.method == 'POST':
        from random import choice
        rancolor = choice(["color1", "color2", "color3", "color4", "color5", "color6",\
             "color7", "color8", "color9", "color10", "color11", "color12"])

        title = request.form.get('title')
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, title=title, color=rancolor, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("note.html", user=current_user)


@views.route('/note-edit', methods = ['GET', 'POST'])
def note_update():
 
    if request.method == 'POST':
        my_data = Note.query.get(request.form.get('note_id'))
 
        my_data.title = request.form['title']
        my_data.data = request.form['note_data']

        db.session.commit()
        flash("Note Updated Successfully")
 
    return redirect(url_for('views.notes'))


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


# --- show contact and New Contact
@views.route('/contacts', methods=['GET', 'POST'])
@login_required
def contacts():

    # my_data = Contact.query.get(request.form.get('contact_id'))
    # avatar = my_data.avatar
    # image_file = url_for('static', filename='images/avatars/' + avatar)

    if request.method == 'POST':

        from random import choice
        list_color = ["blue", "red", "green", "orange", "cyan", "pink", "cardinal", 
                      "dark green", "magenta", "purple", "dark magenta", "fawn", "flame"]
        rancolor = choice(list_color) 

        first_name = request.form.get('name')
        last_name = request.form.get('sname')
        address = request.form.get('address')
        website = request.form.get('website')
        telegram = request.form.get('telegram')

        PhoneList = request.form.getlist('addphone[]')
        EmailList = request.form.getlist('addemail[]')
        file = request.files['avatar']

        # contact.phone_numbers | map(attribute='number') | list

      
        if len(first_name) < 1:
            flash('Name is too short!', category='error')
        elif len(last_name) < 1:
            flash('Surname is too short!', category='error')
        else:
            phone_numbers = list(map(lambda number: PhoneNumber(number=number), PhoneList))
            contact_email = list(map(lambda email: ContactEmail(email=email), EmailList))
            
            new_contact = Contact(name=first_name.capitalize(), sname=last_name.capitalize(), phone_numbers=phone_numbers, \
             contact_email=contact_email, address=address.capitalize(), siteurl=website, telegram=telegram, t_color=rancolor, user_id=current_user.id)
           
            db.session.add(new_contact)
            db.session.commit()

            # # Avatar upload
            # if 'avatar' not in request.files:
            #     flash(f"No file part {request.files}" )
            #     return redirect(request.url)
            # file = request.files['avatar']
            # # If the user does not select a file, the browser submits an
            # # empty file without a filename.
            # if file.filename == '':
            #     flash('No selected file')
            #     return redirect(request.url)
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join('website/static/images/avatars/', filename))
                
                # flash("Contact Updated Successfully")

                return redirect(url_for('views.contacts', name=filename))


            flash('Contact added!', category='success')

    return render_template("contact.html", user=current_user)


# --- Edit contact 
@views.route('/contact-edit', methods = ['GET', 'POST'])
def contact_update():
 
    if request.method == 'POST':

        my_data = Contact.query.get(request.form.get('contact_id'))
        
        file = request.files['avatar']
        my_data.name = request.form.get('name')
        my_data.sname = request.form.get('sname')
        my_data.pnumber = request.form.get('pnumber')
        my_data.avatar = file.filename

        # for contact in current_user.contacts:
        #     contact.

        db.session.commit()
        

        # Avatar upload
        # check if the post request has the file part
        if 'avatar' not in request.files:
            flash(f"No file part {request.files}" )
            return redirect(request.url)
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join('website/static/images/avatars/', filename))
            
            flash("Contact Updated Successfully")

            return redirect(url_for('views.contacts', name=filename))

    return redirect(url_for('views.contacts'))

# -- delete Contact
@views.route('/delete-contact', methods=['POST'])
def delete_contact():
    contact = json.loads(request.data)
    contactId = contact['contactId']
    contact = Contact.query.get(contactId)
    if contact:
        if contact.user_id == current_user.id:
            db.session.delete(contact)
            db.session.commit()

    return jsonify({})


# --- show todo and new todo
@views.route('/todo', methods=['GET', 'POST'])
@login_required
def todo():

    if request.method == 'POST':
        title = request.form.get('title')
        task = request.form.get('task')
        status = request.form.get('status')
        due_date = request.form.get('date')
        due_time = request.form.get('time')        

        if len(title) < 1:
            flash('Task title is too short!', category='error')
        elif len(task) < 1:
            flash('Task description is too short', category='error') 
        else:
            new_task = Task(title=title, task=task, status=status, due_date=due_date, due_time=due_time, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash(f"\"{title}\" is successfully added!", category='success')

    return render_template("todo.html", user=current_user)


# --- Edit Task 
@views.route('/task-edit', methods = ['GET', 'POST'])
def todo_update():
 
    if request.method == 'POST':
        my_data = Task.query.get(request.form.get('task_id'))

        my_data.title = request.form.get('title')
        my_data.task = request.form.get('task')
        my_data.status = request.form.get('status')
        my_data.due_date = request.form.get('due_date')
        my_data.due_time = request.form.get('due_time')
        
        db.session.commit()
        flash(f"\"{my_data.title}\" Updated Successfully")

    return redirect(url_for('views.todo'))


# -- delete Task
@views.route('/delete-task', methods=['POST'])
def delete_task():
    task = json.loads(request.data)
    taskId = task['taskid']
    task = Task.query.get(taskId)
    if task:
        if task.user_id == current_user.id:
            db.session.delete(task)
            db.session.commit()

    return jsonify({})


@views.route('/iqtest', methods=['GET', 'POST'])
@login_required
def IQtest():

    QuestionList = IQtest.query.all()
    Question = IQtest.query.first()

    if request.method == 'POST':

        testid = request.form.get('testid')
        answer = request.form.get('answer')

    return render_template("iqtest.html", QuestionList=QuestionList, Question=Question, user=current_user)


# --- Edit Iq test
# @views.route('/iqtest-edit', methods = ['GET', 'POST'])
# def AddTest():
 
    # if request.method == 'POST':

#to change color of question buttons and disable 
def setStatus(qlist):
    qAttempt=[]
    strval=session['result'].strip()
    ans=strval.split(',')
    for i in range(int(len(ans)/2)):
        qAttempt.append(int(ans[2*i]))  
    
    for rw in qlist:
        if rw.qid in qAttempt:
            rw.bcol='green'   # set color
            rw.status='disabled' # disable


@views.route("/showQuest/<int:Qid>")
def showQuest(Qid):
    questList=IQtest.query.all()
    quest=IQtest.query.filter_by(qid=Qid).first()
    setStatus(questList)
    return render_template("dashboard.html", questList=questList, quest=quest)  


@views.route('/saveAns', methods=["POST"]) 
def saveAns():
    Qid=request.form.get('Qid')
    ans=request.form.get('answer')
    #update the question id and its selected answer in session variable result
    res=session['result']
    res= res+Qid+','+ans+','
    session['result']=res
    questList=IQtest.query.all()
    setStatus(questList)
    quest=IQtest.query.filter_by(id=Qid).first()
    return render_template("dashboard.html", questList=questList, quest=quest)  


@views.route("/logout")
def logout():
    #calculate result
    count=0
    txt=""
    strval=session['result'].strip()
    #split result string by ','
    ans=strval.split(',')
    for i in range(int(len(ans)/2)):
        qd=ans[2*i] # get question id
        qn=ans[2*i+1]  # get the sorresponding answer
        tt=int(qd)
        quest=IQtest.query.filter_by(qid=tt).first()
        actans=quest.answer
        if actans==int(qn):#compare correct answer in questions table with answer chosen by user
            count=count+1 # increment counter
    txt=txt+'You have '+ str(count)+ ' correct questions out of '+ str(int(len(ans)/2))+ ' questions ' # set the result statement
    return render_template("result.html",txt=txt) 