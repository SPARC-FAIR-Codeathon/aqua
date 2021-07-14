# AQUA
### An Advanced QUery Architecture for the SPARC Portal

# Introduction

In today's world where information retrieval is expected in a matter of miliseconds, a strong search engine is essential. Take Google and Facebook, 2 of the five most popular search engines in the world, for example. Every day, millions or even billions of queries are made, potentially with typos and close-matches. Facebook returns suggestions for a profile name we fuzzily search but do not know for sure. Google returns to us not only what we want, but also tons of related information. In the medical research world, unless published datasets are easy to find, their potential for reuse and collaboration will be limited. A search engine serves as the middleman between scientific discovery and scientific progress in that sense. The stronger and smarter the search engine is, the faster the progress.

# Problem

Currently, the search feature of the SPARC Portal is very limited: 

1) It does not account for nearby words. E.g.: when a word is misspelled.

2) The result display is primitive. E.g.: Limited result filtering, or matched text results are not highlighted.

# Solution

1) Apply Artificial Intelligence tools (Natural Language Processing) to the processing of users’ search keywords and to the implementation of predictive typing (suggestion-based typing). 

- In details, in addition to lemmatization, other NIH tools (e.g: NIF Ontology) will be used to derive origins of words and make suggestions for users as they type. This will help AQUA standardize various user inputs and return the most datasets possible that match the search keywords.

2) Enhance the current result display by:

- Bolding/highlighting matched texts in results for easy lookup

- Add a more sophisticated Dataset results filter functionality (based on Relevance, Date of Publication, and other customized filtering) to the current portal.

- Add a “Notify me when related datasets are published” when “No results” are returned. This will allow users to enter their email to be stored by the SPARC Portal for future alerts. 

# Workflow 


<p align="left">
  <img src="https://github.com/SPARC-FAIR-Codeathon/aqua/raw/main/src/assets/images/workflow.JPG" alt="interface" width="600" height="300"> 
  <br/> 
  </img>
</p>


