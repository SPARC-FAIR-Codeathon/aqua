#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3
import pandas as pd
import configparser
import plotly.express as px
import seaborn as sns


# In[2]:


### loading configurations from properties.ini
config = configparser.ConfigParser()
config.read('properties.ini')
dbname=config['SQLite']['dbname']


# In[3]:


### load data into dataframes
conn = sqlite3.connect(dbname)
df_wait = pd.read_sql_query("SELECT * FROM waiting_list", conn)
df_arxiv = pd.read_sql_query("SELECT * FROM archieved_list", conn)
df_fail = pd.read_sql_query("SELECT * FROM Failed_emails", conn)
conn.close()
### Data Prep
## Keywords searched use counts
df_imp_keywords_wait=df_wait[(df_wait['status']!='Failed') & (df_wait['hits']<1)].groupby('keywords')['email'].count().reset_index()
df_imp_keywords_wait.columns=['keywords','Users_Count']
df_imp_keywords_wait['status']='Wait: No matched Datasets'
df_imp_keywords_arx=df_arxiv[(df_arxiv['status']!='Failed') & (df_arxiv['hits']>0)].drop_duplicates(subset=['keywords','email']).groupby('keywords')['email'].count().reset_index()
df_imp_keywords_arx.columns=['keywords','Users_Count']
df_imp_keywords_arx['status']='Matched Datasets Exists'
df_imp_keywords=pd.concat([df_imp_keywords_wait,df_imp_keywords_arx])
df_imp_keywords=df_imp_keywords.sort_values(by='Users_Count', ascending=False)
## Keyword max Hits
key_hits=df_arxiv[['keywords','hits']].drop_duplicates()
key_hits=key_hits.groupby(['keywords'])['hits'].max().reset_index().dropna().sort_values(by='hits', ascending=False)


# In[4]:


def plot_most_frequent_wait():
    fig = px.histogram(df_wait[(df_wait['hits']<1)], x="keywords", color= 'keywords', color_discrete_sequence=px.colors.diverging.Portland).update_xaxes(categoryorder="total descending")
    fig.update_layout( title={ 'text':'<b>Most Frequent search terms that are not yet matched </b>','y':0.95, 'x':0.5,'xanchor': 'center','yanchor': 'top'},
                     titlefont=dict(size =28, color='black', family='Old Standard TT, serif'),
                     xaxis=dict(tickfont=dict(family='Old Standard TT, serif', size=20, color='black')))
    fig.show()


# In[5]:


def plot_most_freq_search_term(n=10):
    title='<b> Top '+str(n)+' Most Frequent Search Terms </b>'
    fig = px.bar(df_imp_keywords[:n], x="keywords",y='Users_Count', title=title, color= 'status', color_discrete_sequence=px.colors.qualitative.Vivid).update_xaxes(categoryorder="total descending")
    fig.update_layout( title={'y':0.9, 'x':0.5,'xanchor': 'center','yanchor': 'top'},
                     titlefont=dict(size =28, color='black', family='Old Standard TT, serif'),
                     xaxis=dict(tickfont=dict(family='Old Standard TT, serif', size=20, color='black')))
    fig.show()


# In[6]:


def plot_key_hits_bar(n=30):
    fig = px.bar(key_hits[:n], x="keywords",y='hits', title='<b> Number of Hits per Keyword Searched </b>', color= 'hits', color_discrete_sequence=px.colors.sequential.Inferno).update_xaxes(categoryorder="total descending")
    fig.update_layout( title={'y':0.9, 'x':0.5,'xanchor': 'center','yanchor': 'top'},
                     titlefont=dict(size =28, color='black', family='Old Standard TT, serif'),
                     xaxis=dict(tickfont=dict(family='Old Standard TT, serif', size=20, color='black')))
    fig.show()


# In[7]:


def plot_key_hits_pie(n=10):
    fig = px.pie(key_hits, names="keywords",values='hits', title='<b> Number of Hits per Keyword Searched </b>', color= 'hits', color_discrete_sequence=px.colors.sequential.Agsunset).update_xaxes(categoryorder="total descending")
    fig.update_layout( title={'y':0.9, 'x':0.5,'xanchor': 'center','yanchor': 'top'},
                     titlefont=dict(size =28, color='black', family='Old Standard TT, serif'),
                     xaxis=dict(tickfont=dict(family='Old Standard TT, serif', size=20, color='black')))
    fig.show()



def plot_key_timetomatch(n=30):
    df_sent_time=df_arxiv[df_arxiv['status']=='Sent'][['keywords','last_modified','register_date']].drop_duplicates()
    df_sent_time['sent_time_in_hrs']=((pd.to_datetime(df_sent_time['last_modified']) - pd.to_datetime(df_sent_time['register_date'])).dt.total_seconds()/3600).round(2)
    df_sent_time=df_sent_time.groupby('keywords')['sent_time_in_hrs'].max().reset_index().sort_values(by='sent_time_in_hrs', ascending=False)

    fig = px.bar(df_sent_time[:n], x="keywords",y='sent_time_in_hrs', title='<b> Maximum Time to Get a Match per Keyword </b>', color= 'sent_time_in_hrs').update_xaxes(categoryorder="total descending")
    fig.update_layout( title={'y':0.9, 'x':0.5,'xanchor': 'center','yanchor': 'top'},
                     titlefont=dict(size =28, color='black', family='Old Standard TT, serif'),
                     xaxis=dict(tickfont=dict(family='Old Standard TT, serif', size=20, color='black')))
    fig.show()



