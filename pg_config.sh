apt-get -qqy update
apt-get -qqy install libpq-dev python-pip python-dev postgresql postgresql-contrib git-all python-django python-psycopg2

sudo pip install --upgrade django==1.11.5
sudo pip install --upgrade psycopg2==2.7.3.1

sudo -u postgres psql -c "CREATE USER developer WITH PASSWORD 'insecurepassword';"
sudo -u postgres psql -c "ALTER ROLE developer CREATEDB;"
sudo -u postgres psql -c "CREATE DATABASE wikiserver;"

python /vagrant/researchproject/manage.py makemigrations
python /vagrant/researchproject/manage.py migrate

sudo -u postgres psql wikiserver -c "insert into auth_user(username, first_name, last_name, email, password, is_superuser, is_staff, is_active, date_joined) values('TestUser01', '', '', '', 'insecurepassword', false, false, true, 'today');"
sudo -u postgres psql wikiserver -c "insert into auth_user(username, first_name, last_name, email, password, is_superuser, is_staff, is_active, date_joined) values('TestUser02', '', '', '', 'insecurepassword', false, false, true, 'today');"

sudo -u postgres psql wikiserver -c "insert into wikiserver_post(owner_id, title, content, pub_date) values('1', 'Lorem', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed pulvinar suscipit augue, vitae auctor nisi porta sed. Pellentesque imperdiet tellus a eleifend tempor. Proin vehicula arcu id nunc pretium finibus. Praesent tincidunt est nec nisl tempor, eu rutrum purus gravida. Nunc nec erat massa. Morbi lobortis, tellus at tristique rutrum, eros nisl aliquam nulla, eu accumsan justo dui sed sem. Mauris suscipit justo est, nec aliquam sapien tempus a. Nulla fermentum ut nunc non commodo. Maecenas suscipit lorem sed ante facilisis vulputate. Maecenas iaculis nisi justo, ac accumsan augue tristique vitae. Mauris magna ex, molestie ac tellus in, mollis sollicitudin ligula. Vestibulum a mollis elit. Vivamus eu luctus est. Pellentesque consequat erat nec felis pulvinar tristique. Proin ac nunc semper, interdum magna vitae, egestas orci. Donec pulvinar odio at facilisis congue. Quisque massa risus, commodo quis accumsan non, consectetur in lectus. Donec eu velit eu ipsum ultrices dictum ut vitae neque. Cras at interdum nunc, ac sollicitudin lacus. Pellentesque porttitor maximus turpis in pretium. Suspendisse dolor eros, aliquam quis finibus ultricies, sagittis sollicitudin lorem. Sed tincidunt enim magna, ut convallis metus accumsan ut. Mauris eu libero in nibh tempus maximus. Aenean sit amet orci interdum, scelerisque eros non, placerat nisl. Duis id gravida orci. Donec eu malesuada felis. Phasellus at felis aliquam, blandit urna eu, dignissim erat. Fusce suscipit lacinia turpis ac laoreet.', 'today');"
sudo -u postgres psql wikiserver -c "insert into wikiserver_post(owner_id, title, content, pub_date) values('1', 'Ipsum', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum a ligula sit amet tortor sagittis tincidunt non eu eros. Suspendisse potenti. Morbi pulvinar fringilla eros, id faucibus elit ultricies ac. Nam auctor efficitur purus convallis porttitor. Fusce lacinia nulla vel ligula mollis scelerisque. Ut iaculis porttitor commodo. Fusce nec elit orci. Donec cursus et urna id faucibus. Vivamus rutrum facilisis lorem, ac euismod diam scelerisque ac. Ut faucibus neque vel quam lacinia condimentum. Maecenas non magna non augue congue faucibus. In semper arcu ut nibh porttitor bibendum. Nulla gravida non augue ut faucibus.', 'today');"
sudo -u postgres psql wikiserver -c "insert into wikiserver_post(owner_id, title, content, pub_date) values('1', 'Roots', 'Maecenas mauris ligula, dignissim quis sodales vitae, tincidunt sit amet ante. Nunc magna felis, aliquet vitae pretium sit amet, interdum ut erat. Nullam vehicula mollis sollicitudin. Phasellus convallis non nisl at posuere. Integer venenatis odio sed dolor cursus bibendum. Morbi aliquam risus id dapibus fringilla. Aenean aliquam vehicula tellus. Fusce porta ultricies posuere.', 'today');"
sudo -u postgres psql wikiserver -c "insert into wikiserver_post(owner_id, title, content, pub_date) values('2', 'Dolor', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum a ligula sit amet tortor sagittis tincidunt non eu eros. Suspendisse potenti. Morbi pulvinar fringilla eros, id faucibus elit ultricies ac. Nam auctor efficitur purus convallis porttitor. Fusce lacinia nulla vel ligula mollis scelerisque. Ut iaculis porttitor commodo. Fusce nec elit orci. Donec cursus et urna id faucibus. Vivamus rutrum facilisis lorem, ac euismod diam scelerisque ac. Ut faucibus neque vel quam lacinia condimentum. Maecenas non magna non augue congue faucibus. In semper arcu ut nibh porttitor bibendum. Nulla gravida non augue ut faucibus.', 'today');"
sudo -u postgres psql wikiserver -c "insert into wikiserver_post(owner_id, title, content, pub_date) values('2', 'Trunk', 'Maecenas mauris ligula, dignissim quis sodales vitae, tincidunt sit amet ante. Nunc magna felis, aliquet vitae pretium sit amet, interdum ut erat. Nullam vehicula mollis sollicitudin. Phasellus convallis non nisl at posuere. Integer venenatis odio sed dolor cursus bibendum. Morbi aliquam risus id dapibus fringilla. Aenean aliquam vehicula tellus. Fusce porta ultricies posuere.', 'today');"
sudo -u postgres psql wikiserver -c "insert into wikiserver_post(owner_id, title, content, pub_date) values('1', 'Mauris', 'Mauris efficitur erat ligula, vitae rhoncus erat commodo nec. Maecenas vulputate viverra ligula id scelerisque. Mauris vehicula est eu velit volutpat viverra. Aenean magna sapien, vestibulum quis sodales in, tempus vitae arcu. Suspendisse vestibulum massa vitae est viverra accumsan. Suspendisse quis arcu turpis. Proin eu est non leo tristique consequat. Etiam bibendum mauris non ligula gravida, eu porta eros venenatis. Praesent vitae odio eget ligula ultricies vehicula. Aenean vel magna aliquet, tempus neque sed, laoreet justo. Vestibulum pretium massa lorem. Sed facilisis vehicula lectus vitae fringilla. Morbi bibendum vitae nunc eu rhoncus. Maecenas commodo fringilla felis ut congue. Vivamus dapibus, lorem ac fermentum commodo, turpis lacus tincidunt ipsum, quis semper felis nisi vitae arcu. Pellentesque id nisl vitae libero venenatis imperdiet sed non metus.', 'today');"
sudo -u postgres psql wikiserver -c "insert into wikiserver_post(owner_id, title, content, pub_date) values('2', 'Amet', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum a ligula sit amet tortor sagittis tincidunt non eu eros. Suspendisse potenti. Morbi pulvinar fringilla eros, id faucibus elit ultricies ac. Nam auctor efficitur purus convallis porttitor. Fusce lacinia nulla vel ligula mollis scelerisque. Ut iaculis porttitor commodo. Fusce nec elit orci. Donec cursus et urna id faucibus. Vivamus rutrum facilisis lorem, ac euismod diam scelerisque ac. Ut faucibus neque vel quam lacinia condimentum. Maecenas non magna non augue congue faucibus. In semper arcu ut nibh porttitor bibendum. Nulla gravida non augue ut faucibus.', 'today');"
sudo -u postgres psql wikiserver -c "insert into wikiserver_post(owner_id, title, content, pub_date) values('1', 'Efficitur', 'Mauris efficitur erat ligula, vitae rhoncus erat commodo nec. Maecenas vulputate viverra ligula id scelerisque. Mauris vehicula est eu velit volutpat viverra. Aenean magna sapien, vestibulum quis sodales in, tempus vitae arcu. Suspendisse vestibulum massa vitae est viverra accumsan. Suspendisse quis arcu turpis. Proin eu est non leo tristique consequat. Etiam bibendum mauris non ligula gravida, eu porta eros venenatis. Praesent vitae odio eget ligula ultricies vehicula. Aenean vel magna aliquet, tempus neque sed, laoreet justo. Vestibulum pretium massa lorem. Sed facilisis vehicula lectus vitae fringilla. Morbi bibendum vitae nunc eu rhoncus. Maecenas commodo fringilla felis ut congue. Vivamus dapibus, lorem ac fermentum commodo, turpis lacus tincidunt ipsum, quis semper felis nisi vitae arcu. Pellentesque id nisl vitae libero venenatis imperdiet sed non metus.', 'today');"
sudo -u postgres psql wikiserver -c "insert into wikiserver_post(owner_id, title, content, pub_date) values('2', 'Maecenas', 'Maecenas mauris ligula, dignissim quis sodales vitae, tincidunt sit amet ante. Nunc magna felis, aliquet vitae pretium sit amet, interdum ut erat. Nullam vehicula mollis sollicitudin. Phasellus convallis non nisl at posuere. Integer venenatis odio sed dolor cursus bibendum. Morbi aliquam risus id dapibus fringilla. Aenean aliquam vehicula tellus. Fusce porta ultricies posuere.', 'today');"
sudo -u postgres psql wikiserver -c "insert into wikiserver_post(owner_id, title, content, pub_date) values('2', 'Ligula', 'Maecenas mauris ligula, dignissim quis sodales vitae, tincidunt sit amet ante. Nunc magna felis, aliquet vitae pretium sit amet, interdum ut erat. Nullam vehicula mollis sollicitudin. Phasellus convallis non nisl at posuere. Integer venenatis odio sed dolor cursus bibendum. Morbi aliquam risus id dapibus fringilla. Aenean aliquam vehicula tellus. Fusce porta ultricies posuere.', 'today');"
sudo -u postgres psql wikiserver -c "insert into wikiserver_post(owner_id, title, content, pub_date) values('2', 'Vehicula', 'Mauris efficitur erat ligula, vitae rhoncus erat commodo nec. Maecenas vulputate viverra ligula id scelerisque. Mauris vehicula est eu velit volutpat viverra. Aenean magna sapien, vestibulum quis sodales in, tempus vitae arcu. Suspendisse vestibulum massa vitae est viverra accumsan. Suspendisse quis arcu turpis. Proin eu est non leo tristique consequat. Etiam bibendum mauris non ligula gravida, eu porta eros venenatis. Praesent vitae odio eget ligula ultricies vehicula. Aenean vel magna aliquet, tempus neque sed, laoreet justo. Vestibulum pretium massa lorem. Sed facilisis vehicula lectus vitae fringilla. Morbi bibendum vitae nunc eu rhoncus. Maecenas commodo fringilla felis ut congue. Vivamus dapibus, lorem ac fermentum commodo, turpis lacus tincidunt ipsum, quis semper felis nisi vitae arcu. Pellentesque id nisl vitae libero venenatis imperdiet sed non metus.', 'today');"
sudo -u postgres psql wikiserver -c "insert into wikiserver_post(owner_id, title, content, pub_date) values('1', 'Dapibus', 'Ut dapibus orci ut eros varius, non luctus mi rhoncus. Aliquam non suscipit velit. Nulla venenatis sem eu ipsum aliquam, pellentesque euismod magna consectetur. Integer maximus malesuada urna non euismod. Nam arcu erat, euismod vel tempus congue, porta at mi. Nunc a venenatis dui. Phasellus maximus cursus quam, non pharetra arcu tempus eget. In posuere commodo augue sed efficitur. Mauris quis fermentum tellus, eu posuere neque. Integer nisl diam, facilisis non leo non, viverra tincidunt felis. Proin a orci varius, consequat libero vitae, rutrum leo. Vestibulum ultrices posuere libero, et luctus justo iaculis in. Integer ut malesuada nulla, eu porttitor ante. Pellentesque ornare rutrum pharetra. In mattis viverra urna ac cursus. Donec ut erat vitae erat vulputate pulvinar in ut mi.', 'today');"
sudo -u postgres psql wikiserver -c "insert into wikiserver_post(owner_id, title, content, pub_date) values('1', 'Praesent', 'Praesent eget eros eu ex bibendum auctor. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Sed a ex a diam tincidunt scelerisque sed sit amet dui. Maecenas vel velit nulla. Nullam hendrerit nisi leo, at ultricies risus aliquam quis. Nulla aliquet id libero eu pretium. Suspendisse placerat ante ut eleifend placerat. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nullam dolor lorem, consectetur ut fermentum vitae, vehicula quis eros.', 'today');"
sudo -u postgres psql wikiserver -c "insert into wikiserver_post(owner_id, title, content, pub_date) values('2', 'Integer', 'Integer varius est et facilisis tincidunt. Cras condimentum sem et mauris facilisis, quis pretium turpis tempus. Phasellus quis diam nisi. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse potenti. Nam a velit rutrum, faucibus sem vitae, imperdiet libero. In varius pellentesque libero, eget viverra lacus.', 'today');"
sudo -u postgres psql wikiserver -c "insert into wikiserver_post(owner_id, title, content, pub_date) values('2', 'Eget', 'Praesent eget eros eu ex bibendum auctor. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Sed a ex a diam tincidunt scelerisque sed sit amet dui. Maecenas vel velit nulla. Nullam hendrerit nisi leo, at ultricies risus aliquam quis. Nulla aliquet id libero eu pretium. Suspendisse placerat ante ut eleifend placerat. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nullam dolor lorem, consectetur ut fermentum vitae, vehicula quis eros.', 'today');"
sudo -u postgres psql wikiserver -c "insert into wikiserver_post(owner_id, title, content, pub_date) values('1', 'Varius', 'Integer varius est et facilisis tincidunt. Cras condimentum sem et mauris facilisis, quis pretium turpis tempus. Phasellus quis diam nisi. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse potenti. Nam a velit rutrum, faucibus sem vitae, imperdiet libero. In varius pellentesque libero, eget viverra lacus.', 'today');"
sudo -u postgres psql wikiserver -c "insert into wikiserver_post(owner_id, title, content, pub_date) values('2', 'Prion', 'Ut dapibus orci ut eros varius, non luctus mi rhoncus. Aliquam non suscipit velit. Nulla venenatis sem eu ipsum aliquam, pellentesque euismod magna consectetur. Integer maximus malesuada urna non euismod. Nam arcu erat, euismod vel tempus congue, porta at mi. Nunc a venenatis dui. Phasellus maximus cursus quam, non pharetra arcu tempus eget. In posuere commodo augue sed efficitur. Mauris quis fermentum tellus, eu posuere neque. Integer nisl diam, facilisis non leo non, viverra tincidunt felis. Proin a orci varius, consequat libero vitae, rutrum leo. Vestibulum ultrices posuere libero, et luctus justo iaculis in. Integer ut malesuada nulla, eu porttitor ante. Pellentesque ornare rutrum pharetra. In mattis viverra urna ac cursus. Donec ut erat vitae erat vulputate pulvinar in ut mi.', 'today');"
sudo -u postgres psql wikiserver -c "insert into wikiserver_post(owner_id, title, content, pub_date) values('1', 'Eros', 'Praesent eget eros eu ex bibendum auctor. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Sed a ex a diam tincidunt scelerisque sed sit amet dui. Maecenas vel velit nulla. Nullam hendrerit nisi leo, at ultricies risus aliquam quis. Nulla aliquet id libero eu pretium. Suspendisse placerat ante ut eleifend placerat. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nullam dolor lorem, consectetur ut fermentum vitae, vehicula quis eros.', 'today');"
sudo -u postgres psql wikiserver -c "insert into wikiserver_post(owner_id, title, content, pub_date) values('1', 'Posuere', 'Ut dapibus orci ut eros varius, non luctus mi rhoncus. Aliquam non suscipit velit. Nulla venenatis sem eu ipsum aliquam, pellentesque euismod magna consectetur. Integer maximus malesuada urna non euismod. Nam arcu erat, euismod vel tempus congue, porta at mi. Nunc a venenatis dui. Phasellus maximus cursus quam, non pharetra arcu tempus eget. In posuere commodo augue sed efficitur. Mauris quis fermentum tellus, eu posuere neque. Integer nisl diam, facilisis non leo non, viverra tincidunt felis. Proin a orci varius, consequat libero vitae, rutrum leo. Vestibulum ultrices posuere libero, et luctus justo iaculis in. Integer ut malesuada nulla, eu porttitor ante. Pellentesque ornare rutrum pharetra. In mattis viverra urna ac cursus. Donec ut erat vitae erat vulputate pulvinar in ut mi.', 'today');"
sudo -u postgres psql wikiserver -c "insert into wikiserver_post(owner_id, title, content, pub_date) values('1', 'Facilisis', 'Integer varius est et facilisis tincidunt. Cras condimentum sem et mauris facilisis, quis pretium turpis tempus. Phasellus quis diam nisi. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse potenti. Nam a velit rutrum, faucibus sem vitae, imperdiet libero. In varius pellentesque libero, eget viverra lacus.', 'today');"
sudo -u postgres psql wikiserver -c "insert into wikiserver_post(owner_id, title, content, pub_date) values('2', 'Tincidunt', 'Integer varius est et facilisis tincidunt. Cras condimentum sem et mauris facilisis, quis pretium turpis tempus. Phasellus quis diam nisi. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse potenti. Nam a velit rutrum, faucibus sem vitae, imperdiet libero. In varius pellentesque libero, eget viverra lacus.', 'today');"
sudo -u postgres psql wikiserver -c "insert into wikiserver_post(owner_id, title, content, pub_date) values('1', 'Bibendum', 'Praesent eget eros eu ex bibendum auctor. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Sed a ex a diam tincidunt scelerisque sed sit amet dui. Maecenas vel velit nulla. Nullam hendrerit nisi leo, at ultricies risus aliquam quis. Nulla aliquet id libero eu pretium. Suspendisse placerat ante ut eleifend placerat. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nullam dolor lorem, consectetur ut fermentum vitae, vehicula quis eros.', 'today');"
sudo -u postgres psql wikiserver -c "insert into wikiserver_post(owner_id, title, content, pub_date) values('1', 'Auctor', 'Praesent eget eros eu ex bibendum auctor. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Sed a ex a diam tincidunt scelerisque sed sit amet dui. Maecenas vel velit nulla. Nullam hendrerit nisi leo, at ultricies risus aliquam quis. Nulla aliquet id libero eu pretium. Suspendisse placerat ante ut eleifend placerat. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nullam dolor lorem, consectetur ut fermentum vitae, vehicula quis eros.', 'today');"
sudo -u postgres psql wikiserver -c "insert into wikiserver_post(owner_id, title, content, pub_date) values('2', 'Pulvinar', 'Ut dapibus orci ut eros varius, non luctus mi rhoncus. Aliquam non suscipit velit. Nulla venenatis sem eu ipsum aliquam, pellentesque euismod magna consectetur. Integer maximus malesuada urna non euismod. Nam arcu erat, euismod vel tempus congue, porta at mi. Nunc a venenatis dui. Phasellus maximus cursus quam, non pharetra arcu tempus eget. In posuere commodo augue sed efficitur. Mauris quis fermentum tellus, eu posuere neque. Integer nisl diam, facilisis non leo non, viverra tincidunt felis. Proin a orci varius, consequat libero vitae, rutrum leo. Vestibulum ultrices posuere libero, et luctus justo iaculis in. Integer ut malesuada nulla, eu porttitor ante. Pellentesque ornare rutrum pharetra. In mattis viverra urna ac cursus. Donec ut erat vitae erat vulputate pulvinar in ut mi.', 'today');"
sudo -u postgres psql wikiserver -c "insert into wikiserver_post(owner_id, title, content, pub_date) values('1', 'Cras', 'Integer varius est et facilisis tincidunt. Cras condimentum sem et mauris facilisis, quis pretium turpis tempus. Phasellus quis diam nisi. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse potenti. Nam a velit rutrum, faucibus sem vitae, imperdiet libero. In varius pellentesque libero, eget viverra lacus.', 'today');"
