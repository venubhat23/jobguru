# Job Guru

Job Guru is a job portal web application built using Flask and MySQL. This application allows users to register as either job seekers or companies, post jobs, apply for jobs, and view job applications.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Features](#features)
- [Routes](#routes)
- [Contributing](#contributing)

## Overview

Job Guru is designed to streamline the job searching and hiring process. Job seekers can browse and apply for job postings, while companies can post job listings and manage applications. The application is built with a Flask backend and a MySQL database.

## Installation

### Prerequisites

- Python 3.x
- MySQL
- Flask
- Git

### Steps

1. **Clone the repository:**
    bash
    git clone https://github.com/venubhat23/jobguru.git
    cd job_guru
    

2. **Create a virtual environment:**
    bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use venv\Scripts\activate
    

3. **Install the dependencies:**
    bash
    pip install -r requirements.txt
    

## Configuration

1. **Database Configuration:**
   - Open `app.py` and configure the database settings:
     python
     app.config['MYSQL_DATABASE_USER'] = 'yourusername'
     app.config['MYSQL_DATABASE_PASSWORD'] = 'yourpassword'
     app.config['MYSQL_DATABASE_DB'] = 'job_guru'
     app.config['MYSQL_DATABASE_HOST'] = 'localhost'
     

2. **Session Configuration:**
   - Optionally, configure session settings:
     python
     app.secret_key = 'your_secret_key'
     

## Database Setup

1. **Start MySQL server:**
   Ensure your MySQL server is running.

2. **Create Database:**
   sql
   CREATE DATABASE job_guru;
   

3. **Create Tables:**
   Run the following SQL commands to create the necessary tables:
   sql
   USE job_guru;

   CREATE TABLE accounts (
       id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(50) NOT NULL,
       password VARCHAR(255) NOT NULL,
       email VARCHAR(100) NOT NULL,
       account_type ENUM('user', 'company') NOT NULL,
       registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

   CREATE TABLE jobs (
       id INT AUTO_INCREMENT PRIMARY KEY,
       title VARCHAR(255) NOT NULL,
       description TEXT NOT NULL,
       company_id INT NOT NULL,
       posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY (company_id) REFERENCES accounts(id)
   );

   CREATE TABLE applications (
       id INT AUTO_INCREMENT PRIMARY KEY,
       job_id INT NOT NULL,
       user_id INT NOT NULL,
       applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY (job_id) REFERENCES jobs(id),
       FOREIGN KEY (user_id) REFERENCES accounts(id)
   );

   CREATE TABLE notifications (
       id INT AUTO_INCREMENT PRIMARY KEY,
       user_id INT NOT NULL,
       message TEXT NOT NULL,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       FOREIGN KEY (user_id) REFERENCES accounts(id)
   );
   

## Running the Application

1. **Run the application:**
    bash
    python app.py
    

2. **Open your web browser:**
    Navigate to `http://localhost:5000/pythonlogin/` to access the application.

## Features

- **User Authentication:** Secure login and registration for job seekers and companies.
- **Role-based Access Control:** Different functionalities for job seekers and companies.
- **Job Posting and Application:** Companies can post jobs, and job seekers can apply for them.
- **Notifications:** Users receive notifications related to their job applications.
- **Profile Management:** Users can manage their profiles.
- **Job Search:** Users can search for jobs based on keywords.

## Routes

- **`/pythonlogin/`**: Login page
- **`/pythonlogin/register`**: Registration page
- **`/pythonlogin/logout`**: Logout route
- **`/pythonlogin/home`**: Home page
- **`/pythonlogin/submit_job`**: Job submission form
- **`/pythonlogin/post_job`**: Job posting page
- **`/apply/<int:id>`**: Apply for a job
- **`/applied_list/<int:id>`**: View applicants for a job
- **`/delete_job/<int:id>`**: Delete a job posting
- **`/pythonlogin/search_api`**: Job search
- **`/pythonlogin/company_home`**: Company home page
- **`/pythonlogin/user_home_page`**: User home page
- **`/pythonlogin/profile`**: User profile page
- **`/pythonlogin/applied_job`**: View applied jobs
- **`/pythonlogin/notification`**: View notifications
    

8. **Update the database configuration:**
   Retrieve the database URL from Heroku and update `app.py`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
