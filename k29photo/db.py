import os
import psycopg2
import psycopg2.extras
from flask import g

DB_CONFIG = {
    'dbname': 'k29photo',
    'user':   'adamshawky',
    'host':   'localhost'
}

def get_db():
    if 'db' not in g:
        database_url = os.environ.get('https://cjrmikobwqbcowuhiuse.supabase.co')
        if database_url:
            # Production: Supabase/Render connection string
            g.db = psycopg2.connect(database_url, sslmode='require')
        else:
            # Local development fallback
            g.db = psycopg2.connect(**DB_CONFIG)
        g.db.autocommit = False
    return g.db

def get_cursor():
    return get_db().cursor(cursor_factory=psycopg2.extras.RealDictCursor)

def commit():
    get_db().commit()

def rollback():
    get_db().rollback()

def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()