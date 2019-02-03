# CarWash

Manage Fuel Point Of Sales.

## Versions

- Python 3.4+

## Project

### Start the database

Go in docker directory:
```cd docker```
Run the dockerfile for postgres:
```docker-compose up -d```

### Create the database:

```sh
sudo su - postgres
createuser --port=54320 --host=localhost carwash --createdb --pwprompt
# Enter the password `carwash` when prompted
createdb --port=54320 --host=localhost carwash --owner carwash
```

### Install python dependencies:

```sh
pip install -r requirements.txt
```

### Try to launch a basic check

```sh
python manage.py check
```

### Initialise the database:

```sh
python manage.py migrate
```

### Run the server locally:

```sh
python manage.py runserver
```

### Create a superuser for the service

```sh
python manage.py createsuperuser
```

### Run the tests:

```sh
python manage.py test
```

## Import Data files
Store the current xml file in directory fixtures

### Run the import:
```sh
python import_file.py --filename fixtures/<name_of_xml_file>
```

### Look at the result:
1. Import the file
```sh
python import_file.py --filename fixtures/PrixCarburants_instantane.xml
```
2. Start the server
```sh
python manage.py runserver
```
3. Open your browser
http://127.0.0.1:8000/pos/
(limited to 50 PDV)

## Limitations
1. Due to a lack of time, coverage is not optimal...
Some unit tests exists, but not a full cases are tested.

2. Error management could be improved, essentially if the file is badly formatted

3. Metrics and logs must be added to monitor correctly the import.

4. A worker can be added (Celery for instance) to automate the download of the file and the automatic integration in the database.

5. Authentication/Authorisations must be added.

Have Fun.
Olivier
