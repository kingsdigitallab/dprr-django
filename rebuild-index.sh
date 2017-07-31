#!/bin/bash

./manage.py build_solr_schema > schema.xml
sudo mv schema.xml /opt/solr/collection1/conf/
sudo service tomcat7 restart
./manage.py rebuild_index --noinput