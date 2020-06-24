# django-pizza

<p align="left">
    <img src="https://flat.badgen.net/dependabot/thepracticaldev/dev.to?icon=dependabot" alt="Dependabot Badge" />
    <img src="https://badgen.net/pypi/v/pip" alt="PIP version">
    <img src="https://badgen.net/github/license/micromatch/micromatch" alt="LICENSE">
</p>


Simplified e-commerce Pizza Ordering platform "Django-Pizza".

## Local Setup

Clone the repository, and locate into the project's root directory:

```bash
git clone https://github.com/EvgeniiKlepilin/django-pizza.git
cd django-pizza
```

### Environment Setup

Create a `.env` file and configure it to your needs. A template is available in `.env.example`, and can be used with provided default values.

```bash
cp .env.example .env
```

Proceed to install dependencies required to run this project. You can do it by installing them globally on your machine or by creating a Python Virtual Environment. Virtual Environment is a recommended way as it keeps dependencies for separate projects separately, thus avoiding conflicts between them. Once you setup it up, activate it with `source` command.

```bash
python3 -m venv env
source env/bin/activate
```

Install Python packages using provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Database Setup

You can use your local PostgreSQL database setup for this project or use provided Docker setup.

### Docker Setup

Create a `docker-compose.yml` file and configure it to your needs. A template is available in `docker-compose.yml.example`, and can be used with provided default values.

## Startup

Make sure your DB is up and running. In case you are using provided Docker setup, run `docker-compose up` or `docker-compose up -d` in case you don't need the logging output to your console.

Set up the database first by running migrations:

```bash
python manage.py migrate
```

Then, start up the server by running `python manage.py runserver`. If you encounter an error, make sure that you have activated Python Virtual Environment in your console and installed all the required packages.

In case of a successful start up you should see following in your console:

```bash
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
June 10, 2020 - 09:11:45
Django version 3.0.7, using settings 'socialnetwork.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

You server should be available at http://127.0.0.1:8000/ .