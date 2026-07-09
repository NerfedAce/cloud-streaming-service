import psycopg
import os
from dotenv import load_dotenv

load_dotenv()


host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
dbname = os.getenv("DB_NAME")
port = os.getenv("DB_PORT")

# db  ----> id , title , url ,img , length , user_id


def get_data_by_user(user: str):
    try:
        conn = psycopg.connect(
            host=host,
            user=db_user,
            password=password,
            dbname=dbname,
            port=port
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM videos WHERE user_id = %s", (user,))
        rows = cursor.fetchall()
        res =[]
        print(rows)
        for row in rows:
            res.append({"id": row[0], "title": row[1], "url": row[2],"img": row[3] ,"length": row[4]})
        conn.close()
        return res

    except psycopg.OperationalError:
        print("exception")
        return []

def get_data_by_id(id: int):
    try:
        conn = psycopg.connect(
            host=host,
            user=db_user,
            password=password,
            dbname=dbname,
            port=port
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM videos WHERE id = %s", (id,))
        row = cursor.fetchone()
        res = {"id": row[0], "title": row[1], "url": row[2], "img": row[3], "length": row[4]}
        conn.close()
        return res

    except psycopg.OperationalError:
        return []

def add_data( title, url, img, length, user):
    try:
        with psycopg.connect(
            host=host,
            user=db_user,
            password=password,
            dbname=dbname,
            port=port,
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO videos
                    ( title, url, img, length, user_id)
                    VALUES ( %s, %s, %s, %s, %s)
                    """,
                    ( title, url, img, length, user),
                )
            conn.commit()
        return True

    except psycopg.Error as e:
        print(e)
        return False






    
    
