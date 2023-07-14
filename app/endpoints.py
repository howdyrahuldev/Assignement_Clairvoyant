from flask import Blueprint, jsonify, request
from main import main_create_tenant, upload_model_to_s3, main_create_project_metadata, main_get_project_metadata

tenant_bp = Blueprint("tenant", __name__, url_prefix="/tenant")
project_metadata_bp = Blueprint("project_metadata", __name__, url_prefix="/project_metadata")


@tenant_bp.route("/", methods=["POST"])
def create_tenant():
    # Retrieve the required data from the request
    data = request.json

    # Extract the relevant fields from the request data
    tenant_name = data.get("name")
    tenant_email = data.get("email")

    try:
        # Create Tenant Entry
        main_create_tenant(tenant_name=tenant_name, email=tenant_email)
        return jsonify({"status": "Successfully created tenant entry"})
    except:
        return jsonify({"status": "Tenant record couldn't be created"})


@project_metadata_bp.route("/", methods=["POST"])
def create_project_metadata():
    # Retrieve the required data from the request
    data = request.json
    # Extract the relevant fields from the request data
    tenant_id = data.get("tenant_id")
    try:
        upload_model_to_s3()
        main_create_project_metadata(tenant=tenant_id)
        return jsonify({"status": "Successfully created project metadata entry and uploaded to S3 bucket"})
    except:
        return jsonify({"status": "Project metadata record couldn't be created"})


@project_metadata_bp.route("/<project_metadata_id>", methods=["GET"])
def get_project_metadata(project_metadata_id):
    # Fetch project metadata from main
    project_metadata = main_get_project_metadata(project_metadata_id)

    if not project_metadata:
        return jsonify({"error": "Project metadata not found"})

    # Return the project metadata record as JSON response
    return jsonify({
        "id": project_metadata.project_metadata_id,
        "tenant_id": project_metadata.tenant,
        "csv_file": project_metadata.csv_file,
        "s3_location": project_metadata.s3_location,
        "evaluation_results": project_metadata.evaluation_results
    })
