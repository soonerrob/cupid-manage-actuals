from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class KpiGoal(db.Model):
    __tablename__ = 'BONUS_KPI_GOALS'
    KPI_GOAL_ID = db.Column(db.Integer, primary_key=True)
    KPI_ID = db.Column(db.Integer, db.ForeignKey('BONUS_KPI_MASTER.KPI_ID'))
    KPI_GOAL_NAME = db.Column(db.String(255))
    KPI_GOAL_YEAR = db.Column(db.Integer)
    KPI_GOAL_QTR = db.Column(db.Integer)
    KPI_GOAL_DATE = db.Column(db.Integer)
    kpi_master = relationship("KpiMaster")

class KpiMaster(db.Model):
    __tablename__ = 'BONUS_KPI_MASTER'
    KPI_ID = db.Column(db.Integer, primary_key=True)
    KPI_NAME = db.Column(db.String(50))
    KPI_DESC = db.Column(db.String(100))
    KPI_DEPT = db.Column(db.Integer)
    KPI_WEIGHT = db.Column(db.Numeric(18, 2))
    KPI_TYPE = db.Column(db.Integer)
    KPI_ISCHILD = db.Column(db.Integer)
    KPI_PARENT = db.Column(db.Integer)
    KPI_ISPARENT = db.Column(db.Integer)
    KPI_LESSISBETTER = db.Column(db.Integer)
    KPI_CALC_TYPE = db.Column(db.Integer)
    KPI_AA1 = db.Column(db.String(50))
    KPI_AA2 = db.Column(db.String(50))
    KPI_AA3 = db.Column(db.String(50))
    KPI_AA4 = db.Column(db.String(50))
    KPI_AB1 = db.Column(db.Numeric(18, 2))
    KPI_AB2 = db.Column(db.Numeric(18, 2))
    KPI_AB3 = db.Column(db.Numeric(18, 2))
    KPI_AB4 = db.Column(db.Numeric(18, 2))
    KPI_ISDEFAULT = db.Column(db.Integer)

class KpiActual(db.Model):
    __tablename__ = 'BONUS_KPI_ACTUALS'
    KPI_ACTUAL_ID = db.Column(db.Integer, primary_key=True)
    KPI_GOAL_ID = db.Column(db.Integer, db.ForeignKey('BONUS_KPI_GOALS.KPI_GOAL_ID'))
    KPI_ACTUAL_VALUE = db.Column(db.Numeric(20, 4))
    KPI_ACTUAL_DATE = db.Column(db.String(10))
    KPI_ACTUAL_COMMENT = db.Column(db.String(200))
    KPI_AA1 = db.Column(db.Numeric(20, 4))
    kpi_goal = relationship("KpiGoal")
    