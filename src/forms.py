from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email

class SubscriptionForm(FlaskForm):
    email = StringField('Email',
                            validators=[DataRequired(), Email()])

    links = StringField('Links',
                                validators=[DataRequired()])

    submit = SubmitField('Subscribe')

class DashboardForm(FlaskForm):
    email = StringField('Email',
                            validators=[DataRequired(), Email()])

    links = StringField('Links',
                                validators=[DataRequired()])

    filters = StringField('Filters',
                                    validators=[DataRequired()]
    )
    user_token = HiddenField()
    update = SubmitField('Update')
