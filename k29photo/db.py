import psycopg2
import psycopg2.extras
from flask import g

DB_CONFIG = {
    'dbname':   'k29photo',
    'user':     'postgres',
    'password': 'postgres',
    'host':     'localhost',
    'port':     5432,
}

def get_db():
    """Open a new DB connection if there is none for the current app context."""
    if 'db' not in g:
        g.db = psycopg2.connect(**DB_CONFIG)
        g.db.autocommit = False
    return g.db

def get_cursor():
    """Return a RealDictCursor so rows come back as dicts."""
    return get_db().cursor(cursor_factory=psycopg2.extras.RealDictCursor)

def close_db(e=None):
    """Close the DB connection at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def commit():
    get_db().commit()

def rollback():
    get_db().rollback()