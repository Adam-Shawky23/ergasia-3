# Εισαγωγή Flask και database συναρτήσεων
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db import get_cursor, commit, rollback
# Εισαγωγή συναρτήσεων κρυπτογράφησης κωδικών
from werkzeug.security import generate_password_hash, check_password_hash

# Δημιουργία blueprint για ταυτοποίηση χρήστη
auth_bp = Blueprint('auth', __name__)


# Δρομολόγηση εγγραφής χρήστη (GET - φόρμα, POST - αποθήκευση)
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name'].strip()
        last_name  = request.form['last_name'].strip()
        email      = request.form['email'].strip().lower()
        password   = request.form['password']
        dob        = request.form.get('dob') or None
        hometown   = request.form.get('hometown', '').strip() or None
        gender     = request.form.get('gender') or None

        # Έλεγχος απαιτούμενων πεδίων
        if not all([first_name, last_name, email, password]):
            flash('Please fill in all required fields.', 'error')
            return render_template('register.html')

        cur = get_cursor()

        # Έλεγχος αν το email ήδη υπάρχει
        cur.execute('SELECT user_id FROM users WHERE email = %s', (email,))
        if cur.fetchone():
            flash('An account with that email already exists.', 'error')
            return render_template('register.html')

        # Κρυπτογράφηση του κωδικού
        hashed = generate_password_hash(password)
        try:
            # Εισαγωγή νέου χρήστη στη βάση δεδομένων
            cur.execute("""
                INSERT INTO users (first_name, last_name, email, dob, hometown, gender, password)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING user_id
            """, (first_name, last_name, email, dob, hometown, gender, hashed))
            user_id = cur.fetchone()['user_id']
            commit()
            # Αποθήκευση στο session
            session['user_id']   = user_id
            session['user_name'] = f'{first_name} {last_name}'
            flash('Welcome to k29photo!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            rollback()
            flash(f'Registration failed: {e}', 'error')

    return render_template('register.html')


# Δρομολόγηση σύνδεσης χρήστη (GET - φόρμα, POST - έλεγχος)
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email'].strip().lower()
        password = request.form['password']

        cur = get_cursor()
        # Αναζήτηση χρήστη με το email
        cur.execute("""
            SELECT user_id, first_name, last_name, password
            FROM users WHERE email = %s
        """, (email,))
        user = cur.fetchone()

        # Έλεγχος κωδικού και σύνδεση
        if user and check_password_hash(user['password'], password):
            # Αποθήκευση στο session
            session['user_id']   = user['user_id']
            session['user_name'] = f"{user['first_name']} {user['last_name']}"
            flash('Logged in successfully.', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.', 'error')

    return render_template('login.html')


# Δρομολόγηση αποσύνδεσης χρήστη
@auth_bp.route('/logout')
def logout():
    # Καθαρισμός session
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))