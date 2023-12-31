import os
from datetime import datetime

import dotenv
from dateutil import parser
from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from flask_bootstrap import Bootstrap5
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import case
from sqlalchemy.sql import func
from wtforms import (DateField, DecimalField, HiddenField, StringField,
                     SubmitField, TextAreaField)
from wtforms.validators import DataRequired, Length

from config import (BOOTSTRAP_BTN_STYLE, DEBUG, ODBC_CONNECTION_STRING,
                    SECRET_KEY)

from .forms import AddActualForm, EditForm
from .models import KpiActual, KpiGoal, KpiMaster, db

dotenv.load_dotenv()
app = Flask(__name__)
app.config['DEBUG'] = DEBUG
app.secret_key = SECRET_KEY
app.config['BOOTSTRAP_BTN_STYLE'] = BOOTSTRAP_BTN_STYLE
app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pyodbc:///?odbc_connect={ODBC_CONNECTION_STRING}'


CORS(app)
Bootstrap5(app)
db.init_app(app)


@app.route("/")
def home():

    return render_template("index.html", active_page="home")


@app.route("/filter_table")
def filter_table():
    selected_goal_id = request.args.get('goal_id')

    if selected_goal_id:
        filtered_data = KpiActual.query.filter_by(
            KPI_GOAL_ID=selected_goal_id).all()
    else:
        filtered_data = []

    return render_template("table_data.html", goal_details=filtered_data)


@app.route("/modal_content/<int:actual_id>", methods=['GET', 'POST'])
def modal_content(actual_id):
    actual = db.get_or_404(KpiActual, actual_id)
    form = EditForm(obj=actual)
    if form.validate_on_submit():
        try:
            actual.KPI_ACTUAL_DATE = form.KPI_ACTUAL_DATE.data.strftime(
                '%m/%d/%Y')
            actual.KPI_AA1 = form.KPI_AA1.data
            actual.KPI_ACTUAL_VALUE = form.KPI_ACTUAL_VALUE.data
            actual.KPI_ACTUAL_COMMENT = form.KPI_ACTUAL_COMMENT.data

            db.session.commit()
            flash("Success: Actual Edited Successfully.")
        except Exception as e:
            print("Error:", e)
            return "An error occurred while processing the form."

        return render_template('table_row.html', actual=actual, row_id=actual.KPI_ACTUAL_ID)

    form.KPI_ACTUAL_DATE.data = parser.parse(actual.KPI_ACTUAL_DATE)

    return render_template("modal_content.html", actual=actual, form=form)


@app.route("/manage_actuals", methods=['GET', 'POST'])
def manage_actuals():
    form = AddActualForm()
    if form.validate_on_submit():
        try:
            # Format the date as MM/DD/YYYY
            formatted_date = form.kpi_actual_date.data.strftime('%m/%d/%Y')

            new_actual = KpiActual(
                KPI_GOAL_ID=form.kpi_goal_id.data,
                KPI_ACTUAL_DATE=formatted_date,
                KPI_ACTUAL_VALUE=form.kpi_actual_value.data,
                KPI_ACTUAL_COMMENT=form.kpi_actual_comment.data,
                KPI_AA1=form.kpi_aa1.data
            )
            db.session.add(new_actual)
            db.session.commit()
            flash("Success: New Actual Added.")
            added_actual = KpiActual.query.get(new_actual.KPI_ACTUAL_ID)

        except Exception as e:
            print("Error:", e)
            return "An error occurred while processing the form."

        return render_template('table_row.html', actual=added_actual, row_id=added_actual.KPI_ACTUAL_ID)

    current_month = datetime.now().month
    current_year = datetime.now().year
    current_quarter = (current_month - 1) // 3 + 1

    goal_details = db.session.query(
        KpiGoal.KPI_GOAL_ID,
        # pylint: disable=no-member
        func.concat(
            'FY', KpiGoal.KPI_GOAL_YEAR, ' - Q', KpiGoal.KPI_GOAL_QTR,
            ' - ', func.trim(KpiMaster.KPI_NAME),
            case(
                (KpiGoal.KPI_GOAL_NAME != '', ' - '),
                else_=''
            ),
            KpiGoal.KPI_GOAL_NAME,
            case(
                (KpiGoal.KPI_GOAL_DATE != '', ' - '),
                else_=''
            ),
            KpiGoal.KPI_GOAL_DATE
        ).label('GOAL_DETAILS')
    ).join(
        KpiMaster, KpiGoal.KPI_ID == KpiMaster.KPI_ID
    ).filter(
        KpiGoal.KPI_GOAL_QTR == current_quarter,
        KpiGoal.KPI_GOAL_YEAR == current_year
    ).order_by(
        KpiMaster.KPI_NAME, KpiGoal.KPI_GOAL_NAME
    ).all()
    return render_template("manage_actuals.html", goal_details=goal_details, form=form, active_page='manage_actuals')


@app.route('/delete', methods=['DELETE'])
def delete_actual():
    actual_id = request.args.get('id')
    actual_to_delete = db.get_or_404(KpiActual, actual_id)
    db.session.delete(actual_to_delete)
    db.session.commit()
    return '', 200
