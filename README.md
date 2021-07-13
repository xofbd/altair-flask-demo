# Altair Flask Demo

This project demonstrates how to serve an [Altair](https://altair-viz.github.io) visualization using [Flask](https://flask.palletsprojects.com). The application shows potential sites to implement a geothermal energy technology by re-purposing old wells. The user specifies the criteria for the wells and a plot is generated showing the location of those wells. One can deploy this app using a service like [Heroku](https://heroku.com) or just locally.

## Prerequisites

### Python environment
All required Python packages can be found in the `requirements.txt` file. Since the project makes use of GNU Make, there is no need to directly create the environment. The creation and activation of the environment is handled by running the Make rules that are shown in later sections.

### SQL database
The application uses an SQL database and makes queries against it to obtain the wells to visualize. Two options are presented: SQLite for only local deployment or PostgreSQL for either local or deployment to Heroku. Instructions for both are found below. Note, you can skip the last step of each and jump to deployment by running `make all`, as running `make all` takes care of creating the database once `.env` has been configured properly.

#### SQLite
1. Create your own `.env`: `cp .env.template .env`
1. Assign `URI_DB` to `sqlite:///data/wells.db`
1. Run `make create_db`

#### Heroku managed PostgreSQL
1. Create a [Heroku](https://heroku.com) account
1. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)
1. Create your own `.env`: `cp .env.template .env`
1. Create a Heroku app: `heroku create`
1. In your `.env`, set `APP_NAME` to your application's name form the previous step
1. Run `make create_db`

## Deployment
Now that you have the SQL database has been created and `.env` configured properly, you are ready to deploy locally or to Heroku.
To deploy the app locally, simply run  `make deploy`. It will use whatever database is specified in `URI_DB` in `.env`.

To deploy the app to Heroku:

1. `git push heroku master`
1. `heroku open`

## Deployment with Docker

You can deploy and run the application locally using [Docker](https://www.docker.com/). After creating a database, you can run `make deploy-docker` or:

1. `docker build -t flask_app .`
1. `docker run -d -p 5000:5000 flask_app`

As with other methods, you need to make sure you've created your database and properly configured your `.env.`

## License

This project is distributed under the GNU General Purpose License. Please see `LICENSE` for more information.
