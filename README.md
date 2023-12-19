# Book Tracker Application

## Description
This repo contains the entire Django project with a single application: `book_tracker`.  
The book tracker application is an interactive web application that can be used to track books being read or
 wanting to be read.  
Initial project framework based on episodes 1-9 BugBytes' YouTube tutorial on [Django & HTMX](https://www.youtube.com/playlist?list=PL-2EBeDYMIbRByZ8GXhcnQSuv2dog4JxY)

## Getting Started
- Clone repo to local computer
- Open folder in terminal: `cd prototype-app`
- Set up Python virtual environment: `python3 -m venv .venv`
- Run virtual environment: `source .venv/scripts/activate`
    - When done run: `deactivate` to stop virtual environment
- Install required libraries: `pip install -r requirements.txt`
- Setup database: `python manage.py migrate`
- Start up Django server: `python manage.py runserver`
    - Use `Ctrl + C` to shut down server 
- Open web browser and go to local host @ `127.0.0.1:8000/register`
- Create a new user for yourself and login

## Notes
- Django Debug Toolbar is an included module in this application and it can reduce performance
  - To remove, delete the `django-debug-toolbar==4.2.0` line from `requirements.txt` before installing

## Author
Ellis Lempriere (ellis@pslfamily.org)