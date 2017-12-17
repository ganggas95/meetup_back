from flask_restplus import Api
restplus = Api(version='1.0', title="Service Meetup Backend", description="All service for meetup tech-talk about GIS")
ns = restplus.namespace("v0.1", "All endpoint for meetup tech-talk")