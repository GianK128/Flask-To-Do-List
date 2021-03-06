from flask import Blueprint, redirect, url_for, request, flash
from flask.templating import render_template
from flask_login.utils import login_required
from werkzeug.utils import secure_filename
from todo_list import db, app
from todo_list.forms import CreateListForm, DeleteListForm, AddItemForm, EditItemForm, ProfilePicForm
from todo_list.models import User, List, Item, ActivityLog
from flask_login import current_user
from PIL import Image
import os

list = Blueprint('list', __name__)

@list.route('<user>')
def my_lists(user):
    form = DeleteListForm()
    picform = ProfilePicForm()
    _user = User.query.filter_by(username=user).first()
    return render_template('lists.html', user=_user, lists=_user.lists, form=form, picform=picform)

@list.route('<user>/<listname>')
def user_list(user, listname):
    form = AddItemForm()
    edit_form = EditItemForm()
    _user = User.query.filter_by(username=user).first()
    _list = List.query.filter_by(name=listname, user_id=_user.id).first()
    item_list = Item.query.filter_by(list_id=_list.id).all()
    return render_template('list_items.html', user=user, list=_list, items=item_list, form=form, edit_form=edit_form)

@list.route('list/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateListForm()
    if form.validate_on_submit():
        new_list = List(
            name = form.name.data,
            user_id = current_user.id
        )
        db.session.add(new_list)
        db.session.commit()

        new_log = ActivityLog(
            type = 4,
            list_id = new_list.id
        )
        db.session.add(new_log)
        db.session.commit()

        current_user.activities.append(new_log)
        db.session.commit()
        return redirect(url_for('list.user_list', user=current_user.username, listname=new_list.name))
    return render_template('lists_create.html', form=form)

@list.route('list/add-item', methods = ['POST'])
@login_required
def add_item():
    form = AddItemForm()
    if form.validate_on_submit():
        new_item = Item(
            content = form.content.data,
            list_id = form.list_id.data
        )
        db.session.add(new_item)

        list_log = ActivityLog.query.filter(ActivityLog.type == 2).filter(ActivityLog.list_id == form.list_id.data).all()
        for log in list_log:
            db.session.delete(log)

        _list = List.query.get(form.list_id.data)
        if _list.completed:
            _list.completed = False

        db.session.commit()
        listname = List.query.filter_by(id=form.list_id.data).first().name
        return redirect(url_for('list.user_list', user=current_user.username, listname=listname))
    else:
        flash("La longitud de la nota debe ser de al menos 2 car??cteres.", category='danger')
        return redirect(url_for('list.user_list', user=current_user.username, listname=List.query.get(form.list_id.data).name))

@list.route('list/edit-item', methods=['POST'])
@login_required
def complete_item():
    form = EditItemForm()
    if form.validate_on_submit():
        # Alternar entre completado o no
        _item = Item.query.filter_by(id=form.id.data).first()
        if _item.list_id != int(form.list_id.data):
            return '<h1>WTF LISTA INCORRECTA</h1>'
        _item.completed = not _item.completed
        db.session.commit()

        # Agregar o quitar log de actividad
        if _item.completed:
            new_log = ActivityLog(
                type = 1,
                item_id = _item.id,
                list_id = int(form.list_id.data)
            )
            db.session.add(new_log)
            current_user.activities.append(new_log)
        else:
            _log = ActivityLog.query.filter_by(item_id = _item.id).first()
            if _item.list.completed:
                _list_log = ActivityLog.query.filter_by(list_id = _item.list.id).first()
                db.session.delete(_list_log)
            db.session.delete(_log)
        db.session.commit()

        # Completar lista si est??n completados todos los items
        completed = True
        if _item.list.items:
            for item in _item.list.items:
                if not item.completed:
                    completed = False
                    break
        else:
            completed = False
        _item.list.completed = completed
        db.session.commit()

        # Agregar log si la lista est?? completa
        if completed:
            new_log = ActivityLog(
                type = 2,
                list_id = _item.list.id
            )
            db.session.add(new_log)
            current_user.activities.append(new_log)
        else:
            _log = ActivityLog.query.filter_by(list_id = _item.list.id).first()
            if _log:
                db.session.delete(_log)
        db.session.commit()

        listname = List.query.filter_by(id=form.list_id.data).first().name
        return redirect(url_for('list.user_list', user=current_user.username, listname=listname))
    else:
        return '<h1>WTF NO VALIDO</h1>'

@list.route('list/erase-item', methods=['POST'])
@login_required
def delete_item():
    form = EditItemForm()
    if form.validate_on_submit():
        _item = Item.query.filter_by(id=form.id.data).first()
        _logs = ActivityLog.query.filter_by(item_id=_item.id)

        if _item.list_id != int(form.list_id.data): 
            return '<h1>WTF LISTA INCORRECTA</h1>'

        db.session.delete(_item)
        for log in _logs:
            db.session.delete(log)

        db.session.commit()
        listname = List.query.filter_by(id=form.list_id.data).first().name
        return redirect(url_for('list.user_list', user=current_user.username, listname=listname))
    else:
        return '<h1>WTF NO VALIDO</h1>'

@list.route('list/delete', methods=['GET', 'POST'])
@login_required
def delete():
    list = request.args.get('list')
    form = DeleteListForm()
    if form.validate_on_submit():
        _list = List.query.get(list)
        _logs = ActivityLog.query.filter_by(list_id=_list.id)
        db.session.delete(_list)
        for log in _logs:
            db.session.delete(log)
        db.session.commit()
    return redirect(url_for('list.my_lists', user=current_user.username))

# Helper para mejor lectura
def delete_img_if_exists_or_not_anon(absolute_path, image_path):
    if os.path.exists(absolute_path) and image_path != 'anon.jpg':
        os.remove(absolute_path)

@list.route('upload-image', methods=['GET','POST'])
@login_required
def upload_image():
    form = ProfilePicForm()
    if form.validate_on_submit():
        delete_img_if_exists_or_not_anon(
            absolute_path = os.path.join(
                app.config['UPLOAD_FOLDER'], 'profiles', current_user.pic_path
            ),
            image_path = current_user.pic_path
        )

        img = form.image.data
        with Image.open(img) as imagen:
            x1, y1, x2, y2 = form.region.data.split('-')
            y1 = 0
            y2 = imagen.height
            imagen = imagen.crop((int(x1), y1, int(x2), y2))
            imagen = imagen.resize(size = (600, 600))

            filename = secure_filename(img.filename)
            filename = filename.split('.')
            filename = [current_user.username, filename[-1]]
            filename = '.'.join(filename)

            imagen.save(os.path.join(
                app.config['UPLOAD_FOLDER'], 'profiles', filename
            ))
        current_user.pic_path = filename
        db.session.commit()
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg, category='danger')
    return redirect(url_for('list.my_lists', user=current_user.username))
