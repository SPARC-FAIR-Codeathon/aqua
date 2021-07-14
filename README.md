# AQUA
### An Advanced QUery Architecture for the SPARC Portal

## Table of Contents

* [Introduction](#introduction)
* [About us](#about-us)
* [Problem](#problem)
* [AQUA solution](#aqua-solution)
* [How it works](#how-it-works)
* [Documentation](#documentation)
* [Developers](#developers)

## Introduction

In today's world where information retrieval is expected in a matter of miliseconds, a strong search engine is essential. Take Google and Facebook, 2 of the five most popular search engines in the world, for example. Every day, millions or even billions of queries are made, potentially with typos and close-matches. Facebook returns suggestions for a profile name we fuzzily search but do not know for sure. Google returns to us not only what we want, but also tons of related information. In the medical research world, unless published datasets are easy to find, their potential for reuse and collaboration will be limited. A search engine serves as the middleman between scientific discovery and scientific progress in that sense. The stronger and smarter the search engine is, the faster the progress.

## About us

AQUA is an application that aims at improving the search capabilities of the [SPARC Portal](https://sparc.science/). In particular, we are looking to make the search engine smarter at reading and understanding user input as search keywords. We also enhance the result display feature of the SPARC Portal by making it more user-friendly and providing users with more sophisticated result filtering and sorting options. Our end goal is to improve exponentially the visibility of the SPARC datasets. This in turn will benefit the SPARC community as a whole since their datasets will be more discoverable for reuse and subsequent collaboration. This project was created during the 2021 SPARC FAIR Codeathon.

## Problem

Currently, the search feature of the SPARC Portal is very limited: 

1) It does not account for nearby words. E.g.: when a word is misspelled.

2) The result display is primitive. E.g.: Limited result filtering, or matched text results are not highlighted.

## AQUA solution

1) Apply Artificial Intelligence tools (Natural Language Processing) to the processing of users’ search keywords and to the implementation of predictive typing (suggestion-based typing). 

- In details, in addition to lemmatization, other NIH tools (e.g: NIF Ontology) will be used to derive origins of words and make suggestions for users as they type. This will help AQUA standardize various user inputs and return the most datasets possible that match the search keywords.

2) Enhance the current result display by:

- Bolding/highlighting matched texts in results for easy lookup

- Add a more sophisticated Dataset results filter functionality (based on Relevance, Date of Publication, and other customized filtering) to the current portal.

- Add a “Notify me when related datasets are published” when “No results” are returned. This will allow users to enter their email to be stored by the SPARC Portal for future alerts. 

## How it works


<p align="left">
  <img src="https://github.com/SPARC-FAIR-Codeathon/aqua/raw/main/src/assets/images/workflow.JPG" alt="interface" width="600" height="300"> 
  <br/> 
  </img>
</p>

## Documentation

For a detailed documentation of our application, please visit here.

## Developers

- Tram Ngo 
- Laila Rasmy
- Niloofar Shahidi
- Yuda Munarko
- Xuanzhi
