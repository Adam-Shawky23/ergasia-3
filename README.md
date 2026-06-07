# k29photo

A full-stack photo-sharing web portal built with **Flask** and **PostgreSQL**, inspired by Flickr. Developed as a university database systems project at the National and Kapodistrian University of Athens (NKUA), Department of Informatics & Telecommunications.

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=flat&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=flat&logo=postgresql&logoColor=white)
![psycopg2](https://img.shields.io/badge/psycopg2-2.9-336791?style=flat)

- **Backend**: Flask (Python 3), raw SQL via psycopg2 — no ORM
- **Database**: PostgreSQL with triggers, constraints, and indexes
- **Frontend**: Jinja2 templates, vanilla CSS (dark editorial theme)
- **Auth**: Session-based authentication, bcrypt password hashing via werkzeug

---

## Features

### User Management
- Register / login / logout with duplicate email detection
- Friends system (directional follow model)
- User search by name or email
- Top 10 contributors leaderboard (score = photos uploaded + comments on others' photos)

### Albums & Photos
- Create, view, and delete albums
- Upload photos (stored as binary BYTEA in PostgreSQL)
- Automatic MIME type detection (PNG, JPEG, GIF, WebP)
- Public browsing — no login required to view content

### Tags
- Tag photos with multiple lowercase tags
- Browse all photos by tag with All / My Photos toggle
- Popular tags page sorted by usage count
- AND-based tag search (e.g. `nafplion sea` finds photos with both tags)

### Comments & Likes
- Registered users and guests can comment on photos
- Users cannot comment on their own photos (enforced by DB trigger)
- Like / unlike photos
- View like count and names of users who liked a photo
- Exact-match comment text search, results ranked by match count

### Recommendations
- **Friend suggestions**: friends-of-friends algorithm, ranked by mutual connection count
- **You may also like**: based on user's 5 most-used tags, ranked by tag match count with fewer total tags as tiebreaker

---

## Database Design

8 tables with full referential integrity:

```
users         — registered users
albums        — photo collections owned by users
photos        — binary image data + caption + tags
tags          — global lowercase tag vocabulary
photo_tags    — M:N junction: photos ↔ tags
comments      — supports both registered users and guests
friends       — directional follow relationships
likes         — M:N junction: users ↔ photos
```

### Constraints & Triggers

| Name | Type | Description |
|------|------|-------------|
| `users.email` | UNIQUE | Prevents duplicate registration |
| `users.gender` | CHECK | Must be M, F, or O |
| `tags.tag_name` | CHECK | Lowercase, no spaces |
| `comments` | CHECK | Either user_id or guest_name must be set, not both |
| `friends` | CHECK | Cannot follow yourself |
| `trg_no_self_comment` | TRIGGER | Prevents commenting on own photos |
| All FKs | CASCADE | Deleting a user removes all their data |

---

## Setup

### Prerequisites
- Python 3.8+
- PostgreSQL 14+

### Quick start

```bash
git clone https://github.com/yourusername/k29photo.git
cd k29photo

# Install dependencies
pip install -r requirements.txt

# Configure database credentials
# Open db.py and set DB_CONFIG['user'] to your PostgreSQL username

# Run setup (creates DB, loads schema + sample data, starts server)
bash setup.sh
```

Then open **http://localhost:5000** in your browser.

### Manual setup

```bash
pip install -r requirements.txt
createdb k29photo
psql -d k29photo -f schema.sql
psql -d k29photo -f data.sql
python3 app.py
```

### Sample data credentials

The database ships with 12 sample users. All use password **`password123`**.

| Email | Name |
|-------|------|
| nikos.p@gmail.com | Nikos Papadopoulos |
| maria.g@gmail.com | Maria Georgiou |
| kostas.a@gmail.com | Kostas Alexiou |

---

## Project Structure

```
k29photo/
├── app.py                  # Flask app factory, blueprint registration
├── db.py                   # PostgreSQL connection (psycopg2)
├── utils.py                # Shared decorators (login_required)
├── main.py                 # Homepage, browse, activity leaderboard
├── auth.py                 # Register, login, logout
├── albums.py               # Album CRUD
├── photos.py               # Photo upload/delete/serve, tag search
├── tags.py                 # Tag browsing, popular tags
├── comments.py             # Post comments, comment search
├── friends.py              # Friends list, user search, follow/unfollow
├── recommendations.py      # Friend-of-friend + you-may-also-like
├── schema.sql              # CREATE TABLE, triggers, indexes
├── data.sql                # Sample data (12 users, 30 photos, 20 tags)
├── setup.sh                # One-command setup script
├── requirements.txt
├── static/
│   └── style.css           # Dark editorial theme
└── templates/              # Jinja2 HTML templates (17 files)
```

---

## SQL Highlights

**AND tag search** — finds photos matching ALL specified tags:
```sql
SELECT p.photo_id, p.caption, ...
FROM photos p
WHERE p.photo_id IN (
    SELECT pt.photo_id
    FROM photo_tags pt
    JOIN tags t ON pt.tag_id = t.tag_id
    WHERE t.tag_name = ANY(%s)
    GROUP BY pt.photo_id
    HAVING COUNT(DISTINCT t.tag_name) = %s
)
```

**Contribution score leaderboard**:
```sql
SELECT u.user_id,
       COUNT(DISTINCT p.photo_id) + COUNT(DISTINCT c.comment_id) AS score
FROM users u
LEFT JOIN albums  a ON a.owner_id = u.user_id
LEFT JOIN photos  p ON p.album_id = a.album_id
LEFT JOIN comments c ON c.user_id = u.user_id
                     AND c.photo_id NOT IN (
                         SELECT ph.photo_id FROM photos ph
                         JOIN albums al ON ph.album_id = al.album_id
                         WHERE al.owner_id = u.user_id
                     )
GROUP BY u.user_id
ORDER BY score DESC LIMIT 10
```

**You-may-also-like** — ranked by tag match count, tiebroken by specificity:
```sql
SELECT p.photo_id,
       COUNT(DISTINCT CASE WHEN pt.tag_id = ANY(%s) THEN pt.tag_id END) AS match_count,
       COUNT(DISTINCT pt.tag_id) AS total_tags
FROM photos p
JOIN photo_tags pt ON p.photo_id = pt.photo_id
WHERE p.photo_id IN (SELECT photo_id FROM photo_tags WHERE tag_id = ANY(%s))
GROUP BY p.photo_id
ORDER BY match_count DESC, total_tags ASC
```

---

## Course

**K29: Database Design and Use** — Spring 2026
National and Kapodistrian University of Athens
Department of Informatics & Telecommunications