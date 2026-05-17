import psycopg2
from psycopg2 import Binary
 
# Mapping: photo_id -> image file path
# Order matches the confirmed mapping:
# Image 1 (19_04_52__1_) -> photo 21 "Friends in costume"
# Image 2 (19_04_52)     -> photo 20 "Carnival parade floats"
# Image 3 (19_04_53__1_) -> photo 23 "Stone bridge of Kipi"
# Image 4 (19_04_53__2_) -> photo 26 "Santorini caldera sunset"
# Image 5 (19_04_53__3_) -> photo 29 "Easter lamb on the spit"
# Image 6 (19_04_53)     -> photo 22 "Vikos gorge overlook"
# Image 7 (19_04_54)     -> photo 30 "Red eggs and tsoureki"
# Image 8 (19_06_32)     -> photo 24 "Group photo at Ladadika"
# Image 9 (19_06_34__1_) -> photo 27 "Sunset from Lycabettus Hill"
# Image 10 (19_06_34)    -> photo 25 "Dancing at the bar"
 
PHOTO_MAP = {
    21: '/mnt/user-data/uploads/WhatsApp_Image_2026-05-16_at_19_04_52__1_.jpeg',
    20: '/mnt/user-data/uploads/WhatsApp_Image_2026-05-16_at_19_04_52.jpeg',
    23: '/mnt/user-data/uploads/WhatsApp_Image_2026-05-16_at_19_04_53__1_.jpeg',
    26: '/mnt/user-data/uploads/WhatsApp_Image_2026-05-16_at_19_04_53__2_.jpeg',
    29: '/mnt/user-data/uploads/WhatsApp_Image_2026-05-16_at_19_04_53__3_.jpeg',
    22: '/mnt/user-data/uploads/WhatsApp_Image_2026-05-16_at_19_04_53.jpeg',
    30: '/mnt/user-data/uploads/WhatsApp_Image_2026-05-16_at_19_04_54.jpeg',
    24: '/mnt/user-data/uploads/WhatsApp_Image_2026-05-16_at_19_06_32.jpeg',
    27: '/mnt/user-data/uploads/WhatsApp_Image_2026-05-16_at_19_06_34__1_.jpeg',
    25: '/mnt/user-data/uploads/WhatsApp_Image_2026-05-16_at_19_06_34.jpeg',
}
 
# ← Change this to your actual postgres username
DB_USER = 'adamshawky'
 
conn = psycopg2.connect(dbname='k29photo', user=DB_USER, host='localhost')
cur = conn.cursor()
 
# 1. Delete photo 28 (Midnight resurrection service)
cur.execute('DELETE FROM photos WHERE photo_id = 28')
print(f'Deleted photo 28 (Midnight resurrection service). Rows affected: {cur.rowcount}')
 
# 2. Update each photo with real image data
for photo_id, filepath in PHOTO_MAP.items():
    with open(filepath, 'rb') as f:
        data = f.read()
    cur.execute('UPDATE photos SET data = %s WHERE photo_id = %s', (Binary(data), photo_id))
    print(f'Updated photo {photo_id} with {filepath.split("/")[-1]} ({len(data)//1024}KB)')
 
conn.commit()
conn.close()
print('\nDone! Refresh your browser to see the real photos.')