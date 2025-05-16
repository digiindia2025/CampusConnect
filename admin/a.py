from flask import Flask, render_template, request, flash, redirect, session, url_for
from flask_mysqldb import MySQL

# Initialize the Flask application
app = Flask(__name__)

# Database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Bau#80021'
app.config['MYSQL_DB'] = 'admin_db'

# Secret key for session management
app.secret_key = 'secret_key'

# Initialize MySQL connection
mysql = MySQL(app)

# Route for login (redirecting to dashboard)


# Login route (handles POST and GET requests)
@app.route('/admin/', methods=['GET', 'POST'])
def adminIndex():
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
        
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, username=%s AND password=%s", (email, password))
    user = cursor.fetchone()

    if user:
            # Storing username in session for dashboard access
            session['admin'] = user['username']
            return redirect(url_for('Index'))
    else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('Index.html')

        
        
    
    

# Dashboard route (only accessible if logged in)
@app.route('/dashboard')
def dashboard():
    if 'admin' not in session:
        return redirect(url_for('adminIndex'))
    return render_template('dashboard.html', admin=session['admin'])

# Users route (fetches user data from database)
@app.route('/users')
def users():
    if 'admin' not in session:
        return redirect(url_for('adminIndex'))
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    return render_template('users.html', users=users)

# Logout route (clears session data and redirects to login)
@app.route('/logout')
def logout():
    session.clear()  # Clears all session data
    flash('Logged out successfully!', 'info')  # Flash message for logout success
    return redirect(url_for('adminIndex'))

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
