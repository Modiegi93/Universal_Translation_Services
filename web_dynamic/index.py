#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv
from  flask import Flask, render_template
from translator.subsriber import Subscriber
from translator import storage

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def index():
    """Index"""
    return render_template('index.html', cache_id=uuid.uuid4())

@app.route('/login', strict_slashes=False)
def login():
    "User login"
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('psw')
        
        # Perform login validation and authentication
        user = User.storage.get(email=email).first()
        if user and user.password == password:
            return jsonify({'message': 'Login successful'})
        else:
            return jsonify({'error': 'Invalid email or password'})
    
    return render_template('index.html', cache_id=uuid.uuid4())

# Sign up endpoint
@app.route('/sign_up', strict_slashes=False)
def signup():
    """Sign up new user"""
    if request.method == 'POST':
        full_name = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('psw')
        
        # Perform sign up and user registration
        user = User(full_name=full_name, email=email, password=password)
        storage.new(user)
        storage.save()
        
        return jsonify({'message': 'Sign up successful'})
    
    return render_template('index.html', cache_id=uuid.uuid4())

@app.route('/subscribe', strict_slashes=False)
def subscribe():
    email = request.form.get('email')
    daily_newsletter = True if request.form.get('daily-newsletter') else False

    # Perform subscription logic here
    subscriber = Subscriber(email=email, daily_newsletter=daily_newsletter)
    storage.new(subscriber)
    storage.save()

    # Send confirmation email
    send_confirmation_email(email)

    return render_template('subscription_success.html', email=email,
                           daily_newsletter=daily_newsletter, cache_id=uuid.uuid4())

def send_confirmation_email(email):
    msg = Message('Subscription Confirmation',
                  sender='your-email@example.com', recipients=[email])
    msg.body = 'Thank you for subscribing to our newsletter!'
    mail.send(msg)

@app.route('/logout', strict_slashes=False)
def logout():
    # Clear the session
    storage.close()
    return redirect(url_for('/'))  # Redirect to the login page

@app.teardown_appcontext
def close_session(exception):
    """Remove the db session or save file"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
