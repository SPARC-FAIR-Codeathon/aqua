# AQUA - Experiment
## About
Experiments of autocomplete and spelling error correction for AQUA SPARC

## How to reproduce experiment results?
[Experiment](Experiment.ipynb)

## How to generate new test collections?
[Test Collections](Data_Test_Generator.ipynb)

## Autocompletion

### Test Collections
We generated two type of autocomplete test collections, [no typo collection](test_autocomplete_pure.json) and [with typo collection](test_autocomplete_typo.json), consists of 200 phrases which are selected from SPARC datasets and NIFS Ontology. The selection process basically is random but still we implement filters to allow more than three character and non numeric phrases only.

### Experiment setup
We compared the performance of AQUA and SPARC's Scigraph to provide autocompletion in the terms of the ability to give suggestion and the execution time.

### Results

<p align="center">
   <img src="https://github.com/napakalas/aqua/blob/aqua_docker/experiment/return_number.png" alt="interface" width="750" height="500"></br>
  <i>Fig 1. Number of completions returned.</i>
</p>

<p align="center">
   <img src="https://github.com/napakalas/aqua/blob/aqua_docker/experiment/execution_time.png" alt="interface" width="750" height="500"></br>
  <i>Fig 2. Execution time analysis.</i>
</p>



## Spelling Error Correction

### Test Collections
We generated test collections by randomly select keywords and authors related to the SPARC data sets, including [biological keywords](query_datatest.json) and [authors](author_datatest.json). Hence, a test collection is a pair of query and a list of the corresponding data sets. Then, we differentiated the test collections based on the number of terms in the query and mimicking typos by performing insertion, deletion, replacement, and spaces removal. In total,there are 31 test collections consisting 50 pairs of query and a list of datasets.

Here are the type of the test collection number of terms in the query we used:
- biological keyword
    - 1 term query
        - no typo
        - 1 deletion
        - 1 insertion
        - 1 replacement
    - 2 terms query
        - no typo
        - 1 deletion
        - 1 insertion
        - 1 replacement
        - no space
        - no space with 1 typo
        - no space with 2 typos
        - no space with 3 typos
        - 3 typos
    - 3 terms query
        - no typo
        - 1 deletion
        - 1 insertion
        - 1 replacement
        - no space
        - no space with 1 typo
        - no space with 2 typos
        - no space with 3 typos
        - 3 typos
- author
    - 1 term query
        - no typo
        - 1 deletion
        - 1 insertion
        - 1 replacement
    - 2 terms query
        - no typo
        - 1 deletion
        - 1 insertion
        - 1 replacement
        - no space

### Experiment setup
We found that the current SPARC search tool uses only the basic features of elastic search, so it can only handle single or double range misspellings such as 'rattusnorvegicus' and 'neromodulation'. Elasticsearch (ES) has a fuzzy search feature that analyzes the query and automatically executes the corrected query. However, its performance seems to suffer when the query consists of more than one typo type. Therefore, AQUA adds an extra layer by creating a pipeline using SymSpellPy to suggest updated queries and then sends them to the ES fuzzy search.

Henceforth, we do not compare the performance of AQUA against the current SPARC search tool because it will be unfair. The tool cannot deal with a complex misspelling such as 'rattunorvegicus', which has one deletion and one replacement, or 'alan garny' and 'marcello bosta', which are the full name of the author. Instead, we compared AQUA to ES and observed whether additional layers could improve retrieval performance. For each test collection, we calculate the Mean Average Precision (MAP) to AQUA and ES. MAP is a standard measurement to represent the performance of an information retrieval system with a range value between 0 and 1, where 1 indicates a perfect system.

### Results


Table 1, shows the Mean Average Precision (MAP) of AQUA and Elasticsearch (ES) over 22 test collections consist of biological keywords as queries. AQUA improves retrieval performance when misspelling occurs in multiple terms queries or misspelling occurs several times. ES is excellent at fixing queries that lose space, even if there is one other typo. However, if there is more than one typo, the performance will be deficient, with a MAP value of 0.057 and 0.18 if there are two or three additional typos in a row. This performance is quite far behind AQUA, which has a MAP of 0.48 and 0.45 for the same addition. Interestingly, AQUA's performance for queries without typos is generally better than ES's.

| Typo            |   ('1 term', 'AQUA') |   ('1 term', 'ES') |   ('2 terms', 'AQUA') |   ('2 terms', 'ES') |   ('3 terms', 'AQUA') |   ('3 terms', 'ES') |
|:----------------|---------------------:|-------------------:|----------------------:|--------------------:|----------------------:|--------------------:|
| 0 typo          |             **0.714785** |           0.711452 |              **0.569673** |           **0.569673**  |              **0.680431** |          0.677097   |
| 1 del           |             0.635935 |           **0.677184** |              **0.555371** |           0.505849  |              **0.668609** |          0.653644   |
| 1 insert        |             0.704785 |           **0.742356** |              0.56559  |           **0.572663**  |              **0.680431** |          0.661312   |
| 1 replace       |             0.644126 |           **0.772202** |              0.548968 |           **0.568364**  |              **0.680431** |          0.646185   |
| no space        |           nan        |         nan        |              0.568006 |           **0.987667**  |              0.667097 |          **0.816667**  |
| no space 1 typo |           nan        |         nan        |              0.559696 |           **0.995918**  |              **0.670508** |          0.0561224  |
| no space 2 typo |           nan        |         nan        |              **0.484005** |           0.0566667 |              **0.644305** |          0.0102041  |
| no space 3 typo |           nan        |         nan        |              **0.446296** |           0.184211  |              **0.589903** |          0.00347222 |
| 3 typo          |           nan        |         nan        |              **0.540761** |           0.481212  |              **0.646919** |          0.621238   |


Table 2 shows the Mean Average Precision (MAP) of AQUA and Elasticsearch (ES) over 9 test collections consisting of authors as queries. AQUA is better to correct a misspelling that appears in a two-term author query. A striking performance difference is AQUA's ability to fix author as a query that loses space where AQUA's MAP is 0.92 while ES is only 0.12.

| Typo      |   ('1 term', 'AQUA') |   ('1 term', 'ES') |   ('2 terms', 'AQUA') |   ('2 terms', 'ES') |
|:----------|---------------------:|-------------------:|----------------------:|--------------------:|
| 0 typo    |             0.863212 |           **0.897673** |              0.926911 |            **0.952778** |
| 1 del     |             0.613025 |           **0.675974** |              **0.818579** |            0.797889 |
| 1 insert  |             0.843871 |           **0.914193** |              0.926944 |            **0.96**     |
| 1 replace |             0.822374 |           **0.867786** |              **0.913039** |            **0.913265** |
| no space  |           nan        |         nan        |              **0.926911** |            0.1245   |
