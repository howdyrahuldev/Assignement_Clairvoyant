# Tenant Data Model

Creates a tenant data and saves the model for the same

## Table of Contents

- [Installation](#installation)
- [API Endpoints](#api-endpoints)


## Installation

Follow the below steps for installation:

```bash
# Clone the repository
git clone https://github.com/howdyrahuldev/Assignement_Clairvoyant

# Change to the project directory
cd Assignment_Clairvoyant

# Install the dependencies
pip install -r requirements.txt

# Change the permission of the run.sh file to executable
chmod +x run.sh

# Run the run.sh file to setup the application environement
./run.sh
```


## API Endpoints

List of the available API endpoints and their descriptions.

POST /tenant: Creates a new tenant.

POST /project_metadata: Creates a new project metadata record.

GET /project_metadata/{id}: Retrieve a project metadata record by ID.
