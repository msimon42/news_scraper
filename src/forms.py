from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class SubscriptionForm(FlaskForm):
    email = StringField('Email',
                            validators=[DataRequired(), Email()])

    links = StringField('Links',
                                validators=[DataRequired()])

    submit = SubmitField('Subscribe')
