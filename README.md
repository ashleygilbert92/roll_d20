# Pathfinder RPG Tool using Python Flask
## https://roll-d20.com/


## Part1:

a)	Title: Pathfinder RPG Tool using Python Flask

b)	What will it do: Keep track of dice roll probability and data for play session 
(damage taken, damage done, healing, EXP earned, etc), calculate EXP, log session notes, 
form for player feedback, and have separate profiles for Dungeon Maters/campaigns, Grid 
overlay for maps, new product notifications.

c)	Target Audience: People who play Pathfinder RPG

d)	Data: Player feedback, play session data, dice rolls, and notes.

e)	Technologies: Python, Python Flask, Bootstrap, MySQL, Jinja

f)	Stretch Goals: Pictures for campaign page, player description page for other players, campaign specific rules page

## Part 2:

a)	Website: Will likely host it on Heroku or AWS. Both have lots of resources for flask apps.



## Project Checkpoints:

October 4th - Server, domain, basic flask app with file structure, mysql database setup with expected tables, create basic template for expected pages

October 23rd - Login page and session handling, routes defined, dice roll page, player feedback page, forms for play session page 

November 8th - Play session page previous session/encounter view, session notes page and view, grid map page setup, DM dashboard

November 27th - Figure out grid map overlay and display/download, figure out how to pull data for notifications, EXP calculation page 


## Checkpoint 1:
Oct 4th: I created my server, domain, basic flask app, mysql database with tables setup, and created templates (currently don't have any content). https://roll-d20.com/


## Checkpoint 2:
Oct 23rd: I have created a login page with session handling across the website (username: ashleymia92@gmail.com 
password: P@ssword1), I've created the dice roll/probability page, I've created the player feedback page for non 
logged in users and logged in users. I still need to create the forms for the play session page and have those 
figured out. Will work on this more and have these tasks finished by the end of the week. 


## Checkpoint 3: 
November 8th: I definitely overpromised on this one but I did still get a fair amount of it done. Styling and color still allude me but I'm trying.
I finished all pages for campaign, play session, notes, and list of encounters. I was not able to finish the final encounter view though. 
That one will be finished this week at the latest. I also spent a lot of time trying to debug sqlalchemy. It did not like me using one session 
for all of my actions. That one took me about and hour or more to figure out. Decided to create a new session for every action. All of the forms/modals
on these pages should work and are fully finished. I want to spend some more time on styling but I'm not sure I'll have time. The play session
page that contains notes and a list of encounters really needs fixed in that area. I'll work on this as much as I can. I changed my mind about the
DM dashboard and that basically turned into the Campaign management section. I want to have a home page for logged in users that just
shows some cool stats or an overview of some kind. We'll see if I get to that. I hope so. The styling on the Probability page needs fixed too.
I'm getting somewhere but I've still got a long way to go.
