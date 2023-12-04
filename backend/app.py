import os
from typing import Optional

from bson import ObjectId
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager

from components.user import User
from monad import option
from routes.order_routes import order_route
from routes.user_routes import user_route

load_dotenv()

flask_app = Flask(__name__)

if __name__ == "__main__":
    flask_app.secret_key = option.unwrap_or(
        os.getenv("FLASK_SECRET_KEY"), "114514_1919810"
    )

    cors = CORS(flask_app)
    flask_app.config["CORS_HEADERS"] = "Content-Type"

    login_manager = LoginManager()
    login_manager.init_app(flask_app)

    @login_manager.user_loader
    def load_user(user_id: str) -> Optional[User]:
        return User.from_id(ObjectId(user_id))

    flask_app.register_blueprint(user_route, url_prefix="/user")
    flask_app.register_blueprint(order_route, url_prefix="/order")
    flask_pp.run(debug=True)
