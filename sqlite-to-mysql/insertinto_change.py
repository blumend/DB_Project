#import os
srcpath = "/home/db/Downloads/track_metaa.sql"
src = open(srcpath, 'r')
#destfile = os.path.splitext(srcpath)[0]
destfile = "/home/db/Downloads/track_meta_changed.sql"
dest = open(destfile, 'w+')
insertstr = "INSERT INTO songs(track_id, title, song_id, album_name, artist_id, artist_mbid, artist_name, duration, artist_familiarity, artist_hotttnesss, year, track_7digitalid, shs_perf, shs_work) VALUES"

for line in src:
	if line.startswith("INSERT INTO songs VALUES"):
		temp = line[24:]
		dest.write(insertstr + temp)
	else:
		dest.write(line)

src.close
dest.close