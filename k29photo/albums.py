# Εισαγωγή απαραίτητων βιβλιοθηκών Flask και database
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from db import get_cursor, commit, rollback

# Δημιουργία blueprint για τη διαχείριση άλμπουμ
albums_bp = Blueprint('albums', __name__)


# Διακοσμητής για έλεγχο αν ο χρήστης είναι συνδεδεμένος
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


# Δρομολόγηση για προβολή ενός άλμπουμ και των φωτογραφιών του
@albums_bp.route('/albums/<int:album_id>')
def view_album(album_id):
    cur = get_cursor()
    cur.execute("""
        SELECT a.album_id, a.name, a.creation_date,
               u.user_id AS owner_id,
               u.first_name || ' ' || u.last_name AS owner_name
        FROM albums a
        JOIN users u ON a.owner_id = u.user_id
        WHERE a.album_id = %s
    """, (album_id,))
    album = cur.fetchone()
    if not album:
        abort(404)

    cur.execute("""
        SELECT p.photo_id, p.caption,
               COUNT(DISTINCT l.user_id) AS like_count,
               COUNT(DISTINCT c.comment_id) AS comment_count
        FROM photos p
        LEFT JOIN likes    l ON p.photo_id = l.photo_id
        LEFT JOIN comments c ON p.photo_id = c.photo_id
        WHERE p.album_id = %s
        GROUP BY p.photo_id, p.caption
        ORDER BY p.photo_id
    """, (album_id,))
    photos = cur.fetchall()

    return render_template('album.html', album=album, photos=photos)


# Δρομολόγηση για δημιουργία νέου άλμπουμ (GET - φόρμα, POST - αποθήκευση)
@albums_bp.route('/albums/create', methods=['GET', 'POST'])
@login_required
def create_album():
    if request.method == 'POST':
        name = request.form['name'].strip()
        if not name:
            flash('Album name is required.', 'error')
            return render_template('create_album.html')
        cur = get_cursor()
        try:
            cur.execute("""
                INSERT INTO albums (name, owner_id)
                VALUES (%s, %s) RETURNING album_id
            """, (name, session['user_id']))
            album_id = cur.fetchone()['album_id']
            commit()
            flash('Album created!', 'success')
            return redirect(url_for('albums.view_album', album_id=album_id))
        except Exception as e:
            rollback()
            flash(f'Error creating album: {e}', 'error')

    return render_template('create_album.html')


# Δρομολόγηση για διαγραφή άλμπουμ (μόνο POST)
@albums_bp.route('/albums/<int:album_id>/delete', methods=['POST'])
@login_required
def delete_album(album_id):
    cur = get_cursor()
    cur.execute('SELECT owner_id FROM albums WHERE album_id = %s', (album_id,))
    album = cur.fetchone()
    if not album:
        abort(404)
    if album['owner_id'] != session['user_id']:
        abort(403)
    try:
        cur.execute('DELETE FROM albums WHERE album_id = %s', (album_id,))
        commit()
        flash('Album deleted.', 'success')
    except Exception as e:
        rollback()
        flash(f'Error deleting album: {e}', 'error')
    return redirect(url_for('main.browse'))


# Δρομολόγηση για προβολή όλων των άλμπουμ του χρήστη
@albums_bp.route('/my-albums')
@login_required
def my_albums():
    cur = get_cursor()
    cur.execute("""
        SELECT a.album_id, a.name, a.creation_date,
               COUNT(p.photo_id) AS photo_count
        FROM albums a
        LEFT JOIN photos p ON p.album_id = a.album_id
        WHERE a.owner_id = %s
        GROUP BY a.album_id, a.name, a.creation_date
        ORDER BY a.creation_date DESC
    """, (session['user_id'],))
    albums = cur.fetchall()
    return render_template('my_albums.html', albums=albums)