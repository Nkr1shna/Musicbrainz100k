import psycopg2
import random
import MySQLdb

conn = psycopg2.connect("dbname='musicbrainz' user='musicbrainz' host='localhost' password='musicbrainz'")
conn1 = MySQLdb.connect(host = "localhost", user = "root", passwd = "40OZlike", db = "plalyst")
print("connections and cursors made...")
cur= conn1.cursor()
conn1.set_character_set('utf8')
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')
cur.close()

def migrateSongDB():
    try:
        cur1 = conn1.cursor()
        cur1.execute("select count(*) from Song")
        numberOfSongs = cur1.fetchall()[0][0]
        cur1.close()
        print("number of songs in our database is ")
        print(numberOfSongs)
        rnumbers = random.sample(range(1, 22660511), 100000-numberOfSongs)
        print("random numbers generated....")
        for eachnum in rnumbers:
            cur = conn.cursor()
            cur1 = conn1.cursor()
            print(eachnum)
            songName=""
            while(songName==""):
                cur.execute("""select name from track where id = %s """, (eachnum,))
                rows = cur.fetchall()
                print(rows)
                if not len(rows)==0:
                    songName = rows[0][0]
                eachnum+=1
            print("Got the track name:")
            print(songName)
            sql = 'INSERT into Song (name) values ( "'+songName+'")'
            print(sql)
            cur1.execute(sql)
            cur1.execute('commit')
            print("inserted into the song table....")
            cur.close()
            cur1.close()

        print("Songs Saved into new Data Base...")
        conn.close()
        conn1.close()
        print("Connections Closed")
    except:
        with conn1 as cursor:
            cursor.execute('select 1;')
            result = cursor.fetchall()
            for cur in result:
                print(cur)
        migrateSongDB()

def main():
    migrateSongDB()
    conn.close()
    conn1.close()

if __name__ == "__main__": main()
