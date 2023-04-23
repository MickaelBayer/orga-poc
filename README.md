# Flask Basic User Authentication and Organisation managment.

Quick POC of an Organisation managment system.

In the root directory  run:

```bash
python3 -m venv env
source env/Scripts/activate
pip install -r requirements.txt
```

Rename ".env example" in ".env", setup your own environment variables in it and run :

```bash
source .env
```

To init the db, run,

```bash
flask db init
flask db migrate
flask db upgrade
```

To run the project :

```bash
python manage.py run
```

To run the tests :

```bash
python manage.py test
```

Base sources:

https://ashutoshkrris.hashnode.dev/how-to-set-up-basic-user-authentication-in-a-flask-app

https://www.freecodecamp.org/news/how-to-setup-user-authentication-in-flask/
