from flask import Flask


CONFIG_TO_OBJECT = {
    'dev': 'config.ConfigDev',
    'prod': 'config.ConfigProd',
    'testing': 'config.ConfigTesting',
}


def create_app(config='dev'):
    app = Flask(__name__)
    app.config.from_object(CONFIG_TO_OBJECT[config])

    from app import views
    app.register_blueprint(views.bp)

    return app
