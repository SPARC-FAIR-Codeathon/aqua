## Lrasmy@AQUA Team   July 17 2021      ##
##########################################
#!/usr/bin/env python
# coding: utf-8
# In[1]:


### loading required packages

import smtplib
import sqlite3
import pandas as pd
import configparser
import json
import requests
import numpy as np
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# In[2]:


### loading configurations from properties.ini

config = configparser.ConfigParser()
config.read('properties.ini')
gmail_user = config['EMAIL']['user']
gmail_password = config['EMAIL']['password']
dbname=config['SQLite']['dbname']


# In[3]:


### Database creation, if not already previously available
def create_notifyme_db(db_name, clean=False):      
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    if clean:
        cur.execute('DROP TABLE IF EXISTS new_register') 
        cur.execute('Drop TABLE IF EXISTS waiting_list')
        cur.execute('Drop TABLE IF EXISTS archieved_list')
        cur.execute('Drop TABLE IF EXISTS Failed_emails')  
    cur.execute('CREATE TABLE IF NOT EXISTS new_register (entry_id INTEGER PRIMARY KEY AUTOINCREMENT,email VARCHAR, register_date VARCHAR ,keywords VARCHAR, status VARCHAR, last_modified VARCHAR )')
    cur.execute('CREATE TABLE IF NOT EXISTS waiting_list (entry_id INTEGER, email VARCHAR, register_date VARCHAR ,keywords VARCHAR, status VARCHAR, last_modified VARCHAR, hits INTEGER, failed_reqid INTEGER )')
    cur.execute('CREATE TABLE IF NOT EXISTS archieved_list (entry_id INTEGER, email VARCHAR, register_date VARCHAR ,keywords VARCHAR, status VARCHAR, last_modified VARCHAR,hits INTEGER, failed_reqid INTEGER )')
    cur.execute('CREATE TABLE IF NOT EXISTS Failed_emails (failed_reqid INTEGER PRIMARY KEY AUTOINCREMENT, corresponding_entry_id INTEGER, error_message VARCHAR, error_date VARCHAR )')
    conn.commit()
    conn.close()
    
create_notifyme_db(dbname)


# In[4]:


### This is the main function to be called by the front end to save the entries
## No cookies stored now, can easily ammend later
def add_new_single_entry(email,keyword):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute('INSERT INTO new_register (email, register_date,keywords , status , last_modified ) VALUES (?, CURRENT_TIMESTAMP, ? , "New" , CURRENT_TIMESTAMP)',
                (email,keyword ))
    conn.commit()
    conn.close()


# In[5]:


### to get how many hits currently exist against keywords, mainly used in scan_new_register 
def get_hits_count(keyword):    
    rsp = requests.get('https://scicrunch.org/api/1/elastic/SPARC_PortalDatasets_pr/_search?api_key=yu3Dsi11Saczah4etEycedoYBvXvPSkS&q='+ keyword)
    rsp = json.loads(rsp.text)
    return rsp['hits']['total']


# In[6]:


### to check if there is any duplicate entries and archieve those for efficency, mainly called in scan_new_register and scan_waiting_list() 
def archieve_duplicates(df):
    df['duplicate_flag']= df.duplicated(subset=['email','keywords'],keep='last')
    df_dup=df[df['duplicate_flag']==True]
    df_dup['status']='Duplicate'
    df_dup['last_modified']=str(pd.to_datetime('now')).split('.')[0]
    df_dup.drop(columns=['duplicate_flag'],inplace=True)
    conn = sqlite3.connect(dbname)
    df_dup.to_sql('archieved_list', conn, if_exists='append', index=False)
    conn.close()
    df=df[df['duplicate_flag']==False].drop(columns=['duplicate_flag'])
    return df


# In[15]:


### This is the main function to retrieve search results as a pandas df to embedd in the email message
def retrieve_search_to_df(keyword):
    rsp = requests.get('https://scicrunch.org/api/1/elastic/SPARC_PortalDatasets_pr/_search?api_key=yu3Dsi11Saczah4etEycedoYBvXvPSkS&q='+ keyword)
    ### need to make sure I got the most matching and get the top 10, that should use our improved search and not just the k core
    rsp = json.loads(rsp.text)
    if rsp['hits']['total']==0:
        return 'Nothing matching yet'
    else:
        df_search=pd.DataFrame.from_dict(rsp['hits']['hits'])
        df_search=pd.concat([df_search['_source'].apply(pd.Series)['pennsieve'].apply(pd.Series)[['identifier']],
            df_search[['_id','_score']],
        df_search['_source'].apply(pd.Series)['item'].apply(pd.Series)[['name','description']],
        df_search['_source'].apply(pd.Series)['item'].apply(pd.Series)['published'].apply(pd.Series)['status'],
        ], axis=1)
        df_search['link']= 'https://sparc.science/datasets/'+df_search['identifier']

        return df_search


# In[8]:


### Sending Email with the results
def send_email_alert_withtable(emaillist, keyword):
    msg = MIMEMultipart()
    msg['Subject'] = "SPARC AQUA Notification: New Dataset Matching your search for "+keyword
    msg['From'] = gmail_user
    
    df_results=retrieve_search_to_df(keyword)
    
    html = """    <html>
      <head></head>
      <body>
        {0}
      </body>
    </html>
    """.format(df_results.to_html(render_links=True))
    
    part1 = MIMEText(html, 'html')
    msg.attach(part1)
    
    mail_errors={}
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        mail_errors=server.sendmail(gmail_user, emaillist, msg.as_string())
        server.close()       
        
    except Exception as e:
        for x in emaillist: mail_errors[x]=e
        
    return mail_errors


# In[9]:


### This function is to send email and capture errors, normally called for records with hits>0 in scan_waiting_list
def send_mail_capture_error(df):
    Failed_entries={}
    sent_entries=[]
    for k, subg in df.groupby('keywords'):
            maillist=list(subg['email'])
            entries_list=list(subg['entry_id'])
            mail_errors=send_email_alert_withtable(maillist,k)
            if len(mail_errors)>0:
                    for e in list(mail_errors.keys()):
                        for i, email in enumerate(maillist):
                            if email==e: 
                                Failed_entries[entries_list[i]]= mail_errors[e]
                            else: sent_entries.extend(entries_list[i])
            else:sent_entries.extend(entries_list)
    return sent_entries,Failed_entries


# In[10]:


def clean_update_hits_df(df,list_entries, status):
    df_clean=df[df['entry_id'].isin(list_entries)]
    df_clean.loc[:,['status']]=status
    df_clean.loc[:,['last_modified']]=str(pd.to_datetime('now')).split('.')[0]
    df_clean.loc[:,['hits']]=df_clean[['hits','updated_hits']].max(axis=1)
    df_clean.drop(columns='updated_hits',inplace=True)
    return df_clean


# In[11]:


def update_failed_email(entry_id,exception):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute('INSERT INTO Failed_emails(corresponding_entry_id,error_message, error_date) VALUES (?,?,  CURRENT_TIMESTAMP)',(entry_id,exception))
    conn.commit()
    cur.execute('Update waiting_list set status="Failed",failed_reqid=(select max(failed_reqid) from Failed_emails where corresponding_entry_id=? ) where entry_id=?',
                (entry_id,entry_id ))
    conn.commit()
    conn.close()


# In[12]:


### This is the first function to run in the periodic (daily routine), mainly to check all new entries,
### archieve duplicates and check the current number of hits and move to the processing waiting list 
def scan_new_register():    
    conn = sqlite3.connect(dbname)
    df = pd.read_sql_query("SELECT * FROM new_register", conn)
    conn.close()
    df = archieve_duplicates(df)
    df['hits']=df['keywords'].apply(get_hits_count)
    df['last_modified']=str(pd.to_datetime('now')).split('.')[0]
    conn = sqlite3.connect(dbname)
    df.to_sql('waiting_list', conn, if_exists='append', index=False)
    cur = conn.cursor()
    cur.execute('Delete from new_register where entry_id in (select distinct entry_id from waiting_list)' )
    cur.execute('Delete from new_register where entry_id in (select distinct entry_id from archieved_list)' )
    conn.commit()
    conn.close()


# In[13]:


### this is the next function following the scan of new entries, and the resposible one for sending emails and capture errors
def scan_waiting_list():    
    conn = sqlite3.connect(dbname)
    df = pd.read_sql_query("SELECT * FROM waiting_list", conn)
    conn.close()
    df = archieve_duplicates(df)
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute("Delete from waiting_list where entry_id in (select distinct entry_id from archieved_list)" )
    df['updated_hits']=0
    df['updated_hits'][df['hits']==0]= df[df['hits']==0]['keywords'].apply(get_hits_count)
    df= df[(df['hits']>0) | (df['updated_hits']>0)]
    entries_sent, failed_dict =send_mail_capture_error(df)
    ###move sent emails entries to archieve table
    df_sent=clean_update_hits_df(df,entries_sent,'Sent')
    df_sent.to_sql('archieved_list', conn, if_exists='append', index=False)
    cur.execute('Delete from waiting_list where entry_id in (select distinct entry_id from archieved_list)' )
    conn.commit()
    conn.close()
    ### Store the failed entries in the failed table and flag the failed entries in the waiting list table 
    if len(failed_dict)>0: 
        for k,v in failed_dict.items(): update_failed_email(k,str(v)) 
