import sqlite3
con = sqlite3.connect("s.db")
cur=con.cursor()
#cur.execute("CREATE TABLE movie(title,year)")
#cur.execute("DROP TABLE movie")
cur.execute("""INSERT INTO movie VALUES('MONTH', 'ER')""")
