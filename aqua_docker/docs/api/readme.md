# AQUA - API

# About

API module for AQUA SPARK

## Searching for datasets

#### Format:

    GET /search?query={query}&force={yes|no}

-   query : is a query terms (optional)
-   force : an argument to force the server to execute the query
    -   yes : the query is not modify
    -   no : the query is modified if results are not found
-   match : an argument to exacute search datasets having exact query string.

#### Examples:

-   A GET request without additional arguments will return all datasets
    -   `http://130.216.216.55/search`
-   Example of query: `rat`
    -   `http://130.216.216.55/search?query=rat`
        -   since `rat` is available, query `rat` is executed
-   Example of query: `rattis`
    -   `http://130.216.216.55/search?query=ratis`
        -   since `rattis` is not available, it is corrected to `rattus`
        -   `rattus` is executed
    -   `http://130.216.216.55/search?query=ratis&force=yes`
        -   although `rattis` is not available, it is forced to execute
        -   no results
-   Example of query: `rattis norvegicu`
    -   `http://130.216.216.55/search?query=rattis%20norvegicu&match=yes`
        -   `rattis novergicu` is corrected to `rattus norvegicus`
        -   `rattus norvegicus` is executed
        -   returning datasets having phrase `rattus norvegicus`

#### Return format:

    {
      "query": "rattus",
      "executed": "rattus",
      "force": "no",
      "match": "no",
      "suggestions": ["rattle", "rattus sp.", "rousettus"],
      "total": 27,
      "filters": {
      "keywords": {
        "vagus nerve stimulation": ["60", "16", "9"],
        },
      "authors": {
        "Terry Powley": ["10", "12", "9", "123", "107", "90", "11", "24", "121"],
        ....
        }
      },
      "sorts": {
        "ranking": ["29", "60", "20", "16", "21", "10", "12", "9", "139", "123", "77", "51", "107", "88", "90", "130", "37", "31", "11", "106", "48", "24", "121", "52", "151", "62", "105"],
        "date": ["151", "139", "105", "130", "123", "121", "107", "106", "90", "60", "88", "77", "37", "16", "51", "29", "12", "11", "10", "62", "20", "21", "52", "24", "31", "9", "48"],
        "name": ["51", "31", "48", "77", "52", "130", "123", "105", "62", "106", "9", "37", "107", "121", "29", "90", "151", "20", "21", "139", "16", "60", "88", "10", "11", "12", "24"]
      },
      "hits": {
        "29": {
          "url": "https:\/\/sparc.science\/datasets\/29",
          "banner": "https:\/\/assets.discover.pennsieve.io\/dataset-assets\/29\/6\/revisions\/1\/banner.jpg",
          "_id": "DOI:10.26275\/xmyx-rnm9",
          "_score": 1.1826954,
          "firstPublishedAt": "2019-07-19T23:20:23.12942Z",
          "updatedAt": "2021-06-23T07:25:53.105281Z",
          "name": "Molecular Phenotype Distribution of Single Rat ICN Neurons",
          "description": "We developed an approach to appreciating ... .",
          "readme": {
            "description": "**Study purpose:** The purpose of this study ... ."
          }
          "samples": "151",
          "subjects": "1",
          "anatomy": ["heart"],
          "organisms": ["Rattus norvegicus"],
          "publication": "true",
          "techniques": ["euthanasia technique", "dissection technique", "tissue fixation technique", "staining technique", "computational technique"],
          "embargoed": "false",
          "highlight": {
            "name":[...],
            "description":[...],
            "readme":[...]
            }
        },
        "60": { .... },
        ....
      }
    }

## Get query autocomplete

#### Format:

    GET /autocomplete?query=query&limit={limit}&verbose={yes|no}

-   query : is a query terms (mandatory)
-   limit : the number of returns
-   verbose :
    -   no : get list of autocomplete
    -   yes : get detail autocomplete in json format

#### Results:
    ["rat","rattus norvegicus","brown rat","norway rat","rattus sp. strain wistar","rattus rattiscus","rattus norwegicus","rats","rattus norvegicus8","gunn rats","rattus"]

#### Example:

-   Example of query: `rat`
    -   `http://130.216.216.55/autocomplete?query=rat&limit=10`
        -   get autocomplete of rat as a list
        -   return 10 phrases
    -   `http://130.216.216.55/autocomplete?query=rat`
        -   get autocomplete of rat as a list
    -   `http://130.216.216.55/autocomplete?query=rat&limit=10&verbose=true`
        -   get autocomplete of rat as a detail dictionary
        -   return 10 phrases

## Get query suggestions

#### Format:

    GET /suggestions?query=query&limit={limit}

-   query : is a query terms (mandatory)
-   limit : the number of returns

#### Example:

-   Example of query: `rat`
    -   `http://130.216.216.55/suggestions?query=rat&limit=10`
        -   get autocomplete of rat as a list
        -   return 10 phrases
    -   `http://130.216.216.55/suggestions?query=rat`
        -   get autocomplete of rat as a list

#### Results:
    ["rat","brat","rate","rmat","cat","ras"]
