from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
#Thease are Flask application intialization
app = Flask(__name__)


app.secret_key = 'your secret key'


# Enter your database connection details below for mysql
app.config['MYSQL_HOST'] = 'sql12.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql12728508'
app.config['MYSQL_DB'] = 'sql12728508'
app.config['MYSQL_PASSWORD'] = 'rltKEYjiDm'
app.config['MYSQL_UNIX_SOCKET'] = '/var/run/mysqld/mysqld.sock'
mysql = MySQL(app)


#This is default login url. it can access get and post request from F.E
#This is for login
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        #This is for check the account data with credential
        account = check_user_credentials(username, password)
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            login_as = account['login_as']
            login_is_user = (login_as == 'user')
            jobs = fetch_jobs_data(account, login_as)
            if login_is_user:
                return render_template("user_home_page.html", jobs = jobs,username=session['username'],login_is_user = login_is_user)
            else:
                return render_template("company_home.html", jobs = jobs,username=session['username'],login_is_user = login_is_user)
        else:
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg=msg)

@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        login_as = request.form['login_as']
        login_is_user = (login_as == 'user')
        #if this is login_is_user we are inserting employee and account table
        #else we are inserting company and account table
        if login_is_user:
            user_location = request.form['user_location']
            gender = request.form['gender']
            date_of_birth = request.form['date_of_birth']
            company_name = ''
            company_location = ''
            company_established_on = ''
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO employee VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (request.form['skills'], request.form['education'], request.form['experience'],request.form['current_package'],request.form['expecting_package'],request.form['working_mode'],date_of_birth,request.form['employee_name'],user_location,gender))            
            mysql.connection.commit()
        else:
            company_name = request.form['company_name']
            company_location = request.form['company_location']
            company_established_on = request.form['company_established_on']
            user_location = ''
            gender = ''
            date_of_birth = ''
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO company VALUES (NULL,%s,%s,%s,%s)', (company_name,company_location,company_established_on,request.form['industry_type']))            
            mysql.connection.commit()

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s)', (username, password, email,login_as,company_name,company_location,company_established_on,user_location,date_of_birth,gender,))            
             # cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()


            msg = 'You have successfully registered!'

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)
    # http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users


#This is job creation part
#on job creation we are inserting jobs and job_category table
@app.route('/pythonlogin/submit_job', methods=['GET', 'POST'])
def submit_job():
    # Check if user is loggedin
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO jobs VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", ( request.form['skills'], request.form['education'],request.form['experience'], request.form['package'],request.form['working_mode'],request.form['company_name'],request.form['working_hour'],request.form['company_location'],request.form['company_description'],request.form['website'],request.form['twitter_link'],request.form['job_description'],request.form['open_postions'],request.form['title'],request.form['job_location'],request.form['job_region'],request.form['job_posters_email'],request.form['start_date'],session['id'],))            
        mysql.connection.commit()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM jobs ORDER BY id DESC LIMIT 1')
        jobs = cursor.fetchone()
        job_id = jobs['id']
        cursor.execute('INSERT INTO job_categories VALUES (NULL,%s,%s,%s)', (request.form['category_name'],request.form['benifit'],job_id))      
        mysql.connection.commit()
        msg = 'Job Posted Succeffully!'
        return render_template('post_job.html', msg=msg,username=session['username'])
    return redirect(url_for('login'))

#This will hit when we clicked post job button in UI
@app.route('/pythonlogin/post_job')
def post_job():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('post_job.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    
#This will when we apply the  jobs from employee login
# here we are insrting applied job, notification table
@app.route('/apply/<int:id>', methods=['GET', 'POST'])
def apply(id):
    jobs = fetch_jobs_data_by_id(id)

    #applied job table insert
    company_id = jobs['job_poster_company_id']
    employee_id = session['id']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO applied_jobs VALUES (NULL,%s,%s,%s)', (employee_id,company_id,id))            
    mysql.connection.commit()

    #Insert into Notification
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    message =  "Hi, You applied for "+ jobs['company_name'] +" Company" + " "  + jobs['title'] +" Job." + "We reviewing your profile. and once you shortlisted, we will get back to you.Thanks For Applying- From HR Team"
    cursor.execute('INSERT INTO notifications VALUES (NULL,%s,%s,%s)', (company_id,employee_id,message,))
    mysql.connection.commit()

    # here we are collecting all applied_jobs record of logged_in user/session use
    # collecting job_id from applied_jobs like job_array = [1,2,3]
    # selecting jobs from job_array it will be the applied job for user

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM applied_jobs WHERE employee_id = %s', [session['id']])
    applied_jobs = cursor.fetchall()
    job_array = []
    for row in applied_jobs:
        job_array.extend([row['job_id']])
    cursor.close()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    placeholders= ', '.join(['%s']*len(job_array)) 
    query = 'SELECT * FROM jobs WHERE id IN ({})'.format(placeholders)
    cursor.execute(query, tuple(job_array))      
    jobs = cursor.fetchall()

    # Show the profile page with account info
    accout = fetch_logged_in_account(session['id'])
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
    account = cursor.fetchone()
    # Show the profile page with account info
    login_as = account['login_as']
    login_is_user = (login_as == 'user')

    return render_template("applied_job.html", jobs = jobs,username=session['username'], login_is_user = login_is_user,message = "Job applied successfully")

    return redirect(url_for('login'))

#here when we click job from company login. we can get list of users
#here id is job id.
#from applied_job we are collecting employee id from job id
# like employee id = [1,2,3,5]
# from employee id we are getting accounts of applied user for job

@app.route('/applied_list/<int:id>', methods=['GET', 'POST'])
def applied_list(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT employee_id FROM applied_jobs WHERE job_id = %s', [id])
    employee_ids = [row['employee_id'] for row in cursor.fetchall()]
    cursor.close()

    accounts = []
    if employee_ids:
        placeholders= ', '.join(['%s']*len(employee_ids)) 
        query = 'SELECT * FROM accounts WHERE id IN ({})'.format(placeholders)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, tuple(employee_ids))      
        accounts = cursor.fetchall()

    return render_template("applied_list.html", accounts = accounts, username=session['username'])


@app.route('/delete_job/<int:id>', methods=['GET', 'POST'])
def delete_job(id):
    # Remove session data, this will log the user out
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute('DELETE FROM jobs WHERE id = %s', (id,))
    mysql.connection.commit()

    account = fetch_logged_in_account(session['id'])

    login_as = account['login_as']
    login_is_user = (login_as == 'user')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM jobs WHERE job_poster_company_id = %s', (account['id'],))

    jobs = cursor.fetchall() 
    return render_template("company_home.html", jobs = jobs,username=session['username'], message = "Job Deleted Succeffully")
    return redirect(url_for('login'))


@app.route('/pythonlogin/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

#This is for search api
#The LIKE operator is used to check specified pattern in a column.
@app.route('/pythonlogin/search_api', methods=['GET', 'POST'])
def search_api():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        # User is not loggedin redirect to login page
        title = request.form['title'].strip()

        skills = request.form['skills'].strip()

        working_mode = request.form['working_mode'].strip()

        company_name = request.form['company'].strip()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""SELECT * FROM jobs WHERE skills LIKE %s OR title LIKE %s OR company_name LIKE %s OR working_mode LIKE %s""", (skills,title,company_name,working_mode))
        jobs = cursor.fetchall()

        account = fetch_logged_in_account(session['id'])

        login_as = account['login_as']
        login_is_user = (login_as == 'user')

        return render_template("user_home_page.html", jobs = jobs,username=session['username'],login_is_user=login_is_user)


@app.route('/pythonlogin/company_home')
def company_home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM jobs WHERE job_poster_company_id = %s', (session['id'],))

        jobs = cursor.fetchall() 
        return render_template("company_home.html", jobs = jobs,username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/pythonlogin/user_home_page')
def user_home_page():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM jobs')
        jobs = cursor.fetchall() 

        account = fetch_logged_in_account(session['id'])


        login_as = account['login_as']
        login_is_user = (login_as == 'user')

        return render_template("user_home_page.html", jobs = jobs,username=session['username'],login_is_user= login_is_user)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route('/pythonlogin/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        account = fetch_logged_in_account(session['id'])
        # Show the profile page with account info
        login_as = account['login_as']
        login_is_user = (login_as == 'user')

        return render_template('profile.html', account=account,login_is_user= login_is_user)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

#This is to check applied job
# here we are collecting all applied_jobs record of logged_in user/session use
# collecting job_id from applied_jobs like job_array = [1,2,3]
# selecting jobs from job_array it will be the applied job for user
@app.route('/pythonlogin/applied_job')
def applied_job():
    # Check if user is logged in
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM applied_jobs WHERE employee_id = %s', [session['id']])
    applied_jobs = cursor.fetchall()

    # If there are applied jobs, get the details for each job
    if applied_jobs:
        job_array = [row['job_id'] for row in applied_jobs]
        placeholders = ', '.join(['%s'] * len(job_array))
        query = 'SELECT * FROM jobs WHERE id IN ({})'.format(placeholders)
        cursor.execute(query, tuple(job_array))      
        jobs = cursor.fetchall()
    else:
        jobs = []

    # Get the account details for the user
    account = fetch_logged_in_account(session['id'])

    # Check if the user is logging in as a user
    login_as = account['login_as']
    login_is_user = (login_as == 'user')

    # Close the cursor
    cursor.close()

    # Show the profile page with account info
    return render_template("applied_job.html", jobs = jobs, username=session['username'], login_is_user = login_is_user)

#This method for Notification
@app.route('/pythonlogin/notification')
def notification():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM notifications WHERE employee_id = %s', [session['id']])
        notifications = cursor.fetchall()
        account = fetch_logged_in_account(session['id'])

        login_as = account['login_as']
        login_is_user = (login_as == 'user')

        return render_template("notification.html", notifications = notifications,username=session['username'],login_is_user= login_is_user)

    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


#Common Methods
#input:- username, password
#Output :- list of account
def check_user_credentials(username, password):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
    account = cursor.fetchone()
    return account

#input:- account, login_as
#Output :- list of jobs
#incase of user all jobs need to show
#incase company only possted job by company admin need to show
def fetch_jobs_data(account, login_as):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    login_is_user = (login_as == 'user')
    if login_is_user:
        cursor.execute('SELECT * FROM jobs ')
    else:
        cursor.execute('SELECT * FROM jobs WHERE job_poster_company_id = %s', (account['id'],))
    jobs = cursor.fetchall() 
    return jobs

#input:- job_id
#Output :- job data
def fetch_jobs_data_by_id(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM jobs WHERE id = %s', (id))
    # Fetch one record and return result
    jobs = cursor.fetchone()
    return jobs

#input:- account id
#Output :- account data
def fetch_logged_in_account(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (id,))
    account = cursor.fetchone()
    return account