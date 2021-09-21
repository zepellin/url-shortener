import flask
import zlib
import json
from dict2xml import dict2xml

app = flask.Flask(__name__)
app.config["DEBUG"] = False

# Defining class for storing URL to identifier mapping
class URLMapping:
    def __init__(self):
        self.urls = {}

    def add_record(self, url):
        indentifier = zlib.adler32(url.encode('UTF-8'))
        if indentifier not in self.urls:
            self.urls[str(indentifier)] = url
        return(indentifier)

    def retrieve_url(self, indentifier):
        if(str(indentifier) in self.urls):
            return(self.urls[indentifier])
        else:
            return(None)

    def get_keys(self):
        records = []
        for record in self:
            records.append(record)
        return(records)

# Initiate instance of a URLMapping class that will serve as our database
db = URLMapping()


# @app.before_first_request
# def create_db():
#     db = URLMapping()

@app.route('/api/v1/shorten/<path:url>', methods=['POST'])
def return_identifier(url):
    # Save identifier and corresponding URL in a "database" class
    db.add_record(url)

    # Create a response dict containing response data sent back to the client
    response_data = {
        "status": "OK",
        "request_url": url,
        "identifier": zlib.adler32(url.encode('UTF-8'))
    }

    # Produce response object with given schema supplied using URL parameters
    response = flask.Response()
    response.status_code = 200

    # Format and create response
    response = format_reponse(flask.request, response_data, response)

    # Send response to client
    return(response)

@app.route('/api/v1/lookup/<identifier>', methods=['GET'])
def return_url(identifier):
    url = db.retrieve_url(identifier)

    # Produce response object with given schema supplied using URL parameters
    response = flask.Response()
    response.status_code = 200 if url is not None else 404 # Generate 302 code to facilitate browser redirects    

    # Create a response dict containing response data sent back to the client
    response_data = {
        "status": "OK" if url is not None else "Not Found",
        "request_url": url if url is not None else "N/A",
        "identifier": str(identifier)
    }

    # Format and create response
    response = format_reponse(flask.request, response_data, response)

    # Send response to client
    return(response)

# Facilitate redirect to URL when <domain>/<identifier> request is received
@app.route('/<identifier>', methods=['GET'])
def redirect_url(identifier):
    url = db.retrieve_url(identifier)

    # Produce response object with given schema supplied using URL parameters
    response = flask.Response()
    if(url is not None):
        response.status_code = 302
        response.headers["Location"] = url
    else:
        response.status_code = 404

    # Send response to client
    return(response)

# Function to format response according to optional format url query parameter
def format_reponse(request, response_data, resp):
    if ('format') in flask.request.args:
        # If format query parameter is xml
        if(flask.request.args['format'] == 'xml'):
            resp.data = dict2xml(response_data)
            resp.mimetype = "application/xml"
            resp.headers["Content-Type"] = "text/xml; charset=utf-8"
        # Default to json for all other format parameters
        else:
            resp.data = json.dumps(response_data)
            resp.mimetype = "application/json"
            resp.headers["Content-Type"] = "application/json; charset=utf-8"

    # If no query parameter is specified
    else:
        resp.data = json.dumps(response_data)
        resp.mimetype = "application/json"
        resp.headers["Content-Type"] = "application/json; charset=utf-8"

    return(resp)


app.run()
