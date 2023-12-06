from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import (DateField, DecimalField, HiddenField, StringField,
                     SubmitField, TextAreaField)
from wtforms.validators import DataRequired, Length


class AddActualForm(FlaskForm):
    kpi_goal_id = HiddenField("MyHiddenField")
    kpi_actual_date = DateField(
        'Date', validators=[DataRequired()], default=datetime.today)
    kpi_aa1 = DecimalField('Possible Value')
    kpi_actual_value = DecimalField(
        'Actual Value', validators=[DataRequired()])
    kpi_actual_comment = TextAreaField('Comment')
    submit = SubmitField('Add Actual')


class EditForm(FlaskForm):
    KPI_ACTUAL_ID = HiddenField("MyHiddenField", validators=[DataRequired()])
    KPI_ACTUAL_DATE = DateField('Date', validators=[DataRequired()])
    KPI_AA1 = DecimalField('Possible Value')
    KPI_ACTUAL_VALUE = DecimalField(
        'Actual Value', validators=[DataRequired()])
    KPI_ACTUAL_COMMENT = StringField('Comment', validators=[Length(max=200)])
    submit = SubmitField('Submit Changes')
