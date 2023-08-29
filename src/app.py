import os
from flask import Flask
from flask_restx import Api as ApiRestx

from src.api.routes import register_endpoints_routes
from src.default_config import DefaultConfig


def create_app():
    app = Flask(__name__)

    DefaultConfig.init_loggers()

    app.config.from_object(DefaultConfig)

    app.instance_path = app.config.get("INSTANCE_PATH")

    # create instance folder if not exists
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path, exist_ok=True)

    apix = ApiRestx(app, prefix=DefaultConfig.PREFIX_PATH, title="Website HTML/PNG snapshot API")

    register_endpoints_routes(apix)

    return app
