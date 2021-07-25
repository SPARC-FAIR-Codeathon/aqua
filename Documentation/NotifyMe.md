# "Notify Me" module
__(Email notification functionality)__

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

The database consists of 4 main tables:

1. __NEW_REGISTER__

| Column Name        | Description           | 
| ------------- |:-------------:| 
| entry_id     | A unique identifier for email requests (autoincrement integer) | 
| email      |   The user entered email (validated at the front end)    |   
| register_date |   The system date and time corresponding to the record creation, which is the time of the request initialization     |    
| keywords     | The user-entered search keywords | 
| status      |  All records in this table should show a ‘New’ status  |   
| last_modified |  In case the record get modified for any reason, this record is representing the last modification date and time for the corresponding record |  


2. __WAITING_LIST__

| Column Name        | Description           | 
| ------------- |:-------------:| 
| entry_id     | A unique identifier for email requests (automatically created in the new_register table) | 
| email      |   The user entered email (validated at the front end)    |   
| register_date |   The date and time of the request     |    
| keywords     | The user-entered search keywords | 
| status      | Request current status. Can be either ‘New’ if no hits still matching, or ‘Failed’ if the last attempt to send an email failed, the detailed error will be stored in Failed_emails |   
| last_modified | The date and time for the last modification of this record |  
| hits| The current number of matching hits exists against the search keywords. This should be ‘0’ for records remaining in ‘New’ status, and an actual number for ‘Failed’ records|
|failed_reqid|This is the reference for the latest corresponding Failed_emails record, showing the exact error that explains why this request failed|

3. __ARCHIEVED_LIST__

| Column Name        | Description           | 
| ------------- |:-------------:| 
| entry_id     | A unique identifier for email requests (automatically created in the new_register table) | 
| email      |   The user entered email (validated at the front end)    |   
| register_date |   The date and time of the request     |    
| keywords     | The user-entered search keywords | 
| status      | Request current status. Can be either ‘Sent’ for successfully sent emails,	‘Duplicate’ for the case in which the request identified earlier to be a duplicate request/entry,	‘Failed’ in case the email request raises an error consistently for more than one month. |   
| last_modified | The date and time for the last modification of this record. Should be corresponding to the time the email is sent if the status is ‘Sent’. |  
| hits| The number of matching hits sent against the search keywords. In case of failed requests, it will be the number of hits that exists at the time the record moved from the waiting_list table to here|
|failed_reqid|This is the reference for the latest corresponding Failed_emails record, showing the exact error that explains why this request failed|

4. __FAILED_EMAILS__

| Column Name        | Description           | 
| ------------- |:-------------:| 
|failed_reqid | A unique identifier for an error recorded against an email request (autoincrement integer)| 
|corresponding_entry_id | The corresponding entry_id of the email request will normally find either in the waiting_list table or the archieved_list table if we fail to send an email for more than a month|   
| register_date | The date and time of the request |    
|error_message | The detailed error message leading for email posting failure | 
|error_date | The system date and time when the error was triggered  |   



## Required Packages
- configparser
- flask_restplus
- numpy
- pandas
- schedule
- smtplib
- sqlite3

and plotly express for visualization examples

