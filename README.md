# SSW-500-Final-Project
Application: Python Quiz Application 

# Technologies used: 
Flask, MongoDB, 

# Overview
This project offers a dynamic web application featuring a Trivia quiz game with user authentication for personalized experiences. The aim is to provide an engaging platform for users to test their knowledge across various topics.

# Features
--> User Authentication: New users can register themselves, while existing users can log in to their accounts.

--> Dashboard: Upon logging in, users are directed to a dashboard. (Future scope includes enhancing the dashboard with user profiles for an improved experience.)

--> Quiz Interface: Users can click on "Take Quiz" on the dashboard to start. Five random questions from different categories appear on the screen.

--> Result Page: After answering the questions, users can submit their answers to view the results. The result page displays the number of correctly answered and incorrectly answered questions, along with the user's selected answers and the correct answers.

--> Interaction Options: Users have the choice to retake the quiz or log out from the quiz interface.

# Project Structure
--> Templates Folder: Contains all HTML files used for the web pages.

--> app.py: Entry point of the code. Contains logic, routes, and API calls. To run the code, execute app.py. The code is hosted on http://127.0.0.1:5000/.

--> models.py: Defines classes to structure the set of questions obtained from the API.
API Used: Open Trivia Database

--> static folder : contains images used throughout the website

# Running the Application
Run app.py.
Visit http://127.0.0.1:5000/ in your browser.
Register with your details or log in using your credentials.
Access the quiz by selecting "Take Quiz" on the dashboard.
Submit your answers to view your scores and the correct answers.
Choose to retake the quiz or log out.
