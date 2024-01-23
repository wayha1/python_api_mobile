from app import create_app

app = create_app()

with app.app_context():
    from app.extensions import db
    from app.models import *
    db.create_all()

if __name__ == '__main__':
    app.run(port=5000)