from flask import Blueprint, render_template, request, session
from db import get_cursor

tags_bp = Blueprint('tags', __name__)


@tags_bp.route('/tags')
def popular_tags():
    """List most popular tags (most photos associated)."""
    cur = get_cursor()
    cur.execute("""
        SELECT t.tag_id, t.tag_name, COUNT(pt.photo_id) AS photo_count
        FROM tags t
        JOIN photo_tags pt ON t.tag_id = pt.tag_id
        GROUP BY t.tag_id, t.tag_name
        ORDER BY photo_count DESC
        LIMIT 20
    """)
    tags = cur.fetchall()
    return render_template('tags.html', tags=tags)


@tags_bp.route('/tags/<tag_name>')
def view_tag(tag_name):
    """
    Show photos for a tag.
    ?view=mine  → only current user's photos with this tag
    ?view=all   → all photos with this tag (default)
    """
    view_mode = request.args.get('view', 'all')
    cur = get_cursor()

    # Confirm tag exists
    cur.execute('SELECT tag_id, tag_name FROM tags WHERE tag_name = %s', (tag_name,))
    tag = cur.fetchone()

    photos = []
    if tag:
        if view_mode == 'mine' and 'user_id' in session:
            cur.execute("""
                SELECT p.photo_id, p.caption,
                       a.name AS album_name,
                       u.first_name || ' ' || u.last_name AS owner_name,
                       COUNT(DISTINCT l.user_id) AS like_count
                FROM photos p
                JOIN albums a ON p.album_id = a.album_id
                JOIN users  u ON a.owner_id  = u.user_id
                JOIN photo_tags pt ON p.photo_id = pt.photo_id
                LEFT JOIN likes l ON p.photo_id = l.photo_id
                WHERE pt.tag_id = %s
                  AND a.owner_id = %s
                GROUP BY p.photo_id, p.caption, a.name, owner_name
                ORDER BY p.photo_id DESC
            """, (tag['tag_id'], session['user_id']))
        else:
            view_mode = 'all'
            cur.execute("""
                SELECT p.photo_id, p.caption,
                       a.name AS album_name,
                       u.first_name || ' ' || u.last_name AS owner_name,
                       COUNT(DISTINCT l.user_id) AS like_count
                FROM photos p
                JOIN albums a ON p.album_id = a.album_id
                JOIN users  u ON a.owner_id  = u.user_id
                JOIN photo_tags pt ON p.photo_id = pt.photo_id
                LEFT JOIN likes l ON p.photo_id = l.photo_id
                WHERE pt.tag_id = %s
                GROUP BY p.photo_id, p.caption, a.name, owner_name
                ORDER BY p.photo_id DESC
            """, (tag['tag_id'],))
        photos = cur.fetchall()

    return render_template('tag_photos.html',
                           tag=tag,
                           tag_name=tag_name,
                           photos=photos,
                           view_mode=view_mode)