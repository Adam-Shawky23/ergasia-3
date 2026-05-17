-- =============================================================
--  k29photo — PostgreSQL Schema
--  Course: K29 Database Design and Use, Spring 2026
-- =============================================================

-- ---------------------------------------------------------------
-- 1. USERS
-- ---------------------------------------------------------------
CREATE TABLE users (
    user_id     SERIAL PRIMARY KEY,
    first_name  VARCHAR(50)  NOT NULL,
    last_name   VARCHAR(50)  NOT NULL,
    email       VARCHAR(100) NOT NULL UNIQUE,
    dob         DATE,                          -- optional per spec
    hometown    VARCHAR(100),
    gender      CHAR(1) CHECK (gender IN ('M', 'F', 'O')),
    password    VARCHAR(255) NOT NULL          -- store hashed value
);

-- ---------------------------------------------------------------
-- 2. ALBUMS
-- ---------------------------------------------------------------
CREATE TABLE albums (
    album_id      SERIAL PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    owner_id      INT          NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    creation_date DATE         NOT NULL DEFAULT CURRENT_DATE
);

-- ---------------------------------------------------------------
-- 3. PHOTOS
-- ---------------------------------------------------------------
CREATE TABLE photos (
    photo_id  SERIAL PRIMARY KEY,
    album_id  INT          NOT NULL REFERENCES albums(album_id) ON DELETE CASCADE,
    caption   VARCHAR(255),
    data      BYTEA        NOT NULL             -- binary image data
);

-- ---------------------------------------------------------------
-- 4. TAGS
--    Global, lowercase, no spaces (enforced by CHECK)
-- ---------------------------------------------------------------
CREATE TABLE tags (
    tag_id   SERIAL PRIMARY KEY,
    tag_name VARCHAR(50) NOT NULL UNIQUE
                CHECK (tag_name = LOWER(tag_name) AND tag_name NOT LIKE '% %')
);

-- ---------------------------------------------------------------
-- 5. PHOTO_TAGS  (M:N junction)
-- ---------------------------------------------------------------
CREATE TABLE photo_tags (
    photo_id INT NOT NULL REFERENCES photos(photo_id) ON DELETE CASCADE,
    tag_id   INT NOT NULL REFERENCES tags(tag_id)     ON DELETE CASCADE,
    PRIMARY KEY (photo_id, tag_id)
);

-- ---------------------------------------------------------------
-- 6. COMMENTS
--    Both registered users and guests may comment.
--    user_id = NULL  → guest comment (guest_name required)
--    user_id = value → registered user (guest_name ignored)
--    Users cannot comment on their own photos (enforced by trigger).
-- ---------------------------------------------------------------
CREATE TABLE comments (
    comment_id  SERIAL PRIMARY KEY,
    photo_id    INT          NOT NULL REFERENCES photos(photo_id)  ON DELETE CASCADE,
    user_id     INT          REFERENCES users(user_id) ON DELETE SET NULL,
    guest_name  VARCHAR(100),                  -- used when user_id IS NULL
    content     TEXT         NOT NULL,
    post_date   DATE         NOT NULL DEFAULT CURRENT_DATE,

    -- Either registered user OR guest, not neither
    CONSTRAINT chk_commenter CHECK (
        (user_id IS NOT NULL AND guest_name IS NULL)
        OR
        (user_id IS NULL AND guest_name IS NOT NULL)
    )
);

-- ---------------------------------------------------------------
-- 7. FRIENDS
--    Directional: (user_id → friend_id) means user_id follows friend_id.
--    No self-friendship (enforced by CHECK + trigger).
-- ---------------------------------------------------------------
CREATE TABLE friends (
    user_id   INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    friend_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, friend_id),
    CONSTRAINT chk_no_self_friend CHECK (user_id <> friend_id)
);

-- ---------------------------------------------------------------
-- 8. LIKES
--    A user can like a photo at most once.
--    Users cannot like their own photos (enforced by trigger).
-- ---------------------------------------------------------------
CREATE TABLE likes (
    user_id  INT NOT NULL REFERENCES users(user_id)  ON DELETE CASCADE,
    photo_id INT NOT NULL REFERENCES photos(photo_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, photo_id)
);


-- =============================================================
--  TRIGGERS
-- =============================================================

-- ---------------------------------------------------------------
-- T1: Prevent a user from commenting on their own photo
-- ---------------------------------------------------------------
CREATE OR REPLACE FUNCTION trg_no_self_comment()
RETURNS TRIGGER AS $$
DECLARE
    v_album_owner INT;
BEGIN
    SELECT u.user_id INTO v_album_owner
    FROM photos p
    JOIN albums a ON p.album_id = a.album_id
    JOIN users  u ON a.owner_id = u.user_id
    WHERE p.photo_id = NEW.photo_id;

    IF NEW.user_id IS NOT NULL AND NEW.user_id = v_album_owner THEN
        RAISE EXCEPTION 'Users cannot comment on their own photos.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_no_self_comment
BEFORE INSERT ON comments
FOR EACH ROW EXECUTE FUNCTION trg_no_self_comment();

-- ---------------------------------------------------------------
-- T2: Prevent a user from liking their own photo
-- ---------------------------------------------------------------
CREATE OR REPLACE FUNCTION trg_no_self_like()
RETURNS TRIGGER AS $$
DECLARE
    v_album_owner INT;
BEGIN
    SELECT u.user_id INTO v_album_owner
    FROM photos p
    JOIN albums a ON p.album_id = a.album_id
    JOIN users  u ON a.owner_id = u.user_id
    WHERE p.photo_id = NEW.photo_id;

    IF NEW.user_id = v_album_owner THEN
        RAISE EXCEPTION 'Users cannot like their own photos.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_no_self_like
BEFORE INSERT ON likes
FOR EACH ROW EXECUTE FUNCTION trg_no_self_like();

-- ---------------------------------------------------------------
-- T3: Prevent duplicate friendship in reverse direction
--     i.e. if (A→B) exists, block (B→A) only if we want
--     strictly one-directional. Remove this trigger if
--     mutual following should be allowed.
-- ---------------------------------------------------------------
-- (Left as optional — one-directional friendships are allowed
--  to be mutual, e.g. A follows B AND B follows A separately.)


-- =============================================================
--  INDEXES  (for query performance)
-- =============================================================
CREATE INDEX idx_albums_owner      ON albums(owner_id);
CREATE INDEX idx_photos_album      ON photos(album_id);
CREATE INDEX idx_comments_photo    ON comments(photo_id);
CREATE INDEX idx_comments_user     ON comments(user_id);
CREATE INDEX idx_photo_tags_tag    ON photo_tags(tag_id);
CREATE INDEX idx_photo_tags_photo  ON photo_tags(photo_id);
CREATE INDEX idx_friends_user      ON friends(user_id);
CREATE INDEX idx_likes_photo       ON likes(photo_id);
