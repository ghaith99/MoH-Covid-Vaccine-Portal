# Reset db

Do the following
1. Connect to Postgres according to .env DB_HOST
2. Create new db and grant to "mohadmin" 
3. Change .env db name
4. Migrate
```
python manage.py makemigrations users
python manage.py migrate users
python manage.py makemigrations pages
python manage.py migrate pages
```

# Known Issue

```
django.db.utils.ProgrammingError: relation "users_customuser" does not exist
```

Solution: migrate users model first