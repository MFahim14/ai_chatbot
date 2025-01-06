import psycopg2
from psycopg2.extras import execute_values
from database.db_config import DBConfig

class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        self.connection = psycopg2.connect(
            host=DBConfig.HOST,
            port=DBConfig.PORT,
            database=DBConfig.NAME,
            user=DBConfig.USER,
            password=DBConfig.PASSWORD
        )

    def create_tables(self):
        with self.connection.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS user_comments (
                    id SERIAL PRIMARY KEY,
                    user_name VARCHAR(255),
                    comment_date TIMESTAMP,
                    comment_text TEXT,
                    rental_id INT
                );

                CREATE TABLE IF NOT EXISTS rentals (
                    id SERIAL PRIMARY KEY,
                    rental_id INT,
                    driver_name VARCHAR(255),
                    car_details VARCHAR(255),
                    license_plate VARCHAR(20),
                    rental_dates TEXT[]
                );
            """)
            self.connection.commit()

    def insert_comment(self, comment):
        with self.connection.cursor() as cur:
            cur.execute("""
                INSERT INTO user_comments (user_name, comment_date, comment_text, rental_id)
                VALUES (%s, %s, %s, %s)
            """, (comment['userName'], comment['commentDate'], comment['commentText'], comment['rental_id']))
            self.connection.commit()

    def insert_rental(self, rental):
        rental_id = int(rental['href'].split('/')[-1])
        with self.connection.cursor() as cur:
            cur.execute("""
                INSERT INTO rentals (rental_id, driver_name, car_details, license_plate, rental_dates)
                VALUES (%s, %s, %s, %s, %s)
            """, (rental_id, rental['driverName'], rental['carDetails'], rental['licensePlate'], rental['rentalDates']))
            self.connection.commit()

    def close(self):
        if self.connection:
            self.connection.close()