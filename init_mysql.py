from sqlalchemy import create_engine
import secret


def reset_database(database_name):
    url = 'mysql+pymysql://root:{}@localhost/?charset=utf8mb4'.format(secret.database_password)

    e = create_engine(url, echo=True)

    with e.connect() as c:
        c.execute('DROP DATABASE IF EXISTS {}'.format(database_name))
        c.execute('CREATE DATABASE {} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'.format(database_name))


if __name__ == '__main__':
    reset_database('hfdev')
