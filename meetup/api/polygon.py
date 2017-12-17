from flask import jsonify, request
from flask_restplus import Resource, fields
from meetup.api.restplus import ns, restplus
from meetup.model.table import PolygonTable
from shapely.geometry import Polygon
from geojson import FeatureCollection, Feature
import logging
polygon = restplus.model("PolygonGeom",{
    "lat" : fields.Float,
    "lng" : fields.Float
})
model_polygon = restplus.model("Polygon",{
    "keterangan" : fields.String,
    "polygon" : fields.List(fields.Nested(polygon))
})
@ns.route("/meetup/polygons")
class ListAPI(Resource):
    def get(self):
        polygons = PolygonTable.query.all()
        data = []
        for poly in polygons:
            data.append(poly.polygon_geom_to_geojson())
        features = FeatureCollection(data)
        return features
    @restplus.expect(model_polygon)
    def post(self):
        data = request.get_json(force=True)
        if data:
            polygon = PolygonTable()
            if 'polygon' in data:
                polygons = []
                for poly in data['polygon']:
                    polygons.append((poly['lng'], poly['lng']))
                polygon.polygon = Polygon(polygons).to_wkt()
            polygon.keterangan = data['keterangan']
            polygon.save()
            return jsonify({"messages":"success add polygon"})
@ns.route("/meetup/polygon/<int:id>")
class PointAPI(Resource):
    def get(self, id):
        polygon = PolygonTable.query.get(id)
        if polygon:
            return polygon.polygon_geom_to_geojson()
    @restplus.expect(model_polygon)
    def post(self, id):
        data = request.get_json(force=True)
        if data:
            polygon = PolygonTable.query.get(id)
            if 'polygon' in data:
                polygons = []
                for poly in data['polygon']:
                    polygons.append((poly['lng'], poly['lng']))
                polygon.polygon = Polygon(polygons).to_wkt()
            if 'keterangan' in data:
                polygon.keterangan = data['keterangan']
            polygon.save()
            return jsonify({"messages":"success edit polygon"})
    def delete(self, id):
        polygon = PolygonTable.query.get(id)
        if polygon:
            polygon.delete()
            return jsonify({"messages":"success delete polygon"})