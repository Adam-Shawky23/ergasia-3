# Εισαγωγή βιβλιοθηκών PostgreSQL και Flask
import psycopg2
import psycopg2.extras
from flask import g

# Ρυθμίσεις σύνδεσης με τη βάση δεδομένων
DB_CONFIG = {
    'dbname':   'k29photo',
    'user':     'adamshawky',
    'password': 'postgres',
    'host':     'localhost',
    'port':     5432,
}

# Συνάρτηση για δημιουργία νέας σύνδεσης ανά αίτημα Flask
def get_db():
    """Ανοιγμα νέας σύνδεσης αν δεν υπάρχει για το τρέχον context εφαρμογής."""
    if 'db' not in g:
        g.db = psycopg2.connect(**DB_CONFIG)
        g.db.autocommit = False
    return g.db

# Συνάρτηση για λήψη cursor με αποτελέσματα ως dictionaries
def get_cursor():
    """Επιστροφή RealDictCursor ώστε τα αποτελέσματα να έρχονται ως dict."""
    return get_db().cursor(cursor_factory=psycopg2.extras.RealDictCursor)

# Συνάρτηση κλεισίματος σύνδεσης βάσης δεδομένων
def close_db(e=None):
    """Κλείσιμο της σύνδεσης BD στο τέλος του αιτήματος."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Συνάρτηση επιβεβαίωσης αλλαγών
def commit():
    get_db().commit()

# Συνάρτηση ακύρωσης αλλαγών
def rollback():
    get_db().rollback()