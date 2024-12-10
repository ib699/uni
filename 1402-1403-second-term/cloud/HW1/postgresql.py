import psycopg2
from dotenv import load_dotenv
import os


class Postgresql():
    def __init__(self):
        load_dotenv()

        self.POSTGRESQL_USER = os.getenv('POSTGRESQL_USER')
        self.POSTGRESQL_PASS = os.getenv('POSTGRESQL_PASS')
        self.POSTGRESQL_HOST = os.getenv('POSTGRESQL_HOST')
        self.POSTGRESQL_PORT = os.getenv('POSTGRESQL_PORT')
        self.DATABASE_NAME = os.getenv('DATABASE_NAME')
        self.TABLE_NAME = os.getenv('TABLE_NAME')

        try:
            self.conn = psycopg2.connect(database=self.DATABASE_NAME, user=self.POSTGRESQL_USER, password=self.POSTGRESQL_PASS,
                                    host=self.POSTGRESQL_HOST, port=self.POSTGRESQL_PORT)
            print("Database Connected!")
            self.cur = self.conn.cursor()
            self.make_table()
        except Exception as e:
            print(f"error connecting to db {e}")

    def make_table(self):
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (id SERIAL PRIMARY KEY, email VARCHAR, status VARCHAR, songid VARCHAR);")
        self.conn.commit()
        print("Exit from make table")

    def insert_new_client(self, email, status):
        self.cur.execute(f"INSERT INTO {self.TABLE_NAME} (email, status) VALUES (%s, %s) RETURNING id;", (email, status))
        self.conn.commit()
        new_record_id = self.cur.fetchone()[0]
        return new_record_id

    def update_client_state(self, id, status):
        self.cur.execute(f"UPDATE {self.TABLE_NAME} SET status = %s WHERE id = %s;", (status, id))
        self.conn.commit()

    def update_client_song_id(self, id, songid):
        self.cur.execute(f"UPDATE {self.TABLE_NAME} SET songid = %s WHERE id = %s;", (songid, id))
        self.conn.commit()

    def get_clients_ready(self):
        self.cur.execute(f"SELECT * FROM {self.TABLE_NAME} WHERE status = 'Ready';")
        return self.cur.fetchall()
    
    def get_all(self):
        self.cur.execute(f"SELECT * FROM {self.TABLE_NAME};")
        return self.cur.fetchall()

    def remove_all_finished(self):
        self.cur.execute(f"DELETE FROM %s WHERE status = 'Done';", (self.TABLE_NAME))


if __name__ == "__main__":
    db = Postgresql()
    print(db.get_all())
