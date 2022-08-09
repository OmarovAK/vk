from connect_to_base import db

db.connect().execute(f'CREATE TABLE IF NOT EXISTS user_vk (user_vk_id integer primary key, '
                     f'name varchar(100), surname varchar(100)); '
                     f'CREATE TABLE IF NOT EXISTS partners (partner_vk_id integer primary key, '
                     f'name varchar(100), surname varchar(100)); '
                     f'CREATE TABLE IF NOT EXISTS user_vk_partners (user_vk_id integer references user_vk(user_vk_id), '
                     f'partner_vk_id integer references partners(partner_vk_id), constraint primary_one primary key (user_vk_id, partner_vk_id)); '
                     )

tuple_tables = db.connect().execute("SELECT table_name FROM information_schema.tables  WHERE table_schem"
                                    "a='public' ORDER BY table_name;").fetchall()

print(tuple_tables)
