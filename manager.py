"""
This script runs the FlaskWebProject application using a development server.
"""
from flask_script import Manager

from wt import dashboard

manager = Manager(dashboard.create_app(config_name="development"))

if __name__ == '__main__':
    manager.run()
