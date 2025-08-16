from flask import Flask, render_template, request, redirect, session, url_for, flash
from auth import auth_bp
from database import init_db, get_db_connection
import chatbot
import webbrowser
import threading
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace this with a strong key
app.register_blueprint(auth_bp)

# Initialize database
init_db()

@app.route('/')
def home():
    return redirect(url_for('auth.login'))

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'user_id' not in session or session.get('is_admin'):
        return redirect(url_for('auth.login'))

    response = ""
    conn = get_db_connection()

    if request.method == 'POST':
        user_message = request.form['message']
        response = chatbot.generate_response(user_message)

        # Save chat to DB
        conn.execute("INSERT INTO chats (user_id, message, response) VALUES (?, ?, ?)",
                     (session['user_id'], user_message, response))
        conn.commit()

    # Get username for both GET and POST
    user = conn.execute("SELECT username FROM users WHERE id = ?", (session['user_id'],)).fetchone()
    username = user['username'] if user else "User"
    conn.close()

    return render_template('chat.html', response=response, username=username)

@app.route('/admin')
def admin_dashboard():
    if not session.get('is_admin'):
        return redirect(url_for('auth.login'))
    return render_template('admin_dashboard.html')

@app.route('/admin/users')
def admin_users():
    if not session.get('is_admin'):
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    users = conn.execute("SELECT id, username, is_admin FROM users").fetchall()
    conn.close()
    return render_template('admin_users.html', users=users)

@app.route('/admin/chats')
def admin_chats():
    if not session.get('is_admin'):
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    chats = conn.execute('''
        SELECT chats.id, users.username, chats.message, chats.response, chats.timestamp
        FROM chats JOIN users ON chats.user_id = users.id
        ORDER BY chats.timestamp DESC
    ''').fetchall()
    conn.close()
    return render_template('admin_chats.html', chats=chats)

def open_browser():
    time.sleep(1)  # Wait a moment for the server to start
    webbrowser.open("http://127.0.0.1:5000/")

if __name__ == '__main__':
    threading.Thread(target=open_browser).start()
    app.run(debug=True)
