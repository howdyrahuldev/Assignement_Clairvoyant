# main.py
import os
import boto3
import pandas as pd
import pickle
from app.ml_component import generate_model
from app.app import db, Tenant, ProjectMetadata

# Read CSV file and target column from environment variables
csv_file = os.getenv('CSV_FILE')
target_column = os.getenv('TARGET_COLUMN')

# Read aws_access_key_id and aws_secret_access_key from environment variables
aws_access_key_id = os.getenv('AWS_ACCESS_KEY')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# Process CSV and generate the model using the ML component
data = pd.read_csv(csv_file)
model, evaluation_results = generate_model(data, target_column)


def main_create_tenant(tenant_name, email):
    # Create a tenant entry
    tenant = Tenant(name=tenant_name, email=email)
    db.session.add(tenant)
    db.session.commit()


def upload_model_to_s3():
    # Save the model as a pickle file locally
    model_file = "model.pkl"
    with open(model_file, "wb") as file:
        pickle.dump(model, file)

    # Upload the model to S3
    s3 = boto3.client("s3", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    s3.upload_file(model_file, "tenant_model_bucket", model_file)


def main_create_project_metadata(tenant):
    # Save metadata to MongoDB
    metadata = ProjectMetadata(
        tenant=tenant,
        csv_file=csv_file,
        s3_location=f"http://s3-us-east-1.amazonaws.com/tenant_model_bucket/{tenant}-model.pkl",
        evaluation_results=evaluation_results
    )
    db.session.add(metadata)
    db.session.commit()


def main_get_project_metadata(project_metadata_id):
    # Fetch the project metadata record from the database
    project_metadata = ProjectMetadata.query.get(project_metadata_id)
    return project_metadata
