# AQUA - API

# About

API module for AQUA SPARK

## Searching for datasets
GET datasets based on the provided query
#### Format:

    GET /search?query={query}&force={yes|no}&match={yes|no}

-   query (optional): is a query terms.
-   force (optional): to force the server to execute a refined query or not.
    -   yes : execute the refined query.
    -   no (default): execute the original query.
-   match : to signal the server to identify datasets with full query phrase or not.
    -   yes : return datasets having the query phrase.
    -   no (default): return dataset having at least one term of the query phrase.

#### Examples:

-   A GET request without additional arguments will return all datasets
    -   `http://130.216.216.55/search`
-   Example of query: `rat`
    -   `http://130.216.216.55/search?query=rat`
        -   since `rat` is available, query `rat` is executed
-   Example of query: `rattis`
    -   `http://130.216.216.55/search?query=ratis`
        -   since `rattis` is not available, it is refined to `rattus`
        -   `rattus` is executed
    -   `http://130.216.216.55/search?query=ratis&force=yes`
        -   `rattis` is executed since `force` is set to `yes`
        -   no datasets returned since `rattis` is not available in all datasets
-   Example of query: `rattisnorvegicu`
    -   `http://130.216.216.55/search?query=rattis%20norvegicu&match=yes`
        -   `rattisnovergicu` is segmented to `rattis norvegicu`
        -   `rattis norvegicu` is refined to `rattus norvegicus`
        -   `rattus norvegicus` is executed
        -   since `match` is `yes`, only datasets having phrase `rattus norvegicus` are returned.

#### Return example:

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
        "status": {
          "public": ["10", "12", "9", ...],
          "embargoed": ["137"]
        }
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

### Autocomplete using fast_autocomplete
GET autocomplete from fast-autocomplete
#### Format:

    GET /autocomplete?query=query&limit={limit}

-   query (mandatory): is a query terms
-   limit (optional): the number of returns (default = 10)

#### Example:

-   Example of query: `ratt`
    -   `http://130.216.216.55/autocomplete?query=ratt&limit=10`
        -   get the autocomplete of ratt as a list
        -   return 10 phrases
    -   `http://130.216.216.55/autocomplete?query=ratt`
        -   get the autocomplete of ratt as a list

#### Return example:
    ["rattus","rattlesnake","rattle","rattle virus","ratti","rattus rattus","rattus norvegicus","rattay","rattails","rattus sp"]

### Autocomplete using SciGraph
GET autocomplete from SciGraph
#### Format:

    GET /autocomplete_sc?query=query&limit={limit}

-   query (mandatory): is a query terms
-   limit (optional): the number of returns (default = 10)

#### Example:

-   Example of query: `ratt`
    -   `http://130.216.216.55/autocomplete_sc?query=ratt&limit=10`
        -   get the autocomplete of ratt as a list
        -   return 10 phrases
    -   `http://130.216.216.55/autocomplete_sc?query=ratt`
        -   get the autocomplete of ratt as a list

#### Return example:
    ["rattails","rattle","rattus","rattus leucopus","rattus muelleri","rattus norvegicus","rattus norvegicus genome","rattus norvegicus8","rattus norwegicus"]

## Get query suggestions
GET autocorrection from symspellpy pipeline and suggestions from SciGraph
#### Format:

    GET /suggestions?query=query&limit={limit}

-   query (mandatory): is a query terms
-   limit (optional): the number of returns (default = 10)

#### Example:

-   Example of query: `rattus`
    -   `http://130.216.216.55/suggestions?query=rattus&limit=10`
        -   get the suggestion of rattus as a list
        -   return 10 phrases
    -   `http://130.216.216.55/suggestions?query=rattus`
        -   get the suggestion of rattus as a list

#### Return example:
    ["rattus","rattle","rattus sp.","rousettus"]

## NotifyMe
POST email and keywords to get notification for new datasets
#### Format:

    curl -d “email=email_address&keywords=keywords”

- email: the registrating email
- keywords: the topic keywords to match to new datasets

#### Return:
      - {'success':'true|false'}
