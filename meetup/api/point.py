from flask import jsonify, request
from flask_restplus import Resource, fields
from meetup.api.restplus import ns, restplus
from meetup.model.table import PointTable
from shapely.geometry import Point
from geojson import FeatureCollection, Feature
import logging
point = restplus.model("PointGeom",{
    "lat" : fields.Float,
    "lng" : fields.Float
})
model_point = restplus.model("Point",{
    "keterangan" : fields.String,
    "point" : fields.Nested(point)
})
@ns.route("/meetup/points")
class ListAPI(Resource):
    def get(self):
        points = PointTable.query.all()
        data = []
        for pt in points:
            data.append(pt.point_geom_to_geojson())
        features = FeatureCollection(data)
        return features
    @restplus.expect    (model_point)
    def post(self):
        data = request.get_json(force=True)
        if data:
            point = PointTable()
            if 'point' in data:
                point.point = Point(data['point']['lng'], data['point']['lat']).to_wkt()
            point.keterangan = data['keterangan']
            point.save()
            return jsonify({"messages":"success add point"})
@ns.route("/meetup/point/<int:id>")
class PointAPI(Resource):
    def get(self, id):
        point = PointTable.query.get(id)
        if point:
            return point.point_geom_to_geojson()
    @restplus.expect(model_point)
    def post(self, id):
        data = request.get_json(force=True)
        if data:
            point = PointTable.query.get(id)
            if 'point' in data:
                point.point = Point(data['point']['lng'], data['point']['lat']).to_wkt()
            if 'keterangan' in data:
                point.keterangan = data['keterangan']
            point.save()
            return jsonify({"messages":"success edit point"})
    def delete(self, id):
        point = PointTable.query.get(id)
        if point:
            point.delete()
            return jsonify({"messages":"success delete point"})