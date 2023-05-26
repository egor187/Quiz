1. Pull repo
2. Create **.env** file in project root with
```python
POSTGRES_DB="your_db_name"
POSTGRES_USER="your_db_username"
POSTGRES_PASSWORD="your_db_password"
DB_URL="postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}"
```
3. Run docker compose up -d
4. Go to http://127.0.0.1:8000/docs 