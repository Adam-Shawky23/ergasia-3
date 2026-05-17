from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db import get_cursor, commit, rollback

comments_bp = Blueprint('comments', __name__)


@comments_bp.route('/photos/<int:photo_id>/comment', methods=['POST'])
def post_comment(photo_id):
    content    = request.form.get('content', '').strip()
    guest_name = request.form.get('guest_name', '').strip() or None

    if not content:
        flash('Comment cannot be empty.', 'error')
        return redirect(url_for('photos.view_photo', photo_id=photo_id))

    user_id = session.get('user_id')

    # Guest must supply a name
    if not user_id and not guest_name:
        flash('Please enter your name to comment as a guest.', 'error')
        return redirect(url_for('photos.view_photo', photo_id=photo_id))

    cur = get_cursor()
    try:
        cur.execute("""
            INSERT INTO comments (photo_id, user_id, guest_name, content)
            VALUES (%s, %s, %s, %s)
        """, (photo_id, user_id, guest_name if not user_id else None, content))
        commit()
        flash('Comment posted!', 'success')
    except Exception as e:
        rollback()
        # Trigger fires for self-comment — show friendly message
        msg = str(e)
        if 'cannot comment on their own' in msg:
            flash('You cannot comment on your own photos.', 'error')
        else:
            flash(f'Error posting comment: {msg}', 'error')

    return redirect(url_for('photos.view_photo', photo_id=photo_id))


@comments_bp.route('/search/comments')
def search_comments():
    """
    Find users whose comments exactly match the query text.
    Returns users sorted by number of matching comments DESC.
    """
    query   = request.args.get('q', '').strip()
    results = []

    if query:
        cur = get_cursor()
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