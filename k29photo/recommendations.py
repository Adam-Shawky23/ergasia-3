# Εισαγωγή Flask και database συναρτήσεων
from flask import Blueprint, render_template, session, redirect, url_for, flash
from db import get_cursor

# Δημιουργία blueprint για προτάσεις
recommendations_bp = Blueprint('recommendations', __name__)


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


# Δρομολόγηση για προτάσεις φίλων και φωτογραφιών
@recommendations_bp.route('/recommendations')
@login_required
def recommendations():
    cur = get_cursor()
    user_id = session['user_id']

    # Προτάσεις φίλων: φίλοι των φίλων που δεν είναι ήδη δικοί μου
    # Παλιαος αλγόριθμος: friend-of-friend
    cur.execute("""
        SELECT u.user_id,
               u.first_name || ' ' || u.last_name AS full_name,
               u.hometown,
               COUNT(*) AS mutual_count
        FROM friends f1                          -- δικοί μου φίλοι
        JOIN friends f2 ON f1.friend_id = f2.user_id  -- των φίλων μου
        JOIN users   u  ON f2.friend_id = u.user_id
        WHERE f1.user_id = %s
          AND f2.friend_id != %s                 -- όχι εσύ 
          AND f2.friend_id NOT IN (              -- όχι ήδη δικός μου φίλος
              SELECT friend_id FROM friends WHERE user_id = %s
          )
        GROUP BY u.user_id, full_name, u.hometown
        ORDER BY mutual_count DESC, full_name
        LIMIT 10
    """, (user_id, user_id, user_id))
    friend_recs = cur.fetchall()

    # Φωτογραφίες που μπορεί να σας αρέσουν
    # Βήμα 1: πάρουμε τις 5 πιο αντιχνειζόμενες ετικέτες
    cur.execute("""
        SELECT t.tag_id, t.tag_name, COUNT(*) AS cnt
        FROM photo_tags pt
        JOIN photos  p ON pt.photo_id = p.photo_id
        JOIN albums  a ON p.album_id  = a.album_id
        JOIN tags    t ON pt.tag_id   = t.tag_id
        WHERE a.owner_id = %s
        GROUP BY t.tag_id, t.tag_name
        ORDER BY cnt DESC
        LIMIT 5
    """, (user_id,))
    top_tags = cur.fetchall()

    photo_recs = []
    if top_tags:
        tag_ids = [row['tag_id'] for row in top_tags]
        n_tags  = len(tag_ids)

        # Βήμα 2: αναζήτηση φωτογραφιών με αυτές τις ετικέτες
        # Αποκλείεται τα δικά μας φωτογραφίες
        cur.execute("""
            SELECT p.photo_id, p.caption,
                   a.name AS album_name,
                   u.first_name || ' ' || u.last_name AS owner_name,
                   COUNT(DISTINCT CASE WHEN pt.tag_id = ANY(%s) THEN pt.tag_id END)
                       AS match_count,
                   COUNT(DISTINCT pt.tag_id) AS total_tags,
                   COUNT(DISTINCT l.user_id) AS like_count
            FROM photos p
            JOIN albums     a  ON p.album_id  = a.album_id
            JOIN users      u  ON a.owner_id  = u.user_id
            JOIN photo_tags pt ON p.photo_id  = pt.photo_id
            LEFT JOIN likes l  ON p.photo_id  = l.photo_id
            WHERE a.owner_id != %s
              AND p.photo_id IN (
                  SELECT photo_id FROM photo_tags
                  WHERE tag_id = ANY(%s)
              )
            GROUP BY p.photo_id, p.caption, a.name, owner_name
            ORDER BY match_count DESC, total_tags ASC
            LIMIT 12
        """, (tag_ids, user_id, tag_ids))
        photo_recs = cur.fetchall()

    return render_template('recommendations.html',
                           friend_recs=friend_recs,
                           photo_recs=photo_recs,
                           top_tags=top_tags)