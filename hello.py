from flask import Flask,render_template,session,redirect,url_for,flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired,Email,Regexp,ValidationError


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config["CACHE_TYPE"] = 'null'
bootstrap = Bootstrap(app)
#moment = Moment(app)

@app.route('/',methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')
        if (old_name is not None) and (old_name != form.name.data):
            flash('Looks like you have changed your name!')
        if (old_email is not None) and (old_email != form.email.data):
            flash('Looks like you have changed your email!')
        session['name'] = form.name.data
        session['email'] = form.email.data
        session['UofTEmail'] = "utoronto" in form.email.data
        return redirect(url_for('index'))
    return render_template('index.html',form=form,name=session.get('name'),email=session.get('email'),UofTEmail=session.get('UofTEmail'))

def EmailCheck(form,field):
    email_address = field.data
    if ('@' not in email_address):
        raise ValidationError(f"Please include an '@' in the email address.'{email_address}' is missing an '@'")

class NameForm(FlaskForm):
    name = StringField("What is your name?",validators=[DataRequired()])
    email = StringField("What is your UofT Email address?",validators=[DataRequired(),EmailCheck])
    submit = SubmitField('Submit')





    # return render_template("user.html",current_time=datetime.utcnow())

# @app.route('/user/<name>')
# def user(name):
#     return '<h1>Hello, {}!</h1>'.format(name)
