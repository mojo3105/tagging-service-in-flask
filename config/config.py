"""
The script contains configurations for models.
"""

def set_configs(app):
    """
    The function will set configurations for database for the flask app
    :param app: flask app instance
    :return app: flask app instance with database configurations set
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Stocks.sqlite3'
    app.config['SECRET_KEY'] = "random strings"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app