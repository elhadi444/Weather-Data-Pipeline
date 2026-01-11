from api_requests import fetch_weather_data, mock_fetch_weather_data
import psycopg2

def connect_to_db():
    print ("Connecting to the database...")
    try:
        conn = psycopg2.connect(
            host="db",
            port="5432",
            dbname="db",
            user="db_user",
            password="db_password"
        )
        return conn
    except psycopg2.Error as e:
        print(f"error connecting to database: {e}")
        raise

def create_table(conn):
    print("creating table if not exists...")
    try:
        conn.cursor().execute("""
            CREATE SCHEMA IF NOT EXISTS dev;
            CREATE TABLE IF NOT EXISTS dev.row_weather_data (
                id SERIAL PRIMARY KEY,
                city TEXT,
                temperature FLOAT,
                weather_desc TEXT,
                wind_speed FLOAT,
                time TIMESTAMP,
                inserted_at TIMESTAMP DEFAULT NOW(),
                utc_offset TEXT
            );
        """)
        conn.commit()
        print("table created.")
    except psycopg2.Error as e:
        print(f"error creating table: {e}")
        raise

def insert_records(conn, data):
    print("inserting weather data...")
    try:
        weather = data['current']
        location = data['location']
        conn.cursor().execute("""
            INSERT INTO dev.row_weather_data (
                city,
                temperature,
                weather_desc,
                wind_speed,
                time,
                inserted_at,
                utc_offset
            ) VALUES (%s, %s, %s, %s, %s, NOW(), %s)

        """, (
            location['name'],
            weather['temperature'],
            weather['weather_descriptions'][0],
            weather['wind_speed'],
            location['localtime'],
            location['utc_offset']
        ))
        conn.commit()
        print('data successfully inserted')
    except psycopg2.Error as e:
        print(f"error inserting data: {e}")
        raise

def main():
    try:
        data = fetch_weather_data()
        conn = connect_to_db()
        create_table(conn)
        insert_records(conn, data)
    except Exception as e:
        print(f"an error occurred in the main: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("database connection closed")

