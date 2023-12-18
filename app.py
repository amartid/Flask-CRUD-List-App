from flask import Flask, render_template, request, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask import render_template, request
from forms import AddPersonForm 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///persons.db'
app.config['SECRET_KEY'] = os.urandom(24)  # Generates a random 24-byte (192-bit) secret key
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Person {self.name}>'

# class AddPersonForm(FlaskForm):
#     name = StringField('Name', validators=[DataRequired()])
#     submit = SubmitField('Add Person')
    
@app.route('/add_person', methods=['GET', 'POST'])
def add_person():
    form = AddPersonForm()

    if form.validate_on_submit():
        name = form.name.data
        new_person = Person(name=name)
        db.session.add(new_person)
        db.session.commit()
        return redirect(url_for('list_persons'))
    return render_template('add_person.html', form=form)

# @app.route('/list_persons')
# def list_persons():
#     persons = Person.query.all()
#     return render_template('index.html', persons=persons)


# @app.route('/list_persons', methods=['GET'])
# def list_persons():
#     page = request.args.get('page', 1, type=int)
#     per_page = 5  
#     persons = Person.query.paginate(page=page, per_page=per_page, error_out=False)

#     return render_template('index.html', persons=persons)
@app.route('/')
@app.route('/list_persons', methods=['GET'])
def list_persons():
    search_query = request.args.get('search', '')

    page = request.args.get('page', 1, type=int)
    per_page = 5 
    persons = Person.query.filter(Person.name.ilike(f'%{search_query}%')).paginate(page=page, per_page=per_page, error_out=False)
    return render_template('index.html', persons=persons, search_query=search_query)

@app.route('/edit_person/<int:id>', methods=['GET', 'POST'])
def edit_person(id):
    person = Person.query.get(id)
    if request.method == 'POST':
        person.name = request.form['name']
        db.session.commit()
        return redirect(url_for('list_persons'))
    return render_template('edit_person.html', person=person)

@app.route('/delete_person/<int:id>')
def delete_person(id):
    person = Person.query.get(id)
    db.session.delete(person)
    db.session.commit()
    return redirect(url_for('list_persons'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
