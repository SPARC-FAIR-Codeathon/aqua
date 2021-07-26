
<p align="center">
   <img src="https://github.com/Niloofar-Sh/aqua/raw/main/src/assets/images/Suggestion%26AutoComplete.jpg" alt="interface" width="780" height="500"></br>
  <i> Query refinement by Auto-completion/Suggestions.</i>
</p>
<br/>

# What is the SPARC dataset metadata?
Metadata is the “Data about data”, i.e., additional information provided about datasets. The **SPARC dataset metadata** includes information such as title, description, techniques, as well as the number of the files, formats, licenses, etc. ([SPARC dataset metadata](https://staging.sparc.science/help/3vcLloyvrvmnK3Nopddrka#metadata)).
<br/>
<br/>

# What is the NIFS ontology?
NIF Standard ontology (**NIFS ontology**) is a neuroscience ontology that maintains an extensive set of terms and concepts important for the domains of neuroscience and biology ([NIFS Ontology](https://github.com/SciCrunch/NIF-Ontology)). This a set of community ontologies used by SPARC to annotate data and models.
<br/>
<br/>

# Sections of the "AQUA Query refinement" module



## Suggestions path (purple box):
If there is a typo or removed space between the words of a query, the ElasticSeach might return either no results or irrelevant results. In this case, we need a suggestion and auto-correction feature to improve the quality of the query. 
Merely using SciGraph is not sufficient because SciGraph returns alternative queries/suggestions without correcting the initial query. To improve this process, we have implemented an auto-correction pipeline along with SciGraph to correct the queries before giving suggestions. This includes an *Auto-correction n-gram model* and a Python library *symspellpy*. 
<br/>

### SciGraph

Represents ontologies and ontology-encoded knowledge in a Neo4j graph. SciGraph reads ontologies with owlapi and ingests ontology formats available to owlapi (OWL, RDF, OBO, TTL, etc) ([SciGraph](https://github.com/SciGraph/SciGraph)).

### Auto-correction n-gram model

In spelling correction task, an n-gram is a contiguous sequence of n letters from a given sample of text. An n-gram model is utilised to compare strings and compute the similarity between two words, by counting the number of similar n-grams they share. This technique is language independent. The more similar n-grams between two words exist the more similar they are ([Ahmed et al.](http://www.scielo.org.mx/pdf/poli/n40/n40a7.pdf)). 

### symspellpy

symspellpy is a Python port of SymSpell for spelling correction, fuzzy search and approximate string matching ([symspellpy](https://pypi.org/project/symspellpy/),[SymSpell](https://github.com/wolfgarbe/SymSpell)).

* __Word segmentstion__

``` 
lookup_compound(phrase, max_edit_distance, ignore_non_words=False, transfer_casing=False, split_phrase_by_space=False, ignore_term_with_digits=False)
```

word_segmentation divides a string into words by inserting missing spaces at the appropriate positions misspelled words are corrected and do not affect segmentation existing spaces are allowed and considered for optimum segmentation.

* __Spelling correction__

Supports compound aware automatic spelling correction of multi-word input strings with three cases:

1. mistakenly inserted space into a correct word led to two incorrect terms
2. mistakenly omitted space between two correct words led to one incorrect combined term
3. multiple independent input terms with/without spelling errors <br/>

Find suggested spellings for a multi-word input string (supports word splitting/merging).

## Auto-completion path (yellow path):
It is an added feature to auto-complete the queries while the user is typing. The idea of auto-completion is to prevent typos occuring and to give a better user experience in the SPARC Portal. We have created an n-gram model for auto-completion and utilised a Python library *fast-autocomplete* [fast-autocomplete](https://pypi.org/project/fast-autocomplete/).

### Auto-completion model
The format of the n-gram model needs to be in the following format:

``` 
{
    phrase: [
        context,
        display value,
        count
    ]
}
``` 

* "phrase" can be 1-2 words. 
* The "context" is related to the context of words, for example Anatomy, chemical reactions, proteins, etc. 
* "display value" defines the standard display of the phrase based on the context.
* "count" is the appearance of the phrase in the SPARC dataset and the NIFS ontology.


### Fast auto-complete
The Elasticsearch's Autocomplete suggestor is not fast enough and does not do everything that we need. Consequently, we have utilised fast-autocomplete library which provides us with a much faster process (reducing the auto-completion required time from 900 ms to 30 ms).

# Packages:

1. symspellpy
2. scigraph
3. fast-autocomplete
