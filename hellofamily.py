import os
from flask_migrate import Migrate
from app import create_app, db
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission


app = create_app('development')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():

    return dict(db=db, User=User, Role=Role, Permission=Permission)


# @app.cli.command()
# def test():
#     """
#     单元测试
#     :return:
#     """
#     import unittest
#     tests = unittest.TestLoader().discover('tests')
#     unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    app.run(debug=True)
