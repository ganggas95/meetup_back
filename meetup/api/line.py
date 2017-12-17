from flask import jsonify, request
from flask_restplus import Resource, fields
from meetup.api.restplus import ns, restplus
from meetup.model.table import LineTable
from shapely.geometry import LineString
from geojson import FeatureCollection, Feature
import logging
line = restplus.model("LineGeom",{
    "lat" : fields.Float,
    "lng" : fields.Float
})
model_line = restplus.model("Line",{
    "keterangan" : fields.String,
    "line" : fields.List(fields.Nested(line))
})
@ns.route("/meetup/lines")
class ListAPI(Resource):
    def get(self):
        lines = LineTable.query.all()
        data = []
        for ln in lines:
            data.append(ln.line_geom_to_geojson())
        features = FeatureCollection(data)
        return features
    @restplus.expect(model_line)
    def post(self):
        data = request.get_json(force=True)
        if data:
            line = LineTable()
            if 'line' in data:
                linestring = []
                for ln in data['line']:
                    linestring.append((ln['lng'], ln['lng']))
                line.line = LineString(linestring).to_wkt()
            line.keterangan = data['keterangan']
            line.save()
            return jsonify({"messages":"success add line"})
@ns.route("/meetup/line/<int:id>")
class PointAPI(Resource):
    def get(self, id):
        line = LineTable.query.get(id)
        if line:
            return line.line_geom_to_geojson()
    @restplus.expect(model_line)
    def post(self, id):
        data = request.get_json(force=True)
        if data:
            line = LineTable.query.get(id)
            if 'line' in data:
                linestring = []
                for ln in data['line']:
                    linestring.append((ln['lng'], ln['lng']))
                line.line = LineString(linestring).to_wkt()
            if 'keterangan' in data:
                line.keterangan = data['keterangan']
            line.save()
            return jsonify({"messages":"success edit line"})
    def delete(self, id):
        line = LineTable.query.get(id)
        if line:
            line.delete()
            return jsonify({"messages":"success delete line"})