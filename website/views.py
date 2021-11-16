from flask import Blueprint, render_template, request, flash, jsonify, session, url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from .models import Note, Contact, Task
from . import db
import json
import os
views = Blueprint('views', __name__)


AVATAR_FOLDER = 'static/images/avatars/'


# --- Home
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
    if request.method == 'POST':

        from random import choice
        list_color = ["blue", "red", "green", "orange", "cyan", "pink", "cardinal", 
                      "dark green", "magenta", "purple", "dark magenta", "fawn", "flame"]
        rancolor = choice(list_color) 

        first_name = request.form.get('name')
        last_name = request.form.get('sname')
        phone_number = request.form.get('pnumber')
        avatar = request.form.get('avatar')

      
        if len(first_name) < 1:
            flash('Name is too short!', category='error')
        elif len(last_name) < 1:
            flash('Surname is too short!', category='error')
        elif len(phone_number) < 1:
            flash('Phone number is too short!', category='error')
        else:
            new_contact = Contact(name=first_name, sname=last_name, pnumber=phone_number,  t_color=rancolor, user_id=current_user.id) # avatar=avatar,
            db.session.add(new_contact)
            db.session.commit()

            # ppath = os.path.join(app.config['AVATAR_FOLDER'], avatar.filename)
            # avatar.save(AVATAR_FOLDER)

            flash('Contact added!', category='success')

    return render_template("contact.html", user=current_user)


# --- Edit contact 
@views.route('/contact-edit', methods = ['GET', 'POST'])
def contact_update():
 
    if request.method == 'POST':
        my_data = Contact.query.get(request.form.get('contact_id'))

        my_data.name = request.form.get('name')
        my_data.sname = request.form.get('sname')
        my_data.pnumber = request.form.get('pnumber')
        my_data.avatar = request.form.get('avatar')

        avatar = url_for('static', filename='images/avatars/' + request.form.get('avatar'))
        
        db.session.commit()
        flash("Contact Updated Successfully")
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
            flash('New Task is successfully added!', category='success')

    return render_template("todo.html", user=current_user)


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
