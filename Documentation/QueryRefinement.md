
<p align="center">
   <img src="https://github.com/Niloofar-Sh/aqua/raw/main/src/assets/images/Suggestion%26AutoComplete.jpg" alt="interface" width="780" height="500"></br>
  <i>Fig 5. Query refinement by Auto-completion/Suggestions.</i>
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
To give suggestions to the users, we have utilised SciGraph, which provides basic "vocabulary" support. To improve the suggestions component of our "Query refinement" module, we have also implemented another parallel path, including an *Auto-correction n-gram model* and a Python library *symspellpy*. 
<br\>

### SciGraph

Represents ontologies and ontology-encoded knowledge in a Neo4j graph. SciGraph reads ontologies with owlapi and ingests ontology formats available to owlapi (OWL, RDF, OBO, TTL, etc) ([SciGraph](https://github.com/SciGraph/SciGraph)).

### Auto-correction n-gram model

In spelling correction task, an n-gram is a contiguous sequence of n letters from a given sample of text. An n-gram model is utilised to compare strings and compute the similarity between two words, by counting the number of similar n-grams they share. This technique is language independent. The more similar n-grams between two words exist the more similar they are ([Ahmed et al.](http://www.scielo.org.mx/pdf/poli/n40/n40a7.pdf)). 

### symspellpy

symspellpy is a Python port of SymSpell for spelling correction, fuzzy search and approximate string matching ([symspellpy](https://pypi.org/project/symspellpy/),[SymSpell](https://github.com/wolfgarbe/SymSpell)).

* __Word segmentstion__

   word_segmentation divides a string into words by inserting missing spaces at the appropriate positions misspelled words are corrected and do not affect segmentation existing spaces are allowed and considered for optimum segmentation.

* __Spelling correction__

   Supports compound aware automatic spelling correction of multi-word input strings with three cases:

   1. mistakenly inserted space into a correct word led to two incorrect terms
   2. mistakenly omitted space between two correct words led to one incorrect combined term
   3. multiple independent input terms with/without spelling errors
   Find suggested spellings for a multi-word input string (supports word splitting/merging).

## Auto-completion path (yellow path):

### Auto-completion model

### Fast auto-complete


# Packages:

1. symspellpy
2. scigraph
3. ???
