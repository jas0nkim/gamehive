from gamehiveplayer import create_app
from gamehiveplayer.models import db

app = create_app()

def init_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
