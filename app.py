from flask import Flask, request, jsonify
import psycopg2
import redis

app = Flask(__name__)

# PostgreSQL connection settings
DB_HOST = 'db'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
DB_NAME = 'mydb'

# Redis connection settings
REDIS_HOST = 'redis'
REDIS_PORT = 6379

# Create a PostgreSQL connection
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return conn

# Create a Redis connection
def get_redis_connection():
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    return r

@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    conn.close()
    return jsonify(users)

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (data['name'], data['email']))
    conn.commit()
    conn.close()
    return jsonify({"message": "User created successfully"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
