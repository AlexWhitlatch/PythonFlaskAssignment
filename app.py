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
		
class Course(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	courseName = db.Column(db.String(80), unique=True)
	department = db.Column(db.String(80), unique=True)
	creditHours = db.Column(db.Integer, unique=True)
	sections = db.relationship('Section', backref = 'course', lazy = 'dynamic')
	
	def __init__(self, courseName, department, creditHours):
		self.courseName = courseName
		self.department = department
		self.creditHours = creditHours


class Section(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	sectionNumber = db.Column(db.Integer, unique=True)
	professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'))
	course_id = db.Column(db.Integer, db.ForeignKey('course.id'))

	def __init__(self, sectionNumber, professor_id, course_id):
		self.sectionNumber = sectionNumber
		self.professor_id = professor_id
		self.course_id = course_id
	
	
	
@app.route('/professors')
def professors():
	professor = Professor.query.all()
	return render_template('add_professor.html', professor = professor)
	
@app.route('/post_professor', methods = ['POST'])
def post_professor():
	professor = Professor(request.form['username'], request.form['email'])
	db.session.add(professor)
	db.session.commit()
	return redirect(url_for('professors'))
	

@app.route('/courses')
def courses():
	course = Course.query.all()
	return render_template('add_course.html', course = course)
	
@app.route('/post_course', methods = ['POST'])
def post_course():
	course = Course(request.form['courseName'], request.form['department'],request.form['creditHours'])
	db.session.add(course)
	db.session.commit()
	return redirect(url_for('courses'))
	
	
@app.route('/sections')
def sections():
	section = Section.query.all()
	course = Course.query.all()
	professor = Professor.query.all()
	return render_template('add_section.html', section = section, course = course, professor = professor)
	
@app.route('/post_section', methods = ['POST'])
def post_section():
	section = Section(request.form['sectionNumber'], request.form['professor_id'], request.form['course_id'])
	db.session.add(section)
	db.session.commit()
	return redirect(url_for('sections'))	
	
if __name__ == "__main__":
	app.run()