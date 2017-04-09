# Musicbrainz100k
random 100k songs from musicbrainz database

These scripts are to get random 100k songs from locally set up musicbrainz database.
This will build a database with 3 tables
Song
SongTag
Tag

Song Table contains auto incremented 'id' and a string 'name'
Tag Table contains auto incremented 'id' and a string 'name'
SongTag Table contains auto incremented 'id' and a int 'song' and int 'tag'

You have to create these tables before running the scripts.
