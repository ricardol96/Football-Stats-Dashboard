from fastapi import FastAPI
import mysql.connector
import os

app = FastAPI()

# MySQL configuration
db_config = {
    'host': os.environ.get('DB_HOST'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'database': 'players'
}

# Function to connect to MySQL and fetch data
def fetch_data_from_mysql():
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Execute the SELECT query
        query = """
                SELECT id,
                    name,
                    position,
                    age,
                    nationality,
                    club,
                    market_value,
                    highest_market_value,
                    value_updated,
                    player_page,
                    league,
                    league_country,
                    response_code,
                    url,
                    updated_on
                FROM players_value;"""
        cursor.execute(query)

        # Fetch all the data
        data = cursor.fetchall()
        row_headers=[x[0] for x in cursor.description]
        # Convert data to a list of dictionaries
        data_list = []
        for row in data:
            data_list.append(dict(zip(row_headers,row)))
        # Close the cursor and the connection
        cursor.close()
        connection.close()

        return data_list

    except mysql.connector.Error as error:
        return f"Error: {error}"

# API endpoint for fetching data from MySQL
@app.get('/data/')
def get_data():
    # Fetch data from MySQL
    data = fetch_data_from_mysql()
    return data
    