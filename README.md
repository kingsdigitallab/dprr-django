
Requirements
=====
Python/Django requirements inside the requirements directory.




Loading the data
=====


Promrep Seed data
====

```
# loading the fixtures

python manage.py runscript promrep.init_data
```


Loading MRR1
====

```
python manage.py runscript promrep.add_mrr1_data -v3
```

- v3 enables a more verbose output

Loading MRR2
====


Running the tests
====

```
    python manage.py test promrep.scripts.test_parsing_aux

```

