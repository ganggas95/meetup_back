from meetup import  app
import  os, datetime

def initConfig():
    app.config['SESSION_TYPE'] = "memcached"
    app.config['SECRET_KEY'] = "Meetup Bismillah!#@$$%^()"
    app.config['THREADS_PER_PAGE'] = 2
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:b1sm1llah@localhost/meetup_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.config['COMPRESS_MIMETYPES'] = ['text/html', 'text/css', 'text/xml', 'application/json',
                                        'application/javascript']
    app.config["COMPRESS_LEVEL"] = 6
    app.config["COMPRESS_MIN_SIZE"] = 500
    app.config['RESTPLUS_MASK_SWAGGER'] = False
    app.debug = True
