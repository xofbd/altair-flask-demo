# Altair Flask Demo

This project demonstrates how to serve an Altair visualization using Flask. The application shows potential sites to implement a geothermal energy technology. The user specifies the criteria for the wells and a plot is generated showing the location of those wells.

## Prerequisites

All required Python packages can be found in the `requirements.txt` file. Additionally, the provided `Makefile` can be used to create a virtual environment by running `make venv`. You will also need a Heroku account, and to have installed the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install).

## Running the app locally using Flask

You may want to run the app using Flask locally before deploying it to Heroku, especially if you have made any changes to the code. To run locally:

1. clone the repository.
1. in the repository, run `make deploy`.
1. open the link provided in the command line.

If you are using Windows, you can:

1. create and activate the virtual environment.

        py -3 -m venv venv
        venv\Scripts\activate.bat

1. `set FLASK_APP=flask_app\app.py` in the command line.
1. run `python -m flask run`.
1. open the link in the command line.

Alternatively, you can deploy using [Docker](https://www.docker.com/).

1. `docker build -t flask_app .`
1. `docker run -d -p 5000:5000 flask_app`

## Deploying to Heroku

Make sure your app is ready to be deployed to Heroku by running Flask locally. To deploy to Heroku:

1. clone the repository (if you haven't yet).
1. `heroku login` and enter your credentials.
1. `heroku create` or `heroku create app-name` where app-name is a custom app name.
1. `git push heroku master`.
1. `heroku config:set DEPLOY=heroku`.
1. `heroku open` or open the app online through your Heroku profile.

## License

This project is distributed under the GNU General Purpose License. Please see `LICENSE` for more information.
