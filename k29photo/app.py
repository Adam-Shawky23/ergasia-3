import os
from flask import Flask
from db import close_db
from auth import auth_bp
from albums import albums_bp
from photos import photos_bp
from tags import tags_bp
from comments import comments_bp
from friends import friends_bp
from recommendations import recommendations_bp
from main import main_bp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def create_app():
    app = Flask(__name__,
                template_folder=os.path.join(BASE_DIR, 'templates'),
                static_folder=os.path.join(BASE_DIR, 'static'))
    app.secret_key = 'k29photo-secret-key-change-in-production'

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(albums_bp)
    app.register_blueprint(photos_bp)
    app.register_blueprint(tags_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(friends_bp)
    app.register_blueprint(recommendations_bp)

    app.teardown_appcontext(close_db)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)
