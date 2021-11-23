from flask import Blueprint, render_template, request, flash, jsonify, session, url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from .models import Note, Contact, Task
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
        phone_number = request.form.get('pnumber')
        file = request.files['avatar']

      
        if len(first_name) < 1:
            flash('Name is too short!', category='error')
        elif len(last_name) < 1:
            flash('Surname is too short!', category='error')
        elif len(phone_number) < 1:
            flash('Phone number is too short!', category='error')
        else:
            new_contact = Contact(name=first_name, sname=last_name, pnumber=phone_number, t_color=rancolor, user_id=current_user.id)
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
