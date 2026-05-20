# Εισαγωγή Flask και database συναρτήσεων
from flask import Blueprint, render_template
from db import get_cursor

# Δημιουργία blueprint για κύριες σελίδες
main_bp = Blueprint('main', __name__)


# Δρομολόγηση για τα στατιστικά τις αρχικής σελίδας
@main_bp.route('/')
def index():
    cur = get_cursor()

    # Πιο δεκτές φωτογραφίες για την αρχική σελίδα
    cur.execute("""
        SELECT p.photo_id, p.caption,
               a.name  AS album_name,
               u.first_name || ' ' || u.last_name AS owner_name,
               COUNT(DISTINCT l.user_id) AS like_count
        FROM photos p
        JOIN albums a ON p.album_id = a.album_id
        JOIN users  u ON a.owner_id  = u.user_id
        LEFT JOIN likes l ON p.photo_id = l.photo_id
        GROUP BY p.photo_id, p.caption, a.name, owner_name
        ORDER BY like_count DESC, p.photo_id DESC
        LIMIT 12
    """)
    top_photos = cur.fetchall()

    # Καλύτερες 8 ετικέτες
    cur.execute("""
        SELECT t.tag_name, COUNT(pt.photo_id) AS cnt
        FROM tags t
        JOIN photo_tags pt ON t.tag_id = pt.tag_id
        GROUP BY t.tag_name
        ORDER BY cnt DESC
        LIMIT 8
    """)
    popular_tags = cur.fetchall()

    # Συνολικό πλήθος φωτογραφιών και χρηστών
    cur.execute("SELECT COUNT(*) AS cnt FROM photos")
    photo_count = cur.fetchone()['cnt']

    cur.execute("SELECT COUNT(*) AS cnt FROM users")
    user_count = cur.fetchone()['cnt']

    return render_template('index.html',
                           top_photos=top_photos,
                           popular_tags=popular_tags,
                           photo_count=photo_count,
                           user_count=user_count)


# Δρομολόγηση για ιστορικό δραστηριότητας χρηστών
@main_bp.route('/activity')
def activity():
    """Σβάλτε 10 χρήστες κατά βαθμό συντομίας:
       βάθμος = φωτογραφίες + σχόλια σε φωτογραφίες που είναι άλλων"""
    cur = get_cursor()
    # Διαταξη χρηστών κατά γενική δραστηριότητα
    cur.execute("""
        SELECT u.user_id,
               u.first_name || ' ' || u.last_name AS full_name,
               u.hometown,
               COUNT(DISTINCT p.photo_id)  AS photo_count,
               COUNT(DISTINCT c.comment_id) AS comment_count,
               COUNT(DISTINCT p.photo_id) + COUNT(DISTINCT c.comment_id) AS score
        FROM users u
        LEFT JOIN albums  a ON a.owner_id  = u.user_id
        LEFT JOIN photos  p ON p.album_id  = a.album_id
        LEFT JOIN comments c ON c.user_id  = u.user_id
                             AND c.photo_id NOT IN (
                                 SELECT ph.photo_id
                                 FROM photos ph
                                 JOIN albums al ON ph.album_id = al.album_id
                                 WHERE al.owner_id = u.user_id
                             )
        GROUP BY u.user_id, full_name, u.hometown
        ORDER BY score DESC
        LIMIT 10
    """)
    top_users = cur.fetchall()
    return render_template('activity.html', top_users=top_users)


# Δρομολόγηση για προβολή όλων των άλμπουμ
@main_bp.route('/browse')
def browse():
    """Ευκολή πρόσβαση σε ολομ τα άλμπουμ."""
    cur = get_cursor()
    # Λήψη όλων των άλμπουμ και τα στοιχεία τους
    cur.execute("""
        SELECT a.album_id, a.name, a.creation_date,
               u.first_name || ' ' || u.last_name AS owner_name,
               COUNT(p.photo_id) AS photo_count
        FROM albums a
        JOIN users  u ON a.owner_id = u.user_id
        LEFT JOIN photos p ON p.album_id = a.album_id
        GROUP BY a.album_id, a.name, a.creation_date, owner_name
        ORDER BY a.creation_date DESC
    """)
    albums = cur.fetchall()
    return render_template('browse.html', albums=albums)