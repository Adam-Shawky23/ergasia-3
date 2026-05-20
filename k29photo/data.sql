-- =============================================================
--  k29photo — Sample Data
--  Course: K29 Database Design and Use, Spring 2026
-- =============================================================
--  Passwords are bcrypt hashes of the plaintext shown in comments.
--  For testing I use plaintext: password123 for all users.
-- =============================================================


-- ---------------------------------------------------------------
-- 1. USERS  (12 users)
-- ---------------------------------------------------------------
INSERT INTO users (first_name, last_name, email, dob, hometown, gender, password) VALUES
('Nikos',      'Papadopoulos', 'nikos.p@gmail.com',     '1995-03-12', 'Athens',       'M', '$2b$12$KIXiRqCvBPMBtnZGVe7eZOqJYCVLWiADhKn7M3HXGz5A3s1FQDO6i'),
('Maria',      'Georgiou',     'maria.g@gmail.com',     '1998-07-24', 'Thessaloniki', 'F', '$2b$12$KIXiRqCvBPMBtnZGVe7eZOqJYCVLWiADhKn7M3HXGz5A3s1FQDO6i'),
('Kostas',     'Alexiou',      'kostas.a@gmail.com',    '1993-11-05', 'Patras',       'M', '$2b$12$KIXiRqCvBPMBtnZGVe7eZOqJYCVLWiADhKn7M3HXGz5A3s1FQDO6i'),
('Elena',      'Stavrou',      'elena.s@gmail.com',     '2000-01-30', 'Heraklion',    'F', '$2b$12$KIXiRqCvBPMBtnZGVe7eZOqJYCVLWiADhKn7M3HXGz5A3s1FQDO6i'),
('Dimitris',   'Katsaros',     'dimitris.k@gmail.com',  '1997-06-18', 'Nafplion',     'M', '$2b$12$KIXiRqCvBPMBtnZGVe7eZOqJYCVLWiADhKn7M3HXGz5A3s1FQDO6i'),
('Sofia',      'Nikolaou',     'sofia.n@gmail.com',     '1999-09-09', 'Volos',        'F', '$2b$12$KIXiRqCvBPMBtnZGVe7eZOqJYCVLWiADhKn7M3HXGz5A3s1FQDO6i'),
('Giorgos',    'Papadakis',    'giorgos.pp@gmail.com',  '1994-04-22', 'Rhodes',       'M', '$2b$12$KIXiRqCvBPMBtnZGVe7eZOqJYCVLWiADhKn7M3HXGz5A3s1FQDO6i'),
('Anna',       'Tsirou',       'anna.t@gmail.com',      '2001-12-03', 'Corfu',        'F', '$2b$12$KIXiRqCvBPMBtnZGVe7eZOqJYCVLWiADhKn7M3HXGz5A3s1FQDO6i'),
('Petros',     'Manolis',      'petros.m@gmail.com',    '1992-08-15', 'Larissa',      'M', '$2b$12$KIXiRqCvBPMBtnZGVe7eZOqJYCVLWiADhKn7M3HXGz5A3s1FQDO6i'),
('Ioanna',     'Lamprou',      'ioanna.l@gmail.com',    '1996-02-27', 'Ioannina',     'F', '$2b$12$KIXiRqCvBPMBtnZGVe7eZOqJYCVLWiADhKn7M3HXGz5A3s1FQDO6i'),
('Christos',   'Vasileiou',    'christos.v@gmail.com',  '1990-05-11', 'Kavala',       'M', '$2b$12$KIXiRqCvBPMBtnZGVe7eZOqJYCVLWiADhKn7M3HXGz5A3s1FQDO6i'),
('Katerina',   'Dimou',        'katerina.d@gmail.com',  '2002-10-08', 'Sparta',       'F', '$2b$12$KIXiRqCvBPMBtnZGVe7eZOqJYCVLWiADhKn7M3HXGz5A3s1FQDO6i');
-- user_id: 1=Nikos 2=Maria 3=Kostas 4=Elena 5=Dimitris 6=Sofia
--          7=Giorgos 8=Anna 9=Petros 10=Ioanna 11=Christos 12=Katerina


-- ---------------------------------------------------------------
-- 2. ALBUMS  (16 albums spread across users)
-- ---------------------------------------------------------------
INSERT INTO albums (name, owner_id, creation_date) VALUES
('Summer in Nafplion',      1,  '2024-07-10'),  -- album_id 1
('Athens Street Art',       1,  '2024-09-05'),  -- album_id 2
('Thessaloniki Food Tour',  2,  '2024-08-20'),  -- album_id 3
('Mountain Hike Olympus',   3,  '2024-06-15'),  -- album_id 4
('Crete Road Trip',         4,  '2024-10-01'),  -- album_id 5
('Nafplion Old Town',       5,  '2024-07-22'),  -- album_id 6
('Volos by the Sea',        6,  '2024-08-11'),  -- album_id 7
('Rhodes Medieval City',    7,  '2024-09-18'),  -- album_id 8
('Corfu Beaches',           8,  '2024-07-30'),  -- album_id 9
('Larissa Carnival',        9,  '2025-02-28'),  -- album_id 10
('Zagori Villages',        10,  '2024-10-14'),  -- album_id 11
('Kavala Harbour',         11,  '2024-08-03'),  -- album_id 12
('Sparta Ruins',           12,  '2024-11-20'),  -- album_id 13
('Friends Night Out',       2,  '2025-01-15'),  -- album_id 14
('Sunset Collection',       6,  '2025-03-02'),  -- album_id 15
('Greek Easter',            9,  '2025-04-20');  -- album_id 16


-- ---------------------------------------------------------------
-- 3. PHOTOS  (30 photos — data is a small placeholder PNG in hex)
--    In production the Flask app inserts real binary data.
-- ---------------------------------------------------------------

INSERT INTO photos (album_id, caption, data) VALUES
-- Album 1: Summer in Nafplion (photos 1-3)
(1,  'Bourtzi fortress at golden hour',         '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
(1,  'Palamidi steps at sunrise',               '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
(1,  'Little harbour with fishing boats',       '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
-- Album 2: Athens Street Art (photos 4-5)
(2,  'Exarcheia mural — colour explosion',      '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
(2,  'Monastiraki graffiti alley',              '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
-- Album 3: Thessaloniki Food Tour (photos 6-7)
(3,  'Bougatsa from Bantis',                    '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
(3,  'Seafood platter at the White Tower',      '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
-- Album 4: Mountain Hike Olympus (photos 8-9)
(4,  'Summit of Mytikas in the clouds',         '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
(4,  'Trail through the pine forest',           '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
-- Album 5: Crete Road Trip (photos 10-11)
(5,  'Balos lagoon turquoise waters',           '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
(5,  'Knossos palace ruins',                    '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
-- Album 6: Nafplion Old Town (photos 12-13)
(6,  'Syntagma square at night',                '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
(6,  'Colourful neoclassical facades',          '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
-- Album 7: Volos by the Sea (photos 14-15)
(7,  'Tsipouradiko on the waterfront',          '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
(7,  'Pagasetic Gulf at dusk',                  '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
-- Album 8: Rhodes Medieval City (photos 16-17)
(8,  'Street of the Knights',                   '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
(8,  'Palace of the Grand Master',              '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
-- Album 9: Corfu Beaches (photos 18-19)
(9,  'Paleokastritsa beach crystal clear',      '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
(9,  'Sunset at Canal d''Amour',                '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
-- Album 10: Larissa Carnival (photos 20-21)
(10, 'Carnival parade floats',                  '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
(10, 'Friends in costume',                      '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
-- Album 11: Zagori Villages (photos 22-23)
(11, 'Vikos gorge overlook',                    '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
(11, 'Stone bridge of Kipi',                    '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
-- Album 14: Friends Night Out (photos 24-25)
(14, 'Group photo at Ladadika',                 '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
(14, 'Dancing at the bar',                      '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
-- Album 15: Sunset Collection (photos 26-27)
(15, 'Santorini caldera sunset',                '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
(15, 'Sunset from Lycabettus Hill Athens',      '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
-- Album 16: Greek Easter (photos 28-30)
(16, 'Midnight resurrection service',           '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
(16, 'Easter lamb on the spit',                 '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea),
(16, 'Red eggs and tsoureki',                   '\x89504e470d0a1a0a0000000d4948445200000001000000010800000000'::bytea);
-- photo_id 1..30 in insertion order


-- ---------------------------------------------------------------
-- 4. TAGS  (20 tags)
-- ---------------------------------------------------------------
INSERT INTO tags (tag_name) VALUES
('nafplion'),     -- 1
('sea'),          -- 2
('sunset'),       -- 3
('friends'),      -- 4
('nature'),       -- 5
('history'),      -- 6
('food'),         -- 7
('travel'),       -- 8
('greece'),       -- 9
('beach'),        -- 10
('mountains'),    -- 11
('nightlife'),    -- 12
('architecture'), -- 13
('streetart'),    -- 14
('island'),       -- 15
('easter'),       -- 16
('carnival'),     -- 17
('village'),      -- 18
('harbour'),      -- 19
('athens');       -- 20


-- ---------------------------------------------------------------
-- 5. PHOTO_TAGS  (rich tagging to test all queries)
-- ---------------------------------------------------------------
INSERT INTO photo_tags (photo_id, tag_id) VALUES
-- photo 1: Bourtzi fortress
(1,  1), (1,  2), (1,  3), (1,  9),
-- photo 2: Palamidi steps
(2,  1), (2,  6), (2,  9), (2, 13),
-- photo 3: Little harbour
(3,  1), (3,  2), (3, 19), (3,  9),
-- photo 4: Exarcheia mural
(4, 14), (4, 20), (4,  9),
-- photo 5: Monastiraki graffiti
(5, 14), (5, 20), (5, 13),
-- photo 6: Bougatsa
(6,  7), (6,  9),
-- photo 7: Seafood platter
(7,  7), (7,  2), (7,  9),
-- photo 8: Summit Mytikas
(8, 11), (8,  5), (8,  9),
-- photo 9: Pine forest trail
(9, 11), (9,  5), (9,  8),
-- photo 10: Balos lagoon
(10, 10), (10,  2), (10, 15), (10,  9),
-- photo 11: Knossos ruins
(11,  6), (11, 13), (11,  9), (11,  8),
-- photo 12: Syntagma square night
(12,  1), (12, 13), (12,  9), (12, 12),
-- photo 13: Neoclassical facades
(13,  1), (13, 13), (13,  9),
-- photo 14: Tsipouradiko
(14,  7), (14,  2), (14,  4),
-- photo 15: Pagasetic Gulf dusk
(15,  2), (15,  3), (15,  9),
-- photo 16: Street of the Knights
(16,  6), (16, 13), (16,  9), (16,  8),
-- photo 17: Palace Grand Master
(17,  6), (17, 13), (17, 15),
-- photo 18: Paleokastritsa beach
(18, 10), (18,  2), (18, 15), (18,  9),
-- photo 19: Canal d'Amour sunset
(19,  3), (19, 10), (19, 15),
-- photo 20: Carnival parade
(20, 17), (20,  4), (20,  9),
-- photo 21: Friends in costume
(21, 17), (21,  4), (21, 12),
-- photo 22: Vikos gorge
(22,  5), (22, 11), (22,  8), (22, 18),
-- photo 23: Stone bridge Kipi
(23,  5), (23, 18), (23,  9), (23,  6),
-- photo 24: Group photo Ladadika
(24,  4), (24, 12), (24,  9),
-- photo 25: Dancing at the bar
(25,  4), (25, 12),
-- photo 26: Santorini sunset
(26,  3), (26, 15), (26,  2), (26,  9),
-- photo 27: Lycabettus sunset
(27,  3), (27, 20), (27,  9),
-- photo 28: Midnight resurrection
(28, 16), (28,  9),
-- photo 29: Easter lamb
(29, 16), (29,  7), (29,  4),
-- photo 30: Red eggs tsoureki
(30, 16), (30,  7), (30,  9);


-- ---------------------------------------------------------------
-- 6. FRIENDS  (directional follows — enough to test friend-of-friend)
-- ---------------------------------------------------------------
INSERT INTO friends (user_id, friend_id) VALUES
(1, 2), (1, 3), (1, 5),
(2, 1), (2, 4), (2, 6),
(3, 1), (3, 7), (3, 9),
(4, 2), (4, 8), (4, 10),
(5, 1), (5, 6), (5, 11),
(6, 2), (6, 5), (6, 12),
(7, 3), (7, 8),
(8, 4), (8, 7), (8, 9),
(9, 3), (9, 8), (9, 10),
(10,4), (10,9),
(11,5), (11,12),
(12,6), (12,11);


-- ---------------------------------------------------------------
-- 7. COMMENTS  (mix of registered users and guests)
--    Rule: users cannot comment on their own photos.
--    photo owner lookup:
--      photos 1-3  → album 1  → user 1 (Nikos)
--      photos 4-5  → album 2  → user 1 (Nikos)
--      photos 6-7  → album 3  → user 2 (Maria)
--      photos 8-9  → album 4  → user 3 (Kostas)
--      photos 10-11→ album 5  → user 4 (Elena)
--      photos 12-13→ album 6  → user 5 (Dimitris)
--      photos 14-15→ album 7  → user 6 (Sofia)
--      photos 16-17→ album 8  → user 7 (Giorgos)
--      photos 18-19→ album 9  → user 8 (Anna)
--      photos 20-21→ album 10 → user 9 (Petros)
--      photos 22-23→ album 11 → user 10 (Ioanna)
--      photos 24-25→ album 14 → user 2 (Maria)
--      photos 26-27→ album 15 → user 6 (Sofia)
--      photos 28-30→ album 16 → user 9 (Petros)
-- ---------------------------------------------------------------
INSERT INTO comments (photo_id, user_id, guest_name, content, post_date) VALUES
-- on Nikos's photos (user 1) — other users comment
(1,  2,  NULL, 'What a stunning view of Bourtzi!',           '2024-07-12'),
(1,  3,  NULL, 'I love Nafplion so much.',                   '2024-07-13'),
(1,  5,  NULL, 'My hometown! Great shot.',                   '2024-07-14'),
(2,  4,  NULL, 'Those steps look exhausting but worth it.',  '2024-07-15'),
(2,  6,  NULL, 'Beautiful light in this photo.',             '2024-07-16'),
(3,  7,  NULL, 'Looks so peaceful.',                         '2024-07-17'),
-- guest comments on Nikos's photos
(1,  NULL, 'Visitor123', 'Amazing place!',                   '2024-07-18'),
(4,  NULL, 'TravelFan',  'Love the street art scene.',       '2024-09-06'),
-- on Maria's photos (user 2)
(6,  1,  NULL, 'Now I am hungry!',                           '2024-08-21'),
(6,  3,  NULL, 'Bougatsa is the best breakfast.',            '2024-08-22'),
(7,  5,  NULL, 'Perfect seafood platter.',                   '2024-08-23'),
(7,  9,  NULL, 'The White Tower view is iconic.',            '2024-08-24'),
-- on Kostas's photos (user 3)
(8,  1,  NULL, 'Top of Greece! Amazing.',                    '2024-06-16'),
(8,  2,  NULL, 'I want to climb Olympus one day.',           '2024-06-17'),
(9,  4,  NULL, 'The forest trail looks magical.',            '2024-06-18'),
-- on Elena's photos (user 4)
(10, 2,  NULL, 'Balos is unreal!',                           '2024-10-02'),
(10, 6,  NULL, 'That water colour!',                         '2024-10-03'),
(11, 3,  NULL, 'History lovers dream.',                      '2024-10-04'),
-- on Dimitris's photos (user 5)
(12, 1,  NULL, 'Nafplion by night is magical.',              '2024-07-23'),
(13, 2,  NULL, 'Such pretty buildings.',                     '2024-07-24'),
-- on Sofia's photos (user 6)
(14, 1,  NULL, 'Great tsipouradiko choice!',                 '2024-08-12'),
(15, 3,  NULL, 'Gorgeous dusk colours.',                     '2024-08-13'),
(15, 4,  NULL, 'Perfect sunset shot.',                       '2024-08-14'),
-- on Giorgos's photos (user 7)
(16, 1,  NULL, 'Rhodes is on my bucket list.',               '2024-09-19'),
(17, 2,  NULL, 'So much history in one place.',              '2024-09-20'),
-- on Anna's photos (user 8)
(18, 1,  NULL, 'Corfu beaches are paradise.',                '2024-07-31'),
(19, 3,  NULL, 'Perfect sunset timing.',                     '2024-08-01'),
(18, NULL, 'BeachLover', 'Crystal clear water!',             '2024-08-02'),
-- on Petros's photos (user 9)
(20, 1,  NULL, 'What a float!',                              '2025-03-01'),
(21, 2,  NULL, 'Love the costumes.',                         '2025-03-02'),
-- on Ioanna's photos (user 10)
(22, 1,  NULL, 'Vikos gorge is breathtaking.',               '2024-10-15'),
(23, 2,  NULL, 'That bridge is so picturesque.',             '2024-10-16'),
-- on Maria's album 14 photos (user 2)
(24, 1,  NULL, 'Looks like an amazing night!',               '2025-01-16'),
(25, 3,  NULL, 'Best night out ever.',                       '2025-01-17'),
(24, NULL, 'NightOwl99', 'Great vibes at Ladadika!',         '2025-01-18'),
-- on Sofia's sunset collection (user 6)
(26, 1,  NULL, 'Santorini sunsets are unmatched.',           '2025-03-03'),
(27, 2,  NULL, 'Athens is so underrated.',                   '2025-03-04'),
-- on Petros's Easter album (user 9)
(28, 1,  NULL, 'Such a special atmosphere.',                 '2025-04-21'),
(29, 2,  NULL, 'Easter lamb looks incredible.',              '2025-04-22'),
(30, 4,  NULL, 'Traditional and beautiful.',                 '2025-04-23');


-- ---------------------------------------------------------------
-- 8. LIKES
--    Users cannot like their own photos (trigger enforces this).
-- ---------------------------------------------------------------
INSERT INTO likes (user_id, photo_id) VALUES
-- likes on photo 1 (owner: Nikos=1)
(2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1),
-- likes on photo 2 (owner: Nikos=1)
(2, 2), (4, 2), (6, 2),
-- likes on photo 3 (owner: Nikos=1)
(3, 3), (5, 3),
-- likes on photo 8 (owner: Kostas=3)
(1, 8), (2, 8), (4, 8), (5, 8),
-- likes on photo 10 (owner: Elena=4)
(1, 10), (2, 10), (6, 10), (7, 10), (8, 10),
-- likes on photo 18 (owner: Anna=8)
(1, 18), (2, 18), (3, 18), (5, 18),
-- likes on photo 22 (owner: Ioanna=10)
(1, 22), (2, 22), (3, 22),
-- likes on photo 26 (owner: Sofia=6)
(1, 26), (2, 26), (3, 26), (4, 26), (5, 26), (7, 26), (9, 26),
-- likes on photo 27 (owner: Sofia=6)
(1, 27), (2, 27), (3, 27),
-- likes on photo 12 (owner: Dimitris=5)
(1, 12), (2, 12), (3, 12), (4, 12),
-- likes on photo 19 (owner: Anna=8)
(1, 19), (3, 19), (6, 19),
-- likes on photo 6 (owner: Maria=2)
(1, 6), (3, 6), (5, 6),
-- likes on photo 7 (owner: Maria=2)
(1, 7), (4, 7), (9, 7),
-- likes on photo 29 (owner: Petros=9)
(1, 29), (2, 29), (4, 29), (6, 29);

