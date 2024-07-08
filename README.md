Backend Setup Guide
This guide will walk you through setting up the backend for your Django application.

Prerequisites
Python 3.x installed on your system (Download Python)
Basic understanding of command-line interface (CLI) usage
Setup Instructions
1. Clone the Repository
Clone the repository from your version control system (e.g., GitHub, GitLab):

bash
Copy code
git clone <repository-url>
cd <repository-name>
2. Set Up Virtual Environment
Create a virtual environment for isolating project dependencies:

bash
Copy code
python -m venv env
Activate the virtual environment. On Windows:

bash
Copy code
env\Scripts\activate
On macOS/Linux:

bash
Copy code
source env/bin/activate
3. Install Dependencies
Install the required packages and libraries defined in requirements.txt:

bash
Copy code
pip install -r requirements.txt
4. Migrate Database Models
Apply database migrations to set up the database schema:

bash
Copy code
python manage.py migrate
5. Configure MongoDB Access
MongoDB Setup: Ensure your MongoDB instance allows connections from your Django application.
Go to your MongoDB Atlas dashboard or local MongoDB instance.
Navigate to the "Network Access" tab.
Add your current IP address to the whitelist to allow connections from your development environment.
6. Run the Development Server
Start the Django development server:

bash
Copy code
python manage.py runserver
The server will start running locally at http://127.0.0.1:8000/.

7. Access the API
Open a web browser and go to http://127.0.0.1:8000/ to access your Django application's API endpoints.

Additional Notes
Creating Superuser: If you need an admin account to access the Django admin interface, create one using python manage.py createsuperuser and follow the prompts.
Settings: Modify settings.py in the project folder to adjust Django settings such as database configurations, static files, and more.
