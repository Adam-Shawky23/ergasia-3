from flask import Blueprint, render_template
from db import get_cursor

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    cur = get_cursor()

    # Latest 12 photos for homepage gallery
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
        ORDER BY p.photo_id DESC
        LIMIT 12
    """)
    recent_photos = cur.fetchall()

    # Top 5 popular tags for sidebar
    cur.execute("""
        SELECT t.tag_name, COUNT(pt.photo_id) AS cnt
        FROM tags t
        JOIN photo_tags pt ON t.tag_id = pt.tag_id
        GROUP BY t.tag_name
        ORDER BY cnt DESC
        LIMIT 5
    """)
    popular_tags = cur.fetchall()

    return render_template('index.html',
                           recent_photos=recent_photos,
                           popular_tags=popular_tags)


@main_bp.route('/activity')
def activity():
    """Top 10 users by contribution score:
       score = photos_uploaded + comments_on_others_photos"""
    cur = get_cursor()
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


@main_bp.route('/browse')
def browse():
    """Browse all albums publicly."""
    cur = get_cursor()
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