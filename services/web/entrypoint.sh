# Verify Postgres is up before creating db

if [ "$DATABASE" = "postgres" ]
then
    echo "Postgre is starting..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "Postgre is running!"
fi

python run.py create_db

exec "$@"