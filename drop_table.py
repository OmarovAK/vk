from connect_to_base import db

tuple_tables = db.connect().execute("SELECT table_name FROM information_schema.tables  WHERE table_schem"
                                      "a='public' ORDER BY table_name;").fetchall()

str_tables = str()
count = 1
for i in tuple_tables:
    for k in i:
        str_tables = str_tables + ', ' + str(k)
        if count == 1:
            str_tables = str_tables[2:]
        count = count + 1

db.connect().execute(f"DROP TABLE {str_tables};")
