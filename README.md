# Who Wants to Be a Millionaire? - Django Application

This Django application implements a "Who Wants to Be a Millionaire?" style quiz game.
This project includes user authentications using custom user, a question answer game system and leaderboard system where show top 10 users who earn the best scores.

## Key Features:

- User registration and authentication with the help of django auth system and customizing it to use email instead of username
- Randomly select quiz questions from database
- Scoring system
- Leaderboard displaying top 10 players

## Project Structure:

- millionaire_project/ (main project directory)
  - game/ (quiz application)
  - account/ (auth and user related application)
  - manage.py (Django management script)
  - millionaire_game/ (main project files)

## Tech Stack:

- Django
- SQLite (database)
- Tailwind CSS (styling)

# Models Documentation

## CustomUser Model

Path: `account/models.py`

This model extends Django's AbstractUser to use email for authentication instead of username

Fields:

- email: EmailField (unique, used for authentication)
- best_score: IntegerField (stores the user's highest score)

## Question Model

Path: `game/models.py`

Represents a game question

Fields:

- text: CharField (the question text)
- points: IntegerField (point value of the question)

## Answer Model

Path: `game/models.py`

Represents an answer to a question. It has one-to-many relation with Question (one Question can have many answers)

Fields:

- question: ForeignKey to Question
- text: CharField (the answer text)
- is_correct: BooleanField (indicates if this is the correct answer)

## Game Model

Path: `game/models.py`

Represents a game session

Fields:

- player: ForeignKey to CustomUser
- score: IntegerField (current game score)
- current_question: IntegerField (tracks the current question number)
- completed: BooleanField (indicates if the game is finished)
- questions: ManyToManyField to Question (stores the game's questions)

# Views Documentation

Location: `account/views.py`

## Account Views

### custom_login

- Handles user login
- Uses CustomLoginForm
- Authenticates user and redirects to home page on success

### register

- Handles user registration
- Uses CustomUserCreationForm
- Creates a new user and logs them in on success

### custom_logout

- Handles user logout
- Redirects to home page after logout
- User must logged in to system

### leaderboard

- Fetches top 10 users based on best scores
- Renders the leaderboard page
- User must logged in to system

## Game Views

### start_game

- Initiates a new game session
- Selects 5 random questions for the game from database
- Redirects to play_game view
- User must logged in to system

### play_game[GET]

- Show current question with the answer
- User can select an answer
- User must logged in to system

### play_game[GET]

- Get the current answer from database
- Check if user already answered this question index or not
- If not check user answer if it's correct add the question score to current game points.
- Also show the user their selected answer and correct answer
- When user answer all the questions and game ended (game.completed == True or game.current_question > 5) it will check the user current best score and if their new score greater than their current score, update their best score.

## Other Views

### home

- Renders the home page
- Show Login/Register buttons if user not authenticated
- Show start game button if user already authenticated

# Views Documentation

The frontend of the application is created by django templates with the help of tailwind css.
