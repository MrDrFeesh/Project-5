# Project Name

## Overview

This project is a web application that allows users to create, share, and vote on builds. Users can sign up, log in, and manage their builds. The application tracks the priority of each build and the number of votes each user has cast.

## Prerequisites

- Python 3.x
- Node.js and npm (or yarn)
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-CORS
- React

## Backend Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/your-repo/project-name.git
    cd project-name/backend
    ```

2. **Create a virtual environment:**

    ```sh
    pipenv shell
    ```

3. **Install backend dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the database:**

    ```sh
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

5. **Run the backend server:**

    ```sh
    flask run
    ```

## Frontend Setup

1. **Navigate to the frontend directory:**

    ```sh
    cd ../frontend
    ```

2. **Install frontend dependencies:**

    ```sh
    npm install
    # or
    yarn install
    ```

3. **Start the frontend development server:**

    ```sh
    npm start
    # or
    yarn start
    ```

## Usage

1. **Access the application:**

    Open your web browser and navigate to `http://localhost:3000`.

2. **Sign up and log in:**

    Create a new account or log in with an existing account.

3. **Create and manage builds:**

    Create new builds, edit existing builds, and delete builds.

4. **Vote on builds:**

    Use the up and down arrow buttons to vote on builds. The priority of each build and the number of votes cast by each user will be tracked.

## Project Structure

- `backend/`: Contains the Flask backend code.
- `frontend/`: Contains the React frontend code.
- `models.py`: Defines the database models.
- `app.py`: Contains the Flask application and routes.
- `UserContext.js`: Provides user context for the frontend.
- `BuildShowcase.js`: Displays the builds and handles voting.
- `ProfilePage.js`: Displays the user's profile and their builds.

## Contributing

1. **Fork the repository:**

    Click the "Fork" button at the top right of the repository page.

2. **Clone your fork:**

    ```sh
    git clone https://github.com/your-username/project-name.git
    cd project-name
    ```

3. **Create a new branch:**

    ```sh
    git checkout -b feature-branch
    ```

4. **Make your changes and commit them:**

    ```sh
    git add .
    git commit -m "Description of your changes"
    ```

5. **Push your changes to your fork:**

    ```sh
    git push origin feature-branch
    ```

6. **Create a pull request:**

    Open your fork on GitHub and click the "New pull request" button.