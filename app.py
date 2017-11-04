from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/schoolschedule'
app.debug = True
db = SQLAlchemy(app)

class Professor(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(120), unique=True)
	sections = db.relationship('Section', backref = 'professor', lazy = 'dynamic')
	
	def __init__(self, username, email):
		self.username = username
		self.email = email
		
	def __repr__(self):
		return '<Professor %r>' % self.username

class Section(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	sectionNumber = db.Column(db.Integer, unique=True)
	professer_id = db.Column(db.Integer, db.ForeignKey('professor.id'))
	course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
	
class Course(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	courseName = db.Column(db.String(80), unique=True)
	department = db.Column(db.String(80), unique=True)
	creditHours = db.Column(db.Integer, unique=True)
	sections = db.relationship('Section', backref = 'course', lazy = 'dynamic')
	
	
	
@app.route('/')
def index():
	return render_template('add_user.html')
	
@app.route('/post_user', methods = ['POST'])
def post_user():
	user = User(request.form['username'], request.form['email'])
	db.session.add(user)
	db.session.commit()
	return redirect(url_for('index'))
	
if __name__ == "__main__":
	app.run()