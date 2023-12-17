# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///persons.db'
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Person {self.name}>'

@app.route('/add_person', methods=['GET', 'POST'])
def add_person():
    if request.method == 'POST':
        name = request.form['name']
        new_person = Person(name=name)
        db.session.add(new_person)
        db.session.commit()
        return redirect(url_for('list_persons'))
    return render_template('add_person.html')

@app.route('/')
@app.route('/list_persons')
def list_persons():
    persons = Person.query.all()
    return render_template('index.html', persons=persons)

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
