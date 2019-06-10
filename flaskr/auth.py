import functools
from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

import pickle

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
	if request.method=='POST':
		username = request.form['username']
		password = request.form['password']
		db = get_db()
		error = None
		
		if not username:
			error = 'usernamme required'
		elif not password:
			error = 'password is required'
		elif db.execute(
			'select id from user where username=?',(username,)
			).fetchone() is not None:
			error = 'User {} is already registered'.format(username)
		if error is None:
			db.execute(
				'INSERT INTO user (username, password) VALUES (?, ?)', 
				(username, generate_password_hash(password))
				)
			db.commit()
			return redirect(url_for('auth.login'))
		flash(error)
	return render_template('auth/register.html')
	#return render_template(url_for('auth.register'))


@bp.route('/login', methods=('GET', 'POST'))
def login():
	if request.method=='POST':
		username = request.form['username']
		password = request.form['password']
		error = None 
		db = get_db()

		if username is not None:
			print('login')
			user = db.execute(
				'SELECT * FROM user WHERE username=?',
				(username,)
				).fetchone()

			if user is None:
				error = 'user not registered'
			elif not check_password_hash(user['password'], password):
				error = 'credentials incorrect'
			
			if error is None:
				session.clear()
				session['user_id']=user['id']
				#print('login')
				#model = pickle.load(open('G:/work/python/flask/flaskr/static/modell.pkl','rb'))
				#session['model'] = model
				return redirect(url_for('weather.index'))
				#return render_template('weather/home.html')
				#return redirect(url_for('index'))
				#return redirect(url_for('weather.index'))
				#return render_template('auth/register.html')
		else:
			error = 'credentials incorrect'	
		
		flash(error)
	return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')

	if user_id is None:
		g.user = None
	else:
		g.user = get_db().execute(
			'SELECT * FROM user WHERE id=?',
			(user_id,)
			).fetchone()


@bp.route('/logout', methods=('GET', 'POST'))
def logout():
	session.clear()
	return redirect(url_for('index'))


def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			redirect(url_for('auth.login'))
		return view(**kwargs)

	return wrapped_view