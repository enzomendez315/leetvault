## Prerequisites
Before running this project locally, ensure you have the following installed:

* Python 3.12 and pip (Python Package Manager)
* Node.js and npm (Node Package Manager)
* IDE or code editor (PyCharm, VS Code, etc.)

## Installation
### Backend Setup
1. Clone this repository.
2. Open the `backend` directory in your preferred IDE.
3. (Optional) Create and activate a virtual environment by running `python3.12 -m venv venv` and `source venv/bin/activate`. 
4. Install dependencies with `pip install -r requirements.txt`.
5. Create a .env file in the root directory (same level as the `backend` or `frontend` directories) with all the needed variables.
6. Run `uvicorn app.main:app --reload` to start the backend server.

### Frontend Setup
1. Navigate to the `frontend` directory in your terminal.
2. Run `npm install` to install the necessary dependencies.
3. Run `npm run dev` to start the React application.