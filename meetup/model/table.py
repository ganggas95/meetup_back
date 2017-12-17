from meetup import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from geoalchemy2 import Geometry, functions as func
import json
from geojson import Feature, FeatureCollection
db = SQLAlchemy(app)
migrate = Migrate(app=app, db=db)
class PointTable(db.Model):
    __tablename__ = "meetup_point"
    __table_args__ = {"extend_existing" : True}
    id = db.Column(db.Integer, primary_key=True)
    point = db.Column(Geometry(geometry_type='POINT', srid=4326))
    keterangan = db.Column(db.Text)
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def point_geom_to_geojson(self):
        # extract x and y coordinates from a point geometry
        geom_json = json.loads(db.session.scalar(func.ST_AsGeoJSON(self.point)))
        return Feature(geometry=geom_json, properties={
            "keterangan" : self.keterangan
        })
class LineTable(db.Model):
    __tablename__ = "meetup_line"
    __table_args__ = {"extend_existing" : True}
    id = db.Column(db.Integer, primary_key=True)
    line = db.Column(Geometry(geometry_type='LINESTRING', srid=4326))
    keterangan = db.Column(db.Text)
    def line_geom_to_geojson(self):
        # extract x and y coordinates from a point geometry
        geom_json = json.loads(db.session.scalar(func.ST_AsGeoJSON(self.line)))
        return Feature(geometry=geom_json, properties={
            "keterangan" : self.keterangan
        })
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class PolygonTable(db.Model):
    __tablename__ = "meetup_polygon"
    __table_args__ = {"extend_existing" : True}
    id = db.Column(db.Integer, primary_key=True)
    polygon = db.Column(Geometry(geometry_type='POLYGON', srid=4326))
    keterangan = db.Column(db.Text)
    def poly_geom_to_geojson(self):
        # extract x and y coordinates from a point geometry
        geom_json = json.loads(db.session.scalar(func.ST_AsGeoJSON(self.polygon)))
        return Feature(geometry=geom_json, properties={
            "keterangan" : self.keterangan
        })
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    def delete(self):
        db.session.delete(self)
        db.session.commit()
