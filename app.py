from flask import Flask
from models import db, Vulnerability
from cvss import CVSS3
import markdown

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vulndb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# RUN ONCE TO CREATE DB
# with app.app_context():
#     db.create_all()

@app.route('/')
def index():
    return "<h1>Hello, World</h1>"