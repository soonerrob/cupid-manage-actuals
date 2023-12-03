import os
from datetime import datetime

import dotenv
from flask import Flask, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap5
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import case
from sqlalchemy.sql import func
from wtforms import (DateField, DecimalField, HiddenField, StringField,
                     SubmitField, TextAreaField)
from wtforms.validators import DataRequired

from models import KpiActual, KpiGoal, KpiMaster, db

dotenv.load_dotenv()
app = Flask(__name__) 
CORS(app)
app.secret_key = os.getenv("APP_SECRET_KEY")
Bootstrap5(app)


# Raw ODBC connection string
odbc_connection_string = (
    "DRIVER=" + os.getenv("ODBC_CONNECTION_DRIVER") + ";"
    "SERVER=" + os.getenv("ODBC_CONNECTION_SERVER") + ";"
    "DATABASE=" + os.getenv("ODBC_CONNECTION_DATABASE") + ";"
    "UID=" + os.getenv("ODBC_CONNECTION_UID") + ";"
    "PWD=" + os.getenv("ODBC_CONNECTION_PWD")
)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pyodbc:///?odbc_connect={odbc_connection_string}'

db.init_app(app)


class KpiActualForm(FlaskForm):
    kpi_goal_id = HiddenField("MyHiddenField")
    kpi_actual_date = DateField('Date', validators=[DataRequired()], default=datetime.today)
    kpi_aa1 = DecimalField('Possible Value')
    kpi_actual_value = DecimalField('Actual Value', validators=[DataRequired()])
    kpi_actual_comment = TextAreaField('Comment')    
    submit = SubmitField('Submit')


@app.route("/")
def home():
    
    return render_template("index.html")


@app.route("/filter_table")
def filter_table():
    selected_goal_id = request.args.get('goal_id')

    if selected_goal_id:
        filtered_data = KpiActual.query.filter_by(KPI_GOAL_ID=selected_goal_id).all()
    else:
        filtered_data = []

    return render_template("table_data.html", goal_details=filtered_data)


@app.route("/manage_actuals", methods=['GET', 'POST'])
def manage_actuals():
    form = KpiActualForm()
    if form.validate_on_submit():
        try:
            # Format the date as MM/DD/YYYY
            formatted_date = form.kpi_actual_date.data.strftime('%m/%d/%Y')

            # Create a new KpiActual object and populate it with form data
            new_actual = KpiActual(
                KPI_GOAL_ID=form.kpi_goal_id.data,
                KPI_ACTUAL_DATE=formatted_date,
                KPI_ACTUAL_VALUE=form.kpi_actual_value.data,
                KPI_ACTUAL_COMMENT=form.kpi_actual_comment.data,
                KPI_AA1=form.kpi_aa1.data
            )
            # Add new_actual to the database
            db.session.add(new_actual)
            db.session.commit()

        except Exception as e:
            # Catch any exceptions
            print("Error:", e)
            return "An error occurred while processing the form."

        return redirect(url_for('manage_actuals'))
    
    
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
    return render_template("manage_actuals.html", goal_details=goal_details, form=form)
        

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)    
    