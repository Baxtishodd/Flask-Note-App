from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from .models import Note, Contact
from . import db
import json
import os
views = Blueprint('views', __name__)


AVATAR_FOLDER = 'static/images/avatars/'


# --- Home
@views.route('/')
def home():

    return render_template("home.html", user=current_user)



# --- Notes
@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
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


# @views.route('/note_update', methods=['GET', 'POST'])
# @login_required
# def update(id):
    
#     if request.method == 'POST':
#         my_data = Note.query.get(request.form.get('id'))
        
#         my_data.data = request.form['note_data']

#         db.session.commit()
#         flash("Note has successfully updated!")

#         return render_template("note.html", user=current_user)


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


# --- New Contact
@views.route('/contacts', methods=['GET', 'POST'])
@login_required
def contacts():
    if request.method == 'POST':

        from random import choice
        list_color = ["blue", "red", "green", "orange", "cyan", "pink", "cardinal", 
                      "dark green", "magenta", "purple", "dark magenta", "fawn", "flame"]
        rancolor = choice(list_color) 

        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone_number = request.form.get('phone_number')
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
