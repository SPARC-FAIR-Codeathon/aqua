# "Notify Me" module
### Email notification functionality

## Main Purpose

The primary purpose of this functionality is to notify users whenever a new dataset is published against their search terms if nothing is available at the moment.

However, users can still use the same function to receive a summary table including basic information and links to all datasets currently matching their keywords.

Additionally, as requests are saved in a database, this information can be further accessed and analysed to get further content improvement.


## How to run

1. Run notifyme_api.py, in order fetch the user email and search keywords.
 
 an example call:
 	
  http://localhost:5432/aqua/notifyme?email=<email>&keywords=<keywords>
 
 
2. In order to schedule the keywords search and sending emails, you need to run notifyme_sched.py

The current setting is scheduling emails to be sent daily at 2 am


 3. A sample analytics visualization can run through [NotifyMe_analytics_visual.ipynb](https://nbviewer.jupyter.org/github/lrasmy/aqua/blob/main/NotifyMe/NotifyMe_analytics_visual.ipynb)
 

## How it works

<p align="left">
  <img src="https://github.com/Niloofar-Sh/aqua/blob/main/src/assets/images/NotifyMe.jpeg" alt="interface" width="900" height="550"> 
  <br/> 
  </img>
</p>

<br/>

We can summarize the "Notify Me" actions as follow:
1.	Add email requests with keywords.
2.	Scan for existing search hits and send email
3.	Moving pending requests to a waiting list that’s scanned daily
4.	Moving fulfilled requests to an archived list
5.	Any failed requests (that already have matching hits) will remain on the waiting list for one month, during which the "Notify Me" module will try to send the email daily. Afterwards, if the email still failing, it will move to the archived list with a final failed status for efficiency.

NotifyMe.db is the "Notify Me" SQLite database file. The database will be automatically created during the first call of the "Notify Me" module.  If one needs to drop and recreate the database for any reason, they can call the create_notifyme_db function from Notifyme_utils and set the clean option to True.


## Required Packages
- configparser
- flask_restplus
- numpy
- pandas
- schedule
- smtplib
- sqlite3

and plotly express for visualization examples

