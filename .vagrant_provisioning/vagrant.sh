#!/usr/bin/env bash

# Update apt sources
sudo echo 'deb http://apt.postgresql.org/pub/repos/apt/ wheezy-pgdg main' >> /etc/apt/sources.list
sudo wget -O- https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
apt-get update

apt-get -y install vim-nox emacs

apt-get -y install zsh
sudo su - vagrant -c 'wget --no-check-certificate https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | sh'
sudo chsh -s /bin/zsh vagrant

apt-get -y install mercurial adminer

# VM specific packages
apt-get -y install python-dev python-setuptools
sudo easy_install pip
sudo pip install virtualenv

apt-get -y install binutils libproj-dev gdal-bin
apt-get -y install postgresql-9.3 postgresql-client-9.3 libpq-dev postgresql-contrib-9.3

apt-get -y install libjpeg-dev
apt-get -y install libldap-dev libsasl2-dev
apt-get -y install libxml2-dev libxslt1-dev
apt-get -y install redis-server

# Java and SOLR
sudo apt-get -y install openjdk-7-jdk
mkdir /usr/java
ln -s /usr/lib/jvm/java-7-openjdk-amd64 /usr/java/default

wget http://mirror.catn.com/pub/apache/lucene/solr/4.10.4/solr-4.10.4.tgz
tar xvzf solr-4.10.2.tgz
rm solr-4.10.2.tgz
sudo mv solr-4.10.2/ /usr/share/


sudo su - postgres -c "psql -c \"create user vagrant with superuser password 'vagrant';\""
sudo su - postgres -c "psql -c \"create user app_dprr password 'app_dprr';\""
sudo su - postgres -c "createdb app_dprr_local -E UTF-8 -T template0 -O app_dprr"
sudo su - postgres -c "psql app_dprr_local < /vagrant/.vagrant_provisioning/dprr.db"
sudo su - postgres -c "psql app_dprr_local -c \"grant all on database app_dprr_local to app_dprr;\""

for tbl in `sudo su - postgres -c "psql -qAt -c \"select tablename from pg_tables where schemaname = 'public';\" app_dprr_local"`;
do  sudo su - postgres -c "psql -c \"alter table $tbl owner to app_dprr;\" app_dprr_local"
done

for tbl in `sudo su - postgres -c "psql -qAt -c \"select sequence_name from information_schema.sequences where sequence_schema = 'public';\" app_dprr_local"`;
do  sudo su - postgres -c "psql -c \"alter table $tbl owner to app_dprr;\" app_dprr_local"
done

for tbl in `sudo su - postgres -c "psql -qAt -c \"select table_name from information_schema.views where table_schema = 'public';\" app_dprr_local"`;
do  sudo su - postgres -c "psql -c \"alter table $tbl owner to app_dprr;\" app_dprr_local"
done

# copies the local_settings file to the DPRR settings folder
cp /vagrant/.vagrant_provisioning/local_settings.py /vagrant/dprr/settings/local.py


virtualenv /home/vagrant/venv
source /home/vagrant/venv/bin/activate

pip install -r /vagrant/requirements/dev.txt
pip install -U wagtail==0.7
pip install -U django==1.7.5
pip install -U django-compressor==1.4
pip install -U libsass==0.5.1
pip install -U django-libsass==0.3

python /vagrant/manage.py migrate
sudo chown -R vagrant /home/vagrant/venv/
