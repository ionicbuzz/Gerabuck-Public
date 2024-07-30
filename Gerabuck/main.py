from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'hello'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class users(db.Model):
    _id         = db.Column('id', db.Integer, primary_key=True)
    name        = db.Column(db.String(100))
    email       = db.Column(db.String(100))
    pnumber     = db.Column(db.String(100))
    password    = db.Column(db.String(100))
    gender      = db.Column(db.String(100))
    dob         = db.Column(db.String(100))

    def __init__(self, name, email, pnumber, password, gender, dob):
        self.name     = name    
        self.email    = email   
        self.pnumber  = pnumber 
        self.password = password
        self.gender   = gender  
        self.dob      = dob     


@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/user', methods=['POST', 'GET'])
def user():
    if request.method == 'POST':
        name        = request.form['name']
        email       = request.form['email']
        pnumber     = request.form['phone']
        password    = request.form['password']
        gender      = request.form['gender']
        dob         = f"{request.form['dob-day']}/{request.form['dob-month']}/{request.form['dob-year']}"
        
        print(f'Name: {name}')
        print(f'Email: {email}')
        print(f'Phone: {pnumber}')
        print(f'Passw: {password}')
        print(f'Gender: {gender}')
        print(f'Date of Birth: {dob}')

        is_user_exist = users.query.filter_by(name=name).first()
        if not is_user_exist:
            db_user = users(name, email, pnumber, password, gender, dob)
            db.session.add(db_user)
            db.session.commit()

    return render_template('user.html')

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        id = request.form['id']
        users.query.filter_by(_id=id).delete()
        db.session.commit()
    return render_template('admin.html', values=users.query.all())

@app.route('/journey')
def journey():
    return render_template('journey.html')

@app.route('/subscription')
def subscription():
    return render_template('subscription.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)