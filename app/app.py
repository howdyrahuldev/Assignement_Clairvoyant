# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mongodb://localhost:27017/domongo"
db = SQLAlchemy(app)


class Tenant(db.Model):
    tenant = db.Column("TenantID", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column("Name", db.String(100))
    email = db.Column("EmailID", db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


class ProjectMetadata(db.Model):
    project_metadata_id = db.Column("ProjectID", db.Integer, primary_key=True, autoincrement=True)
    tenant = db.Column("TenantID", db.Integer)
    csv_file = db.Column("CSVLocation", db.String(500))
    s3_location = db.Column("S3Location", db.String(500))
    evaluation_results = db.Column("EvaluationResult", db.Float)

    def __init__(self, tenant, csv_file, s3_location, evaluation_results):
        self.tenant = tenant
        self.csv_file = csv_file
        self.s3_location = s3_location
        self.evaluation_results = evaluation_results


if __name__ == '__main__':
    db.create_all()
    app.run()

