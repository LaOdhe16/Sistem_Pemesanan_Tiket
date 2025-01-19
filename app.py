from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__, template_folder='views')
app.secret_key = "secret_key"

# Konfigurasi koneksi database lokal
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Sesuaikan password Anda
    database="ticket_booking"
)
cursor = conn.cursor()

# Routes
@app.route('/')
def index():
    search = request.args.get('search')  # Ambil parameter pencarian
    if search:
        query = "SELECT * FROM events WHERE title LIKE %s"
        cursor.execute(query, ('%' + search + '%',))
    else:
        cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    return render_template('index.html', events=events)

@app.route('/detail/<int:event_id>')
def detail(event_id):
    cursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
    event = cursor.fetchone()
    return render_template('detail.html', event=event)

@app.route('/book/<int:event_id>', methods=['POST'])
def book(event_id):
    name = request.form['name']
    email = request.form['email']
    cursor.execute("INSERT INTO bookings (event_id, name, email) VALUES (%s, %s, %s)", (event_id, name, email))
    conn.commit()
    flash("Tiket berhasil dipesan!", "success")
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    return render_template('admin.html', events=events)

@app.route('/admin/add', methods=['POST'])
def add_event():
    title = request.form['title']
    date = request.form['date']
    location = request.form['location']
    cursor.execute("INSERT INTO events (title, date, location) VALUES (%s, %s, %s)", (title, date, location))
    conn.commit()
    flash("Acara berhasil ditambahkan!", "success")
    return redirect(url_for('admin'))

@app.route('/admin/delete/<int:event_id>')
def delete_event(event_id):
    cursor.execute("DELETE FROM events WHERE id = %s", (event_id,))
    conn.commit()
    flash("Acara berhasil dihapus!", "success")
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
