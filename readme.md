# Hacker News Clone (FastAPI + PostgreSQL)

This is a simple Hacker News clone built with FastAPI and PostgreSQL. The purpose of this project is to educate users on how to deploy database-dependent applications on Leapcell.

## Features

- FastAPI backend
- PostgreSQL database integration
- Jinja2 templating for rendering views

## Project Structure

```
.
├── LICENSE               # License file
├── main.py               # Main application entry point
├── models.py             # Database models using SQLAlchemy
├── requirements.txt      # Project dependencies
└── templates/            # HTML templates for rendering views
    ├── index.html        # Homepage displaying the list of posts
    └── post_detail.html  # Template for displaying post details
```

## Deployment on Leapcell

This guide will walk you through setting up and deploying the project on Leapcell.

### Prerequisites

Ensure you have the following:

- A Leapcell account
- PostgreSQL database instance
- Python installed (recommended: Python 3.8+)

### Environment Variables

This project requires a PostgreSQL connection string, which should be set using the following environment variable:

```bash
DATABASE_DSN=<your_postgresql_connection_string>
```

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/leapcell/fastapi-hackernews-clone
   cd fastapi-hackernews-clone
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Running Locally

To start the project locally, ensure your PostgreSQL instance is running and execute:

```bash
uvicorn main:app --reload
```

The application will be accessible at `http://localhost:8000`.

### Deploying on Leapcell

1. Push your code to a GitHub repository.
2. Log in to Leapcell and connect your repository.
3. Configure the `DATABASE_DSN` environment variable in the Leapcell deployment settings.
4. Deploy your application.

Once deployed, your application will be accessible via the Leapcell-generated domain.

## Contributing

Feel free to submit issues or pull requests to improve this project.

## Contact

For support, reach out via the Leapcell Discord community or email support@leapcell.io.
