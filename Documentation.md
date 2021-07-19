
# Analysis of the existing SPARC search portal

1. Limited search feature of the SPARC Portal:
   It does not recognize nearby words (in case of **typos**). As an example, if we type "rattis" (typo) instead of "rattus", it does not recognize it or give any suggestion (Fig 1).
   | ![rattis_current_result.jpg](https://github.com/Niloofar-Sh/aqua/blob/main/src/assets/images/rattis_current_result.jpg) | 
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

# Objectives for the new SPARC search portal
Specific features have beed added to the new SPARC search portal as listed below:
<br/>
* __Query refinement__:
   * Auto-completion
   * Suggestion
* __Results display__:
   * Improved filtering
* __Additional feature__:
   * ''Notify me" 
<br/>


##  __Query refinement__:

   * Auto-completion:<br/>
      Based on the term, our tool automatically completes the queries if it partially/completely matches any keywords. 
      
   * Suggestion:<br/>
      If no matches are found, it finds close-matches and suggests them to the user with popping up the phrase: *"Did you mean ...?"*
      
The AQUA pipeline for the query refinement on the SPARC portal is shown in Fig 4.
<br/>
   | ![query_refinement](https://github.com/Niloofar-Sh/aqua/blob/main/src/assets/images/query_refinement.jpg) | 
   |:--:| 
   | *Fig 4. AQUA Query refinement pipeline for the SPARC portal.* |
   <br/>

## Suggestion

## Improved filtering

### Keywords
biologocal ....

#### Authors

#### Date


## Notify me

SQLite, Python



### Languages:

    
    
### Query result formats:
Json
    
    


# Platform

# Installation
Docker application on your machine
## Dependencies


## Docker 
(refer to the link ==> lighter)
Easier (if possible) ==> Image on Docker

# Testing

# Examples


 
