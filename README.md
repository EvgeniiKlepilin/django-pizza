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

### Admin Setup

To access Administration site part, you have to create at least one super user:

```bash
$ python manage.py createsuperuser
Username: superuser
Email address: superuser@djangopizza.com
Password: 
Password (again): 
Superuser created successfully.
```

### Delivery Setup

Checking out requires a setup of at least one default delivery method. To do that, proceed to http://127.0.0.1:8000/admin/ , login with an Admin account, go to *Orders->Delivery*, and create a Delivery object with a *cost* value, while omitting *country* value. This will create a *Generic Delivery* that can be used as a default for all orders.

## Deploying on Heroku

Make sure you have a [Heroku account](https://signup.heroku.com/signup/dc), and a [Postgres installed locally](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

Install Heroku CLI tool via `sudo snap install heroku --classic` if you are using Ubuntu 16+. If you are using a different OS, please refer to the according installation procedures on fficial [Getting Started](https://devcenter.heroku.com/articles/getting-started-with-python) page.

Login to your heroku account via command line and create a new Heroku app. You can omit the app name parameter, in which case Heroku will assign a random name to your app.

```bash
$ heroku login
heroku: Press any key to open up the browser to login or q to exit: 
Opening browser to https://cli-auth.heroku.com/auth/cli/browser/6dsvj31-d2d2-45ji-vnkk-sdfbjksviuhsf
Logging in... done
Logged in as admin@djangopizza.com
$ heroku create dj-pizza
Creating ⬢ dj-pizza... done
https://dj-pizza.herokuapp.com/ | https://git.heroku.com/dj-pizza.git
```

Add a Postgres Resource to the project using following command:

```bash
$ heroku addons:create heroku-postgresql:hobby-dev
Creating heroku-postgresql:hobby-dev on ⬢ dj-pizza... free
Database has been created and is available
 ! This database is empty. If upgrading, you can transfer
 ! data from another database with pg:copy
Created postgresql-emeraldmeadows-51234 as DATABASE_URL
Use heroku addons:docs heroku-postgresql to view documentation
```

Proceed to open your [Heroku dashboard](https://dashboard.heroku.com/), locating to your newly created app, going into *Settings*, and setting environment variables necessary to run this project. They are located in *Config Vars* section. Refer to `.env.example`.

After that, go ahead and push the master branch to the Heroku server:

```bash
git push heroku master
```

Once everything succeeds, make sure to run migrations on the server:

```bash
heroku run python manage.py migrate
```

After this step, the app should be all set and ready. Open https://dj-pizza.herokuapp.com/ to view it in the browser.