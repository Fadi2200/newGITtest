from flask import Flask, redirect, url_for, render_template, request, flash
#from models import db, Contact
#from forms import ContactForm, myChoices
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Email, Length


myChoices = {"Bosch" : "Bosch", 
             "Strasse":"Strasse",
             "Not Found":"Not Found",
             "Schelter":"Schelter",
             "In active state":"In active state",
             "Levcon":"Levcon"}
            
            


class ContactForm(FlaskForm):
    barcode = StringField('Barcode', validators=[Length(min=5, max=80, message='You cannot have more than 200 characters')])
    kennzeichen = StringField('Kennzeichen', validators=[DataRequired(), Length(min=5, max=80, message='You cannot have more than 80 characters')])
    herkunft =SelectField(u'Herkunft', choices =myChoices, validators=[Length(min=-1, max=200, message='You cannot have more than 100 characters')])

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my secret'
app.config['DEBUG'] = False

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route("/")
def index():
    '''
    Home page
    '''
    return redirect(url_for('contacts'))


@app.route("/new_contact", methods=('GET', 'POST'))
def new_contact():
    '''
    Create new contact
    '''
    form = ContactForm()
    if form.validate_on_submit():
        my_contact = Contact()
        form.populate_obj(my_contact)
        my_contact.herkunftpython  = dict(myChoices).get(form.herkunft.data)
        db.session.add(my_contact)
        try:
            db.session.commit()
            # User info
            flash('Motor created correctly', 'success')
            return redirect(url_for('contacts'))
        except:
            db.session.rollback()
            flash('Error generating contact.', 'danger')

    return render_template('web/new_contact.html', form=form)

def getApp():   
    return app
@app.route("/edit_contact/<id>", methods=('GET', 'POST'))
def edit_contact(id):
    '''
    Edit contact

    :param id: Id from contact
    '''
    my_contact = Contact.query.filter_by(id=id).first()
    form = ContactForm(obj=my_contact)
    if form.validate_on_submit():
        try:
            # Update contact
            form.populate_obj(my_contact)
            db.session.add(my_contact)
            db.session.commit()
            # User info
            flash('Saved successfully', 'success')
        except:
            db.session.rollback()
            flash('Error update Motors system.', 'danger')
    return render_template(
        'web/edit_contact.html',
        form=form)

@app.route("/contacts")
def contacts():
    '''
    Show alls contacts
    '''
    contacts = Contact.query.order_by(Contact.barcode).all()
    return render_template('web/contacts.html', contacts=contacts)


@app.route("/search")
def search():
    '''
    Search
    '''
    name_search = request.args.get('name')
    all_contacts = Contact.query.filter(Contact.barcode.contains(name_search)).all()
    return render_template('web/contacts.html', contacts=all_contacts)


@app.route("/contacts/delete", methods=('POST',))
def contacts_delete():
    '''
    Delete contact
    '''
    try:
        mi_contacto = Contact.query.filter_by(id=request.form['id']).first()
        db.session.delete(mi_contacto)
        db.session.commit()
        flash('Delete successfully.', 'danger')
    except:
        db.session.rollback()
        flash('Error delete  motor.', 'danger')

    return redirect(url_for('contacts'))



class Contact(db.Model):


    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(80), nullable=True)
    #surname = db.Column(db.String(100), nullable=True)
    #email = db.Column(db.String(200), nullable=True, unique=False)
    #phone = db.Column(db.String(20), nullable=True, unique=False)
    kennzeichen= db.Column(db.String(200), nullable=False)
    herkunft= db.Column(db.String(200), nullable=False)
    barcode= db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Contacts %r>' % self.barcode

if __name__ == "__main__":
    app.run(host="0.0.0.0")
