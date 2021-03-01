from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://mdhhfweg:6M3poDyjXOZPBK14DfsngQyiMoYBFY7G@ziggy.db.elephantsql.com:5432/mdhhfweg"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app) 
ma = Marshmallow(app)

profile_db = {
    "success": True,
    "data": {
        "last_updated": "2/3/2021, 8:48:51 PM",
        "username": "Akeenu Allen",
        "role": "Electronics Engineer",
        "color": "Burgundy"

class Tank(db.model):
    __tablename__ = "tanks"

    id = db.Column(db.Integer, primary_key = True)
    location = db.Column(db.String(), nullable=False)
    lat = db.Column(db.Float(), nullable=False)
    long = db.Column(db.Float(), nullable=False)
    percent_full = db.Column(db.Integer(), nullable=False)

class TankSchema(ma.SQLAlchemySchema):
  class Meta:
    model = Tank
    fields = ("id", "location", "lat", "long", "percent_full")

db.init_app(app) 
migrate = Migrate(app, db)

@app.route("/data", methods=["GET", "POST"])
def data():
    if request.method == "POST":
        newTank = Tank(
            location = request.json["location"],
            lat =  request.json["lat"],
            long = request.json["long"],
            percent_full = request.json["percent_full"]
        )

        db.session.add(newTank)
        db.session.commit()
        return TankSchema().dump(newTank)

    else:
        tanks = Tank.query.all()
        tanks_json = TankSchema(many=True).dump(tanks)
        return  jsonify(tanks_json)


@app.route("/data/<int:id>", methods=["PATCH", "DELETE"])
def update(id):

    if request.method == "PATCH":
        Tank = Tank.query.get(id)
        update = request.json

        if "location" in update: tank.location = update["location"]
        if "lat" in update: tank.lat = update["lat"]
        if "long" in update: tank.long = update["long"]
        if "percent_full" in update: tank.percent_full = update["percent_full"]
        db.session.commit()
        return TankSchema().dump(tank)     
        
    elif request.method == "DELETE":
        tank = Tank.query.get(id)
        db.session.delete(tank)
        db.session.commit()
        return {"success": True}

    else:
        tanks = Tank.query.all()
        tanks_json = TankSchema(many=True).dump(tanks)
        return  jsonify(tanks_json)


if __name__ == '__main__':
   app.run(debug = True)