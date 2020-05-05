from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class SubscriptionForm(FlaskForm):
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
