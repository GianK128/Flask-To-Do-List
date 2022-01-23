from flask import Blueprint, flash, redirect, url_for
from flask.templating import render_template
from flask_login.utils import login_required
import sqlalchemy
from todo_list import db
from todo_list.forms import CreateListForm, DeleteListForm, AddItemForm, EditItemForm
from todo_list.models import User, List, Item, ActivityLog
from flask_login import current_user

list = Blueprint('list', __name__)

@list.route('<user>')
def my_lists(user):
    form = DeleteListForm()
    _user = User.query.filter_by(username=user).first()
    user_lists = List.query.filter_by(user_id=_user.id).all()
    return render_template('lists.html', user=_user.username, lists=user_lists, form=form)

@list.route('<user>/<listname>')
def user_list(user, listname):
    form = AddItemForm()
    edit_form = EditItemForm()
    _list = List.query.filter_by(name=listname).first()
    item_list = Item.query.filter_by(list_id=_list.id).all()
    return render_template('list_items.html', user=user, list=_list, items=item_list, form=form, edit_form=edit_form)

@list.route('create', methods=['GET', 'POST'])
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

@list.route('add-item', methods = ['POST'])
def add_item():
    form = AddItemForm()
    if form.validate_on_submit():
        new_item = Item(
            content = form.content.data,
            list_id = form.list_id.data
        )
        db.session.add(new_item)
        db.session.commit()
        listname = List.query.filter_by(id=form.list_id.data).first().name
        return redirect(url_for('list.user_list', user=current_user.username, listname=listname))
    else:
        return '<h1>WTF</h1>'

@list.route('complete-item', methods=['POST'])
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
                item_id = _item.id
            )
            db.session.add(new_log)
            current_user.activities.append(new_log)
        else:
            _log = ActivityLog.query.filter_by(item_id = _item.id).first()
            db.session.delete(_log)
        db.session.commit()

        # Completar lista si están completados todos los items
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

        # Agregar log si la lista está completa
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

@list.route('delete-item', methods=['POST'])
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

@list.route('delete/<list>', methods=['GET', 'POST'])
@login_required
def delete(list):
    form = DeleteListForm()
    if form.validate_on_submit():
        _list = List.query.get(list)
        _logs = ActivityLog.query.filter_by(list_id=_list.id)
        db.session.delete(_list)
        for log in _logs:
            db.session.delete(log)
        db.session.commit()
    return redirect(url_for('list.my_lists', user=current_user.username))
