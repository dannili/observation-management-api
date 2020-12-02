# Falsk CLI tool to run the app from the command line

from flask.cli import FlaskGroup
from app import app, db, Target

cli = FlaskGroup(app)

# To create table,
# run 'docker-compose exec web python run.py create_db'
@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

# To add a sample target to the table,
# run 'docker-compose exec web python run.py test_db'
@cli.command("test_db")
def test_db():
	target_sample = Target(name='Mont Tremblant', latitude=46.1185, longitude=74.5962, elevation=875)

	db.session.add(target_sample)
	db.session.commit()

if __name__ == "__main__":
	cli()
