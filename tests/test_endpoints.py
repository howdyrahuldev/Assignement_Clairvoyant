import unittest
import json
from app.app import app, db, Tenant, ProjectMetadata


class EndpointsTestCase(unittest.TestCase):
    def setUp(self):
        # Configure the Flask application for testing
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "mongodb://localhost:27017/domongo"
        self.app = app.test_client()

        # Create the database tables
        db.create_all()

    def tearDown(self):
        # Clean up the database after testing
        db.session.remove()
        db.drop_all()

    def test_create_tenant(self):
        # Test the create_tenant endpoint

        # Prepare the request data
        data = {
            "name": "Rahuldev Sarkar",
            "email": "rahuldev@test.com"
        }

        # Send a POST request to create a tenant
        response = self.app.post("/tenant/", data=json.dumps(data), content_type="application/json")

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Parse the response JSON data
        response_data = json.loads(response.data)

        # Assert the expected keys in the response data
        self.assertIn("tenant", response_data)
        self.assertIn("name", response_data)
        self.assertIn("email", response_data)

        # Assert the tenant was created correctly
        tenant = Tenant.query.first()
        self.assertEqual(response_data["tenant"], tenant.tenant)
        self.assertEqual(response_data["name"], tenant.name)
        self.assertEqual(response_data["email"], tenant.email)

    def test_create_project_metadata(self):
        # Test the create_project_metadata endpoint

        # Prepare the request data
        data = {
            "tenant_id": 1,
            "csv_file": "data.csv",
            "s3_location": "http://s3-us-east-1.amazonaws.com/tenant_model_bucket/1-model.pkl",
            "evaluation_results": 3.6
        }

        # Send a POST request to create project metadata
        response = self.app.post("/project_metadata/", data=json.dumps(data), content_type="application/json")

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Parse the response JSON data
        response_data = json.loads(response.data)

        # Assert the expected keys in the response data
        self.assertIn("project_metadata_id", response_data)
        self.assertIn("tenant", response_data)
        self.assertIn("csv_file", response_data)
        self.assertIn("s3_location", response_data)
        self.assertIn("evaluation_results", response_data)

        # Assert the project metadata was created correctly
        project_metadata = ProjectMetadata.query.first()
        self.assertEqual(response_data["project_metadata_id"], project_metadata.project_metadata_id)
        self.assertEqual(response_data["tenant"], project_metadata.tenant)
        self.assertEqual(response_data["csv_file"], project_metadata.csv_file)
        self.assertEqual(response_data["s3_location"], project_metadata.s3_location)
        self.assertEqual(response_data["evaluation_results"], project_metadata.evaluation_results)

    def test_get_project_metadata(self):
        # Test the get_project_metadata endpoint

        # Create a sample project metadata record
        project_metadata = ProjectMetadata(tenant_id=1, csv_file="data.csv", s3_location="http://s3-us-east-1.amazonaws.com/tenant_model_bucket/1-model.pkl", evaluation_results=3.6)
        db.session.add(project_metadata)
        db.session.commit()

        # Send a GET request to retrieve the project metadata
        response = self.app.get(f"/project_metadata/{project_metadata.project_metadata_id}")

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

        # Parse the response JSON data
        response_data = json.loads(response.data)

        # Assert the expected keys in the response data
        self.assertIn("project_metadata_id", response_data)
        self.assertIn("tenant", response_data)
        self.assertIn("csv_file", response_data)
        self.assertIn("s3_location", response_data)
        self.assertIn("evaluation_results", response_data)

        # Assert the retrieved project metadata matches the sample record
        self.assertEqual(response_data["project_metadata_id"], project_metadata.project_metadata_id)
        self.assertEqual(response_data["tenant"], project_metadata.tenant)
        self.assertEqual(response_data["csv_file"], project_metadata.csv_file)
        self.assertEqual(response_data["s3_location"], project_metadata.s3_location)
        self.assertEqual(response_data["evaluation_results"], project_metadata.evaluation_results)


if __name__ == "__main__":
    unittest.main()
