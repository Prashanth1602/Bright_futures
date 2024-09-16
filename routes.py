import os
import csv
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Dummy job data
jobs = [
    {"title": "Railway Engineer", "location": "Kolkata"},
    {"title": "Public Sector Bank PO", "location": "Chennai"},
    {"title": "Income Tax Inspector", "location": "Hyderabad"},
    {"title": "SSC CGL Officer", "location": "Lucknow"},
    {"title": "Defense Officer", "location": "Pune"},
    {"title": "Customs Officer", "location": "Ahmedabad"},
    {"title": "State Civil Services Officer", "location": "Bhopal"},
    {"title": "Indian Postal Service Officer", "location": "Patna"},
    {"title": "Reserve Bank of India Grade B Officer", "location": "Mumbai"},
    {"title": "Public Sector Undertaking (PSU) Engineer", "location": "Noida"},
    {"title": "DRDO Scientist", "location": "Bangalore"},
    {"title": "ISRO Scientist", "location": "Thiruvananthapuram"},
    {"title": "Food Corporation of India (FCI) Manager", "location": "Chandigarh"},
    {"title": "LIC AAO", "location": "Delhi"},
    {"title": "Government School Teacher", "location": "Jaipur"},
    {"title": "State Police Constable", "location": "Kolkata"},
    {"title": "Assistant in Ministry of External Affairs", "location": "Delhi"}
]

# Dummy daily wage jobs data
daily_wage_jobs = [
    {"title": "Construction Laborer", "location": "Bangalore"},
    {"title": "Warehouse Worker", "location": "Delhi"},
    {"title": "Delivery Helper", "location": "Mumbai"},
    {"title": "Electrician", "location": "Pune"},
    {"title": "Gardener", "location": "Chennai"},
    {"title": "Plumber", "location": "Hyderabad"},
    {"title": "Carpenter", "location": "Noida"},
    {"title": "Auto Rickshaw Driver", "location": "Kolkata"},
    {"title": "Housekeeping Staff", "location": "Gurgaon"},
    {"title": "Packager", "location": "Indore"}
]

# Dummy industrial job listings
job_listings = [
    {"title": "Welder", "location": "Mumbai"},
    {"title": "Assembly Line Worker", "location": "Pune"},
    {"title": "Maintenance Technician", "location": "Hyderabad"},
    {"title": "Forklift Operator", "location": "Chennai"},
    {"title": "Production Supervisor", "location": "Delhi"}
]

# Dummy small-scale jobs data
small_scale_jobs = [
    {"title": "Freelance Photographer", "location": "Delhi"},
    {"title": "Bakery Chef", "location": "Mumbai"},
    {"title": "Event Planner", "location": "Chennai"},
    {"title": "Handicraft Maker", "location": "Jaipur"},
    {"title": "Freelance Web Developer", "location": "Bangalore"}
]

# CSV file paths
USER_DATA_FILE = 'user_data.csv'
APPLIED_JOBS_FILE = 'applied_jobs.csv'

@app.route('/')
def home():
    name = session.get('user_name', 'Guest')
    return render_template('home.html', user_name=name)

@app.route('/govjobs', methods=['GET', 'POST'])
def government_jobs():
    if request.method == 'POST':
        sort_by = request.form.get('sort_by', 'location')
        sorted_jobs = sorted(jobs, key=lambda x: x.get(sort_by, ''))
    else:
        sorted_jobs = jobs
    return render_template('govtjobs.html', jobs=sorted_jobs)

@app.route('/dailywagejobs', methods=['GET', 'POST'])
def daily_wage_jobs_section():
    if request.method == 'POST':
        sort_by = request.form.get('sort_by', 'location')
        sorted_jobs = sorted(daily_wage_jobs, key=lambda x: x.get(sort_by, ''))
    else:
        sorted_jobs = daily_wage_jobs
    return render_template('dailywagejobs.html', jobs=sorted_jobs)

@app.route('/joblistings', methods=['GET', 'POST'])
def industrial_job_listings():
    if request.method == 'POST':
        sort_by = request.form.get('sort_by', 'location')
        sorted_jobs = sorted(job_listings, key=lambda x: x.get(sort_by, ''))
    else:
        sorted_jobs = job_listings
    return render_template('joblistings.html', jobs=sorted_jobs)

@app.route('/smallscalejobs', methods=['GET', 'POST'])
def small_scale_jobs_section():
    if request.method == 'POST':
        sort_by = request.form.get('sort_by', 'location')
        sorted_jobs = sorted(small_scale_jobs, key=lambda x: x.get(sort_by, ''))
    else:
        sorted_jobs = small_scale_jobs
    return render_template('smallscalejobs.html', jobs=sorted_jobs)

@app.route('/apply_for_job', methods=['POST'])
def apply_for_job():
    job_title = request.form.get('job_title')
    user_name = session.get('user_name', None)

    if user_name and job_title:
        # Store job applied in CSV file
        with open(APPLIED_JOBS_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([user_name, job_title])
        
        flash(f'Applied for job: {job_title}', 'success')
    else:
        flash('You must be logged in and select a job to apply for.', 'error')

    return redirect(url_for('home'))

@app.route('/about')
def about():
    # Get the current user's name from the session
    current_user_name = session.get('user_name', None)
    if not current_user_name:
        flash("No user is currently logged in.", "warning")
        return redirect(url_for('home'))

    # Read user data and jobs applied from CSV files
    user_data = []
    applied_jobs = []

    # Read user data from the file
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, mode='r') as file:
            reader = csv.reader(file)
            user_data = [row for row in reader if row[0] == current_user_name]

    # Read applied jobs from the file
    if os.path.exists(APPLIED_JOBS_FILE):
        with open(APPLIED_JOBS_FILE, mode='r') as file:
            reader = csv.reader(file)
            applied_jobs = [row for row in reader if row[0] == current_user_name]

    return render_template('about.html', user_data=user_data, applied_jobs=applied_jobs)

@app.route('/submit_user_details', methods=['POST'])
def submit_user_details():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    
    if not name or not email or not phone:
        flash('All fields are required!', 'error')
        return redirect(url_for('home'))

    # Store user details in CSV file
    with open(USER_DATA_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, email, phone])
    
    # Set the user name in the session
    session['user_name'] = name

    flash('User details submitted successfully!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
