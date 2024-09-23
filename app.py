from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        description = request.form['description']
        new_event = Event(title=title, date=date, description=description)
        db.session.add(new_event)
        db.session.commit()
        flash('Event created successfully!')
        return redirect(url_for('events'))
    return render_template('create_event.html')

@app.route('/events')
def events():
    all_events = Event.query.all()
    return render_template('events.html', events=all_events)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database within an application context
    app.run(debug=True)
