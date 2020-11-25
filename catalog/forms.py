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

    
    
