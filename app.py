"""
    Список трат на комплектующие для компьютера с выводом суммы.
    Поля ввода: устройство, стоимость. БД: hardware_part, price
"""

import flask
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = flask.Flask(__name__, template_folder='template')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "database.db"
)
db = SQLAlchemy(app)


class HardwarePart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512), nullable=False)

    def __init__(self, name, price):
        self.name = name
        self.price = [Price(price=price)]


class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)

    hardware_id = db.Column(
        db.Integer, db.ForeignKey(HardwarePart.id), nullable=False
    )
    device_price = db.relationship("HardwarePart", backref=db.backref("price", lazy=True))


@app.route("/", methods=["GET"])
def hello():
    return flask.render_template("index.html", devices=HardwarePart.query.all())


@app.route("/add_detail", methods=["POST"])
def add_detail():
    name = flask.request.form["name"]
    price = flask.request.form["price"]
    db.session.add(HardwarePart(name, price))
    db.session.commit()

    return flask.redirect(flask.url_for("hello"))

@app.route("/remove_details", methods=["POST"])
def remove_details():
    db.drop_all()
    db.create_all()

    return flask.redirect(flask.url_for("hello"))


with app.app_context():
    db.create_all()
app.run()
