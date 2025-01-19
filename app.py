from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__, template_folder='views')

# Koneksi ke database
def get_db_connection():
    hostname = "85bq3.h.filess.io"
    database = "pesantiket_readbandis"
    port = "3306"
    username = "pesantiket_readbandis"
    password = "4e91b84ea24ea854125e8ca69180250fff7dffe4"

    try:
        connection = mysql.connector.connect(
            host=hostname,
            database=database,
            user=username,
            password=password,
            port=port
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

# Route utama index
@app.route('/')
def index():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM events")
        events = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('index.html', events=events)
    else:
        return "Error connecting to database"

# Detail acara
@app.route('/event/<int:event_id>')
def event_detail(event_id):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM events WHERE event_id = %s", (event_id,))
        event = cursor.fetchone()
        cursor.close()
        connection.close()
        return render_template('detail.html', event=event)
    else:
        return "Error connecting to database"

# Route untuk pemesanan tiket
@app.route('/book_ticket/<int:event_id>', methods=['GET', 'POST'])
def book_ticket(event_id):
    if request.method == 'POST':
        user_name = request.form['user_name']
        user_email = request.form['user_email']
        ticket_count = request.form['ticket_count']
        
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO booking (event_id, user_name, user_email, ticket_count, status) VALUES (%s, %s, %s, %s, %s)",
                           (event_id, user_name, user_email, ticket_count, 'Booked'))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('index'))
    return render_template('book_ticket.html', event_id=event_id)

# Route admin untuk menambahkan acara
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        event_time = request.form['event_time']
        event_location = request.form['event_location']
        available_tickets = request.form['available_tickets']
        event_description = request.form['event_description']

        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO events (event_name, event_date, event_time, event_location, available_tickets, event_description)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (event_name, event_date, event_time, event_location, available_tickets, event_description))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('admin'))

    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)
