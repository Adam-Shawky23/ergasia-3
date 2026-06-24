import psycopg2
from psycopg2 import Binary

# Local DB
local = psycopg2.connect(dbname='k29photo', user='adamshawky', host='localhost')
local_cur = local.cursor()

# Supabase DB (paste your pooler URI)
remote = psycopg2.connect("postgresql://postgres.cjrmikobwqbcowuhiuse:rankIp-cisrot-1tudjy@aws-0-eu-west-1.pooler.supabase.com:6543/postgres")
remote_cur = remote.cursor()

# Fetch all photos with data from local
local_cur.execute("SELECT photo_id, data FROM photos WHERE data IS NOT NULL")
photos = local_cur.fetchall()

print(f"Found {len(photos)} photos with image data")

for photo_id, data in photos:
    if data:
        remote_cur.execute(
            "UPDATE photos SET data = %s WHERE photo_id = %s",
            (Binary(bytes(data)), photo_id)
        )
        print(f"✓ Updated photo {photo_id} ({len(bytes(data))//1024}KB)")

remote.commit()
remote.close()
local.close()
print("Done!")