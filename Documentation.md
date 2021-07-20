# Application name:

<p align="center">
  <img src="https://github.com/Niloofar-Sh/aqua/blob/main/src/assets/images/logo_aqua-1.jpg" alt="interface" width="500" height="300"> 
  <br/> 
  </img>
</p>

# Analysis of the existing SPARC search portal

1. Limited search feature of the SPARC Portal:
   It does not recognize nearby words (in case of **typos**). As an example, if we type "rattis" (typo) instead of "rattus", it does not recognize it or give any suggestion (Fig 1).
   | ![rattis_current_result](https://github.com/Niloofar-Sh/aqua/blob/main/src/assets/images/rattis_current_result.jpg) | 
   |:--:| 
   | *Fig 1. Search results for a typo (rattis) on the SPARC portal.* |
   <br/>
2. You need to enter the exact correct keywords in the search bar (Fig 2) and yet, it does not **highlight the keywords** of your query among the search results.
   
   | ![rattus_current_result](https://github.com/Niloofar-Sh/aqua/blob/main/src/assets/images/rattus_current_result.jpg) | 
   |:--:| 
   | *Fig 2. Search results for a correct keyword (rattis) on the SPARC portal. Keywords are not highlighted in the results.* |
   <br/>
   
3. Limited **filterings** on the results display page, i.e., sorting based on the date of publication, author, and alphabetical order. The website currently refines the results by either being "Public" or "Embargoed" (Fig 3).

   | ![rattus_filters](https://github.com/Niloofar-Sh/aqua/blob/main/src/assets/images/rattus_filters.jpg) | 
   |:--:| 
   | *Fig 3. Limited filterings for the results display on the SPARC portal.* |
   <br/>
   
4. In case of no results being found for the queries, there is no way for the user to get informed on whether a **new dataset/resource** (related to their query) has been published on the SPARC portal or not.
<br/>

# AQUA objectives for the new SPARC search portal
Specific features of AQUA are listed below:
<br/>
* __Query refinement__
   * Auto-completion:<br/>
      Based on the term, our tool automatically completes the queries if it partially/completely matches any keywords. It then sends the selected keyword to AQUA backend.
   * Suggestion:<br/>
      If no exact matches are found, it finds close-matches and suggests them to the user with popping up the phrase: *"Did you mean ...?"*. Otherwise, it will send the raw and uncorrected query to AQUA backend.

* __Results filtering__
   * Sort by:<br/>
      When the results for the query are displayed, user will have the option of sorting them based on the *Relevance*, *Date published*, and *Alphabetical order*.
    * Filter by:<br/>
      The results can also be filtered based on *Keyword*, *Author*, and *Category*.
    * Matched text bolded/highlighted
    
    
* __Additional feature__
   * ''Notify me":<br/>
      At the end, if no results are returned by the AQUA backend, our tool asks the user if they want to get notified when a related resource is published or not. For a given email address, the tool checks for its validity and then stores it using SQLite. Thereafter, it will check for any updated/uploaded related resource on the SPARC portal everyday at 2AM EDT. In case of the requested resource availability, it sends a notification email to the registered user. 
Fig 4 demonstrates the AQUA pipeline.
<br/>

| <img src="https://github.com/Niloofar-Sh/aqua/blob/main/src/assets/images/workflow_aqua.jpg" alt="interface" width="550" height="1000">| 
   |:--:| 
   | *Fig 4. AQUA pipeline including three major sections: Query refinement, Results filtering, and Notify me.* |
   <br/>


# Platform
The AQUA platform integrates Python libraries, data mining tools, a SQL database engine, and Document Object Model (DOM) API to mimic an environment similar to the SPARC search portal with an improved functionality in multiple ways. In general, the AQUA platform consists of a presentation layer as the User Interface (UI) (referred to as frontend) and a server-side data-access layer (referred to as backend). The **AQUA UI** and the **AQUA Backend** bridge between the user and the Knowledge Management Core (K-Core) database. K-Core is the SPARC knowledge graph database.


## AQUA Backend
<br/>
The AQUA backend includes querying the K-Core database for information, delivering data to the frontend, and processing any logic that the AQUA UI requires. The main tools utilised for the AQUA Backend are Python (Jupyter Lab), Docker, SQLite, and SciGraph.
<br/>
The AQUA backend focuses on two main features:
<br/>
*__Query refinement by Auto-completion/Suggestions__ (To read more visit: Yuda Readme)  
<br/>
*__Email notification by the "Notify me" module__ (To read more visit: Laila Readme)

## AQUA UI
<br/>
AQUA UI receives the user's queries, formulates them, and transfers to the AQUA Backend module. When the response from the AQUA backend is received, the AQUA UI interprets it and displays the content on the screen. The AQUA UI is constructed using VueJS and implemented by the HTML-CSS-JS trio. 

# How to use AQUA?
blah blah blah

## Installation
You can setup and deploy the Docker module for AQUA by following the steps in: [AQUA Docker](https://github.com/Niloofar-Sh/aqua/tree/main/aqua_docker#readme)
## Dependencies

[Docker](https://www.docker.com/) is a platform that bundles and delivers software in packages called containers.


## Docker 
(refer to the link ==> lighter)
Easier (if possible) ==> Image on Docker

# Testing

# Examples
Here, we have provided examples of how AQUA improves the search experience in two scenarios, i.e.:  <br/>
1) AQUA auto-completion feature helps the user find a correct keyword while typing (Fig 5), and
2) AQUA suggests close-matches for a query with typo (Fig 6).  
The user's decision to either select one of the close-matches or go with thier raw, uncorrected query leads to "Result(s) display" or "No results" notification (Fig 7). When at least one result is returned, AQUA displays options to sort or filter the results. This is shown with an example in Fig 8.

 
