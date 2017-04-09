import psycopg2
import random
import MySQLdb

conn = psycopg2.connect("dbname='musicbrainz' user='musicbrainz' host='localhost' password='musicbrainz'")
conn1 = MySQLdb.connect(host = "localhost", user = "root", passwd = "40OZlike", db = "plalyst")
cur= conn1.cursor()
conn1.set_character_set('utf8')
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')
cur.close()
cur1 = conn1.cursor()
print("connections and cursors made...")
cur1.execute("select name from Song order by id desc")
result = cur1.fetchall()
result = [item for sublist in result for item in sublist]
cur1.close()
def migrateSongDB(result):
    try:
        cur=conn.cursor()
        cur1 = conn1.cursor()
        print("Yei..")
        for eachsong in result:
            print("The song name :"+eachsong)
            cur1.execute('select id from Song where name="'+eachsong+'"')
            songId =cur1.fetchall()[0][0]
            cur.execute("""select t.name from track tr
                join recording r
                on tr.recording = r.id
                join recording_tag rt
                on rt.recording = r.id
                join tag t
                on
                rt.tag= t.id
                where tr.name = %s
                order by t.name""", (eachsong,))
            tags = cur.fetchall()
            print(tags)
            for tag in tags:
                sql = 'Select id from Tag where name = ( "'+tag[0]+'")'
                cur1.execute(sql)
                tagId = cur1.fetchall()
                if(not tagId):
                    print("Tag Not Present..")
                    sql = 'INSERT into Tag (name) values ( "'+tag[0]+'")'
                    cur1.execute(sql)
                    print("Tag Inserted..")
                    cur1.execute('commit')
                    cur1.execute('SELECT id from Tag where name = "'+tag[0]+'"')
                    tagId = cur1.fetchall()[0][0]
                else:
                    tagId = tagId[0][0]
                print(songId)
                print(tagId)
                sql = 'INSERT into SongTag (song,tag) values ( '+str(songId)+','+str(tagId)+')'
                cur1.execute(sql)
                print("inserted into SongTag..")

    except:
        print(e)
        cur1.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cur1.execute("Truncate table Song")
        cur1.execute("Truncate table Tag")
        cur1.execute("Truncate table SongTag")
        cur1.execute("SET FOREIGN_KEY_CHECKS = 1;")
        with conn1 as cursor:
            cursor.execute('select 1;')
            result = cursor.fetchall()
            for cur in result:
                print(cur)
        #migrateSongDB()

def main():
    migrateSongDB(result)
    conn.close()
    conn1.close()

if __name__ == "__main__": main()
