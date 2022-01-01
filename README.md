# MovieChecker
### Video Demo: https://youtu.be/uZdfqNzUZBE
### Description:

Final Project for CS50x 2021

For this project, I took the cs50-Finance homework we did for week 9 and used it as the skeleton for my project. I used the same ideas for the authentication process, and the general form of my application.py file. Using flask, I created the necessary routes for my project. I created a database, moviecheck.db and interacted with the database to perform user actions and log them for different users. 

At first I modified the finance50 layout.html to suit my project. After that changing some colors seemed to be the right choice.
I needed a login page to start and a register page at first. After creating them, I configured my application to process the login info and route the user to the index.html.
On index.html we see the most popular movies at the time. This data is coming from the API I used for the project, The movie database API. Getting the API key was not that difficult but getting the results in the format I could use was the hard part. I managed to complete this part eventually.
I took the helpers.py and edited the functions and added a few of my own to get the functionality we require. I am actually very proud of what I did to the apology function :). That made my coding experience a joy. 
At the favorites page, we can see our favorite movies and remove them from the list if we want. 
At the search page we can search for a movie to add to our favorites. Of course we can't add the same movie twice. 
At the history page we can see all of our actions.
Using the link at reset password we can change our password and this can't be the same as our original password.
I used the hashing algorithm we used for finance50 to store user passwords.
In my database, I have 3 tables:
Users
Actions
Favorites
Using these tables, all the functionality we want can be achieved. I think I could've designed my database better. 

For the templates I have:
apology: to render the error with a random image
favorites: to show the user what their favorite movies are
history: to keep track of user actions
index: to be a starting point of the experience and show the most popular movies at the time
layout: To provide the general layout of the page for the jinja templating
login: login page for the application
me: about me part
passres: to reset user password
register: to register the user
search: to search for a movie
searched: to show the results of the movie searched at search.html

Honestly, I could've made a lot more changes but realizing the assignment is due on 31st of December, and me realizing this at 29th of December prevented a lot of things I could've made. But after my submission, I will try to improve the application even further.  

Overall, CS50 was a blast and I really did have fun with all the homeworks(maybe not with DNA, that was a lot more challenging for me).

Thank you. 

