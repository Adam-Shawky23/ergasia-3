# Εισαγωγή Flask και database συναρτήσεων
from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, flash, abort, send_file, Response)
from db import get_cursor, commit, rollback
import io

# Δημιουργία blueprint για φωτογραφίες
photos_bp = Blueprint('photos', __name__)


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


# Δρομολόγηση για προβολή μιας φωτογραφίας και των σχολίων της
@photos_bp.route('/photos/<int:photo_id>')
def view_photo(photo_id):
    cur = get_cursor()
    # Λήψη στοιχείων φωτογραφίας
    cur.execute("""
        SELECT p.photo_id, p.caption, p.album_id,
               a.name AS album_name,
               u.user_id AS owner_id,
               u.first_name || ' ' || u.last_name AS owner_name
        FROM photos p
        JOIN albums a ON p.album_id  = a.album_id
        JOIN users  u ON a.owner_id  = u.user_id
        WHERE p.photo_id = %s
    """, (photo_id,))
    photo = cur.fetchone()
    if not photo:
        abort(404)

    # Λήψη ετικετών της φωτογραφίας
    cur.execute("""
        SELECT t.tag_id, t.tag_name
        FROM tags t
        JOIN photo_tags pt ON t.tag_id = pt.tag_id
        WHERE pt.photo_id = %s
        ORDER BY t.tag_name
    """, (photo_id,))
    tags = cur.fetchall()

    # Λήψη σχολίων στη φωτογραφία
    cur.execute("""
        SELECT c.comment_id, c.content, c.post_date,
               COALESCE(u.first_name || ' ' || u.last_name, c.guest_name) AS author,
               c.user_id
        FROM comments c
        LEFT JOIN users u ON c.user_id = u.user_id
        WHERE c.photo_id = %s
        ORDER BY c.post_date ASC
    """, (photo_id,))
    comments = cur.fetchall()

    # Λήψη χρηστών που έδωσαν ψήφους
    cur.execute("""
        SELECT u.user_id,
               u.first_name || ' ' || u.last_name AS full_name
        FROM likes l
        JOIN users u ON l.user_id = u.user_id
        WHERE l.photo_id = %s
    """, (photo_id,))
    likes = cur.fetchall()

    # Έλεγχος αν ο τρέχων χρήστης έχει θέσει στοίχεια ψήφου
    user_liked = False
    if 'user_id' in session:
        cur.execute("""
            SELECT 1 FROM likes
            WHERE user_id = %s AND photo_id = %s
        """, (session['user_id'], photo_id))
        user_liked = cur.fetchone() is not None

    return render_template('photo.html',
                           photo=photo,
                           tags=tags,
                           comments=comments,
                           likes=likes,
                           user_liked=user_liked)


# Δρομολόγηση για προβολή εικόνας φωτογραφίας
@photos_bp.route('/photos/<int:photo_id>/image')
def serve_image(photo_id):
    cur = get_cursor()
    # Λήψη δεδομένων εικόνας
    cur.execute('SELECT data FROM photos WHERE photo_id = %s', (photo_id,))
    row = cur.fetchone()
    if not row:
        abort(404)
    data = bytes(row['data'])
    # Έλεγχος τύπου εικόνας από μαγική συναγώγή
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        mime = 'image/png'
    elif data[:3] == b'\xff\xd8\xff':
        mime = 'image/jpeg'
    elif data[:6] in (b'GIF87a', b'GIF89a'):
        mime = 'image/gif'
    elif data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        mime = 'image/webp'
    else:
        mime = 'image/jpeg'
    return Response(data, mimetype=mime)


# Δρομολόγηση για φόρτωση νέας φωτογραφίας
@photos_bp.route('/photos/upload', methods=['GET', 'POST'])
@login_required
def upload_photo():
    cur = get_cursor()
    # Λήψη άλμπουμ του χρήστη
    cur.execute("""
        SELECT album_id, name FROM albums
        WHERE owner_id = %s ORDER BY name
    """, (session['user_id'],))
    albums = cur.fetchall()

    if request.method == 'POST':
        album_id = request.form.get('album_id')
        caption  = request.form.get('caption', '').strip()
        tags_raw = request.form.get('tags', '').strip().lower()
        file     = request.files.get('photo')

        # Έλεγχος απαιτούμενων πεδίων
        if not album_id or not file or file.filename == '':
            flash('Album and photo file are required.', 'error')
            return render_template('upload_photo.html', albums=albums)

        # Έλεγχος κτείασης
        cur.execute('SELECT owner_id FROM albums WHERE album_id = %s', (album_id,))
        alb = cur.fetchone()
        if not alb or alb['owner_id'] != session['user_id']:
            abort(403)

        # Ανάγνωση δεδομένων εικόνας
        image_data = file.read()
        try:
            from psycopg2 import Binary
            # Εισαγωγή φωτογραφίας στη βάση δεδομένων
            cur.execute("""
                INSERT INTO photos (album_id, caption, data)
                VALUES (%s, %s, %s) RETURNING photo_id
            """, (album_id, caption, Binary(image_data)))
            photo_id = cur.fetchone()['photo_id']

            # Εισαγωγή ετικετών και άλλη λογική
            if tags_raw:
                tag_list = [t.strip() for t in tags_raw.replace(',', ' ').split() if t.strip()]
                for tag_name in tag_list:
                    # Εισαγωγή ή αναματε ετικέτας
                    cur.execute("""
                        INSERT INTO tags (tag_name) VALUES (%s)
                        ON CONFLICT (tag_name) DO NOTHING
                    """, (tag_name,))
                    cur.execute('SELECT tag_id FROM tags WHERE tag_name = %s', (tag_name,))
                    tag_id = cur.fetchone()['tag_id']
                    # Γνώσεις φωτογραφίας-ετικέτας
                    cur.execute("""
                        INSERT INTO photo_tags (photo_id, tag_id)
                        VALUES (%s, %s) ON CONFLICT DO NOTHING
                    """, (photo_id, tag_id))

            commit()
            flash('Photo uploaded!', 'success')
            return redirect(url_for('photos.view_photo', photo_id=photo_id))
        except Exception as e:
            rollback()
            flash(f'Upload failed: {e}', 'error')

    return render_template('upload_photo.html', albums=albums)


@photos_bp.route('/photos/<int:photo_id>/delete', methods=['POST'])
@login_required
def delete_photo(photo_id):
    cur = get_cursor()
    cur.execute("""
        SELECT a.owner_id, p.album_id
        FROM photos p
        JOIN albums a ON p.album_id = a.album_id
        WHERE p.photo_id = %s
    """, (photo_id,))
    row = cur.fetchone()
    if not row:
        abort(404)
    if row['owner_id'] != session['user_id']:
        abort(403)
    album_id = row['album_id']
    try:
        cur.execute('DELETE FROM photos WHERE photo_id = %s', (photo_id,))
        commit()
        flash('Photo deleted.', 'success')
    except Exception as e:
        rollback()
        flash(f'Error deleting photo: {e}', 'error')
    return redirect(url_for('albums.view_album', album_id=album_id))


@photos_bp.route('/photos/<int:photo_id>/like', methods=['POST'])
def like_photo(photo_id):
    if 'user_id' not in session:
        flash('Please log in to like photos.', 'error')
        return redirect(url_for('auth.login'))
    cur = get_cursor()
    try:
        from psycopg2 import Binary
        cur.execute("""
            INSERT INTO likes (user_id, photo_id)
            VALUES (%s, %s) ON CONFLICT DO NOTHING
        """, (session['user_id'], photo_id))
        commit()
        flash('Photo liked!', 'success')
    except Exception as e:
        rollback()
        flash(str(e), 'error')
    return redirect(url_for('photos.view_photo', photo_id=photo_id))


@photos_bp.route('/photos/<int:photo_id>/unlike', methods=['POST'])
@login_required
def unlike_photo(photo_id):
    cur = get_cursor()
    try:
        cur.execute("""
            DELETE FROM likes WHERE user_id = %s AND photo_id = %s
        """, (session['user_id'], photo_id))
        commit()
        flash('Like removed.', 'info')
    except Exception as e:
        rollback()
        flash(str(e), 'error')
    return redirect(url_for('photos.view_photo', photo_id=photo_id))


@photos_bp.route('/search')
def search():
    """AND-based tag search + popular tags for discover page."""
    query   = request.args.get('q', '').strip().lower()
    results = []
    cur     = get_cursor()

    if query:
        tag_list = query.split()
        n = len(tag_list)
        cur.execute("""
            SELECT p.photo_id, p.caption,
                   a.name AS album_name,
                   u.first_name || ' ' || u.last_name AS owner_name,
                   COUNT(DISTINCT l.user_id) AS like_count
            FROM photos p
            JOIN albums a ON p.album_id = a.album_id
            JOIN users  u ON a.owner_id  = u.user_id
            LEFT JOIN likes l ON p.photo_id = l.photo_id
            WHERE p.photo_id IN (
                SELECT pt.photo_id
                FROM photo_tags pt
                JOIN tags t ON pt.tag_id = t.tag_id
                WHERE t.tag_name = ANY(%s)
                GROUP BY pt.photo_id
                HAVING COUNT(DISTINCT t.tag_name) = %s
            )
            GROUP BY p.photo_id, p.caption, a.name, owner_name
            ORDER BY like_count DESC
        """, (tag_list, n))
        results = cur.fetchall()

    # Always load popular tags for the discover page
    cur.execute("""
        SELECT t.tag_name, COUNT(pt.photo_id) AS photo_count
        FROM tags t
        JOIN photo_tags pt ON t.tag_id = pt.tag_id
        GROUP BY t.tag_name
        ORDER BY photo_count DESC
        LIMIT 20
    """)
    tags = cur.fetchall()

    return render_template('search.html', query=query, results=results, tags=tags)