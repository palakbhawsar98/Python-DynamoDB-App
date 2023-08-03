import boto3
from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "0069318"  
dynamo_db = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamo_db.Table('users')

@app.route('/signup', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        table.put_item(Item={'username': username, 'password': password})
        return redirect(url_for('signin'))
    
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        response = table.get_item(Key={'username': username})
        item = response.get('Item', None)

        if item and item['password'] == password:
            session['user_id'] = username
            return redirect(url_for('dashboard'))

    return render_template('signin.html')

@app.route('/signout')
def signout():
    session.pop('user_id', None)
    return redirect(url_for('signin'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return f"Welcome, user {session['user_id']}!"
    else:
        return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
