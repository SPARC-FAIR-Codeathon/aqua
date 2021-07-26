<p align="center">
  <img src="https://github.com/SPARC-FAIR-Codeathon/aqua/raw/main/src/assets/images/logo_aqua-1.jpg" alt="interface" width="420" height="250"> 
  <br/> 
  </img>
</p>

## Table of Contents

* [About AQUA](#about-aqua)
* [The Problem](#the-problem)
* [AQUA solution](#aqua-solution)
* [How it works](#how-it-works)
* [How to install](#how-to-install)
* [Documentation](#documentation)
* [Developers](#developers)

## About AQUA

AQUA (Advanced QUery Architecture for the SPARC Portal) is an application that aims at improving the search capabilities of the [SPARC Portal](https://sparc.science/). In particular, we are looking to make the search engine smarter at reading and understanding user input as search keywords. We also enhance the result display feature of the SPARC Portal by making it more user-friendly and providing users with more sophisticated result filtering and sorting options. Our end goal is to improve exponentially the visibility of the SPARC datasets. This in turn will benefit the SPARC community as a whole since their datasets will be more discoverable for reuse and subsequent collaboration. This project was created during the 2021 SPARC FAIR Codeathon.

## The Problem

Currently, the search feature of the SPARC Portal is very limited: 

1) It does not recognize nearby words (typos and close-matches) or synonyms.

2) The result display is limited. E.g.: Limited result filtering and sorting (only by Published Date or Alphabetical Ordered Titles).

## AQUA solution

1) Apply Artificial Intelligence tools (Natural Language Processing) to the processing of users’ search keywords and to the implementation of predictive typing (suggestion-based typing). 

- In details, in addition to lemmatization, other NIH tools (e.g: NIF Ontology) will be used to derive origins of words and make autocomplete suggestions for users as they type. This will help AQUA standardize various user inputs and return the most datasets possible that match the search keywords.
- AQUA also fixes typos and close matches and suggests corrected search keywords.

2) Enhance the current result display by:

- Bolding/highlighting matched texts in results for easy lookup

- Add a more sophisticated Dataset results sorting and filtering functionality (based on Relevance, Date of Publication, and other customized filtering) to the current portal.

- Add a “Notify me when related datasets are published”. This will allow users to enter their email to be stored by the SPARC Portal for future alerts. 

## How it works

<p align="left">
  <img src="https://github.com/SPARC-FAIR-Codeathon/aqua/raw/main/src/assets/images/workflow_new.jpg" alt="interface" width="850" height="470"> 
  <br/> 
  </img>
</p>
 
## How to install

**Step 1:** Git clone the AQUA project: `git clone https://github.com/SPARC-FAIR-Codeathon/aqua.git`

**Step 2:** Go into the `aqua` directory and run the following commands:

```
# install dependencies
$ yarn install

# serve with hot reload at localhost:3000
$ yarn dev

# build for production and launch server
$ yarn build
$ yarn start

```

## Documentation

For a detailed user documentation of our application, please visit [documentation](https://github.com/SPARC-FAIR-Codeathon/aqua/blob/main/Documentation/Documentation.md).

## Developers

- [Tram Ngo](https://github.com/tramngo1603) (Lead)
- [Laila Rasmy](https://github.com/lrasmy) (Sysadmin)
- [Niloofar Shahidi](https://github.com/Niloofar-Sh) (Technical writer)
- [Yuda Munarko](https://github.com/napakalas) (Sysadmin)
- [Xuanzhi](https://github.com/marcusLXZ) (Front-end)
