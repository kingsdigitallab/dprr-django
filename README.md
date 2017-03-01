[![Build Status](https://travis-ci.org/kingsdigitallab/dprr-django.svg?branch=develop)](https://travis-ci.org/kingsdigitallab/dprr-django)

### Requirements

Python/Django requirements can be found in the `requirements.txt` file.

### Setting up 

#### Cloning the project 

 `git clone -b develop --recursive git@github.com:kingsdigitallab/dprr-django.git`

The above command will clone the development branch, as well as all the submodules.  

### Project Structure 

The main application is `promrep`. 

#### Faceting 

Given that the desired output is a list of Persons, we need to Group the results by person. To do that we use a common field to all Assertion index objects, the `person_id`. We’re also using different indexes to reflect the different Assertion types. The queryset is defined in the `promrep/forms.py` file: 

```python
queryset = GroupedSearchQuerySet().models(
    PostAssertion,
    StatusAssertion,
    RelationshipAssertion).group_by('person_id')
```

##### Grouping Facets

Given that we wish to search on the Assertions but list Persons we opted to use the SOLR Grouping/Field collapsing feature: 
* See http://wiki.apache.org/solr/FieldCollapsing for the Solr feature

This is currently unsupported by Haystack. We're using an experimental backend for Haystack 2.0 adapted from the following code:
* See https://gist.github.com/3750774 for the current version of this code

The backend code can be found on `promrep/solr_backends/solr_backend_field_collapsing`. 

##### Adding a new facet

Add the new facet to the `search_index.py` file, following Haystack’s documentation. 

There are 4 types of index classes: 
* GenericIndex 
* PostAssertionIndex
* StatusAssertionIndex
* RelationshipAssertionIndex

After adding the new field to the search_indexes file (as well as the prepare method, if needed), you need to:
* rebuild the SOLR schema xml file (overwriting the `schema.xml` in the solr config folder)
* restart Tomcat
* rebuild the index (using the management command `python manage.py rebuild_index`)

To add the facet to the frontendend, add the facet field to either the `facet_fields` or the `autocomplete facets` lists in the `PromrepFacetedSearchView` (`promrep/views.py`). These lists will be used by the `.facet()` function. These are also used in the template to control how to display the facet.

##### Hierarchical lists

Some authority lists are hierarchical -- see the Office and Province models, for instance. These were developed using the `django-mptt` library: 

https://github.com/django-mptt/django-mptt 

In order to display them correctly all hierarchical model objects need to exist in the template. This is currently done in the `views.py` file, where each model is added to the context (`get_context_data`). In the template we use MPTT `recursetree` tag to recurse the tree and display each node.  

#### Scripts and data 

There are various scripts in the `promrep/scripts` folder. Most were written to be used only once to load data in the staging database. The data itself (usually `csv` files created by the project partners) is not stored on the server but, for provenance reasons, all scripts refer to the name/version of the data file that was loaded into the database.

##### Management Scripts

* `add_highest_office`: script that adds the `highest_office` field to all persons on the database. The script checks if the `highest_office_edited` field is False and, if so, overwrites it;
* `add_senator_statusassertions`: # this script enriches the database with the Senator StatusAssertions; for full rules and dicussion please see the [original JIRA ticket]( https://jira.dighum.kcl.ac.uk/projects/DPRR/issues/DPRR-256). Only adds/removes StatusAssertions if the person doesn't have any Senatorial StatusAssertions flagged as `is_verified` (defaults to False). 
