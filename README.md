[![Build Status](https://travis-ci.org/kingsdigitallab/dprr-django.svg?branch=develop)](https://travis-ci.org/kingsdigitallab/dprr-django)

# DPRR:  Digital Prosopography of the Roman Republic (DPRR)
## [romanrepublic.ac.uk](romanrepublic.ac.uk)

### Overview

This is the repository for Digital Prosopography of the Roman Republic, currently maintained by [King's Digital Lab](https://github.com/kingsdigitallab/).

This project has been redesigned to run in a Docker container, aimed at an Openstack deployment. 

### Containers:

- [nginx-proxy](https://hub.docker.com/r/nginxproxy/nginx-proxy): This is the primary entry point for the stack, running on 80.  It automatically builds a proxy to other containers.
- [django 3.2](https://hub.docker.com/layers/library/python/3.6-slim-buster/images/sha256-5dd134d6d97c67dd02e4642ab24ecbb9d23059ea018a8b5185784d29dce2f37a?context=explore): The main container for the project (see more detailed description below.) 
- [nginx](https://hub.docker.com/_/nginx): This is the static data container, serving Django's static content.
- db ([Postgres 12.3](https://www.postgresql.org/docs/12/index.html)): The database container for Django above.
- elasticsearch [7.10](https://hub.docker.com/_/elasticsearch): The indexing container, used by Haystack 3.2.1. (Pre-migration, Haystack 2 was using Solr 6.)
- rdf: This container is an encapsulation of a Tomcat server running John Bradley's modified [RDF4J](https://rdf4j.org/) to provide the DPRR dataset as linked open data.  For more information, see the documentation at [DPRRRDF](https://romanrepublic.ac.uk/rdf/doc/index.html)

### ENV file

The compose file will look for deployment variables in a compose/.env file.  Below is a sample file:

```
#Django
DJANGO_READ_DOT_ENV_FILE=True
DJANGO_ALLOWED_HOSTS=
DJANGO_SECRET_KEY=
DJANGO_DEBUG=False

# Elasticsearch
# ------------------------------------------------------------------------------
discovery.type=single-node


# Postgres
# ------------------------------------------------------------------------------
POSTGRES_HOST=db
POSTGRES_PORT=5432
#POSTGRES_DB=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
```

Fill in the database credentials and Django variables.  If deploying via a CI pipeline such as Gitlab, this file will need to be included in its variables (in the KDL setup, we encode this in base64 and add it to the CI/CD variables in the repository settings.)

### Deployment notes

- After deployment, don't forget to run python manage.py update_index to build the Haystack index.  This won't happen automatically.



   

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

##### PDF Export

PDF export will not work when behind http auth. This means it will not work on -dev or -stg, but will work on the live site.

The PDF export needs a virtual X server. If this is not working, ensure the following commands have been run.

* `apt-get install wkhtmltopdf`
* `apt-get install xvfb`
* `echo -e '#!/bin/bash\nxvfb-run -a --server-args="-screen 0, 1024x768x24" /usr/bin/wkhtmltopdf -q $*' > /usr/bin/wkhtmltopdf.sh`
* `chmod a+x /usr/bin/wkhtmltopdf.sh`
* `ln -s /usr/bin/wkhtmltopdf.sh /usr/local/bin/wkhtmltopdf`
