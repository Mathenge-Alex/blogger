# Blogger
This is a bloggers website where a user can post, edit and comment on blogs.

### [View Here]() 

## Description

This is a flask application that enables a user to view and post blogs by other people. A user can create a blog, like or dislike a blog and leave a comment in a blog posted by a different person.

## User Journey
A new user can use the following features:
- Register an account which entails an email and password. A welcome email is sent
- Login as a registered user.
- While authenticated, create, update, delete, and comment on blogs, update account info, and like or dislike a blog.
- Users can reset their passwords if they have forgotten
 
## User Installation

    # Use git to clone the repository to your local directory.
    $ git clone git@github.com:Mathenge-Alex/blogger.git
    $ cd flask_posts
    # Open with your favorite code editor and continue with installations below.
    
    
### Create a Virtual Environment with pipenv and Activate it

    $ pipenv install
    $ pipenv shell

### Install the Application Dependencies.

    $ pipenv install -r requirements.txt 
   
    
 ### Running the Application
 
     $ python3 app.py
     
## License
The application is governed by an MIT License

Copyright &copy; 2022 Mathenge Alex