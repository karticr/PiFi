import sqlite3 as lite
con = lite.connect('dataControl.db')
with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM pifi")
    data =  cur.fetchall()
    print(data[1][0])
