# Εισαγωγή Flask και database συναρτήσεων
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db import get_cursor, commit, rollback

# Δημιουργία blueprint για σχόλια
comments_bp = Blueprint('comments', __name__)


# Δρομολόγηση για προσθήκη σχολίου σε φωτογραφία
@comments_bp.route('/photos/<int:photo_id>/comment', methods=['POST'])
def post_comment(photo_id):
    content    = request.form.get('content', '').strip()
    guest_name = request.form.get('guest_name', '').strip() or None

    user_id = session.get('user_id')

    # Έλεγχος: το σχόλιο πρέπει να έχει περιεχόμενο
    if not content:
        flash('Comment cannot be empty.', 'error')
        return redirect(url_for('photos.view_photo', photo_id=photo_id))

    # Έλεγχος: επισκέπτης πρέπει να δώσει όνομα
    # Guest must supply a name
    if not user_id and not guest_name:
        flash('Please enter your name to comment as a guest.', 'error')
        return redirect(url_for('photos.view_photo', photo_id=photo_id))

    cur = get_cursor()
    try:
        # Εισαγωγή σχολίου στη βάση δεδομένων
        cur.execute("""
            INSERT INTO comments (photo_id, user_id, guest_name, content)
            VALUES (%s, %s, %s, %s)
        """, (photo_id, user_id, guest_name if not user_id else None, content))
        commit()
        flash('Comment posted!', 'success')
    except Exception as e:
        rollback()
        # Έλεγχος σφάλματος για σχόλια στις δικές του φωτογραφίες
        # Trigger fires for self-comment — show friendly message
        msg = str(e)
        if 'cannot comment on their own' in msg:
            flash('You cannot comment on your own photos.', 'error')
        else:
            flash(f'Error posting comment: {msg}', 'error')

    return redirect(url_for('photos.view_photo', photo_id=photo_id))


# Δρομολόγηση για αναζήτηση σχολίων που ταιριάζουν ακριβώς με το ερώτημα
@comments_bp.route('/search/comments')
def search_comments():
    """
    Αναζήτηση χρηστών των οποίων τα σχόλια ταιριάζουν ακριβώς με το κείμενο ερωτήματος.
    Επιστρέφει χρήστες ταξινομημένους κατά αριθμό συμφωνούντων σχολίων (φθίνουσα σειρά).
    """
    query   = request.args.get('q', '').strip()
    results = []

    if query:
        cur = get_cursor()
        # Αναζήτηση χρηστών με σχόλια που ταιριάζουν ακριβώς
        cur.execute("""
            SELECT u.user_id,
                   u.first_name || ' ' || u.last_name AS full_name,
                   COUNT(*) AS match_count
            FROM comments c
            JOIN users u ON c.user_id = u.user_id
            WHERE c.content = %s
            GROUP BY u.user_id, full_name
            ORDER BY match_count DESC
        """, (query,))
        results = cur.fetchall()

    return render_template('search_comments.html', query=query, results=results)