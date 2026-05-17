from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db import get_cursor, commit, rollback

friends_bp = Blueprint('friends', __name__)


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


@friends_bp.route('/friends')
@login_required
def my_friends():
    """Show current user's friends list and a search box."""
    cur = get_cursor()

    # Friends the current user follows
    cur.execute("""
        SELECT u.user_id,
               u.first_name || ' ' || u.last_name AS full_name,
               u.hometown
        FROM friends f
        JOIN users u ON f.friend_id = u.user_id
        WHERE f.user_id = %s
        ORDER BY full_name
    """, (session['user_id'],))
    friends = cur.fetchall()

    # Search other users
    search_q = request.args.get('q', '').strip()
    search_results = []
    if search_q:
        cur.execute("""
            SELECT u.user_id,
                   u.first_name || ' ' || u.last_name AS full_name,
                   u.hometown,
                   EXISTS (
                       SELECT 1 FROM friends
                       WHERE user_id = %s AND friend_id = u.user_id
                   ) AS already_friend
            FROM users u
            WHERE u.user_id != %s
              AND (LOWER(u.first_name || ' ' || u.last_name) LIKE LOWER(%s)
                   OR LOWER(u.email) LIKE LOWER(%s))
            ORDER BY full_name
        """, (session['user_id'], session['user_id'],
              f'%{search_q}%', f'%{search_q}%'))
        search_results = cur.fetchall()

    return render_template('friends.html',
                           friends=friends,
                           search_q=search_q,
                           search_results=search_results)


@friends_bp.route('/friends/add/<int:friend_id>', methods=['POST'])
@login_required
def add_friend(friend_id):
    if friend_id == session['user_id']:
        flash('You cannot add yourself as a friend.', 'error')
        return redirect(url_for('friends.my_friends'))

    cur = get_cursor()
    try:
        cur.execute("""
            INSERT INTO friends (user_id, friend_id)
            VALUES (%s, %s) ON CONFLICT DO NOTHING
        """, (session['user_id'], friend_id))
        commit()
        flash('Friend added!', 'success')
    except Exception as e:
        rollback()
        flash(f'Error: {e}', 'error')

    return redirect(url_for('friends.my_friends'))


@friends_bp.route('/friends/remove/<int:friend_id>', methods=['POST'])
@login_required
def remove_friend(friend_id):
    cur = get_cursor()
    try:
        cur.execute("""
            DELETE FROM friends WHERE user_id = %s AND friend_id = %s
        """, (session['user_id'], friend_id))
        commit()
        flash('Friend removed.', 'info')
    except Exception as e:
        rollback()
        flash(f'Error: {e}', 'error')

    return redirect(url_for('friends.my_friends'))