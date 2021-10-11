from flask import Flask, request, jsonify
from flask_cors import CORS

# Ariadne is a Python library for implementing GraphQL servers. 
from ariadne import graphql_sync, make_executable_schema, gql, load_schema_from_path
from ariadne.constants import PLAYGROUND_HTML

from gql_setup.resolvers import query, mutation

# Create our type definitions, then create our schema
type_defs = gql(load_schema_from_path('./gql_setup/schema.graphql'))
schema = make_executable_schema(type_defs, query, mutation)

# Create flask instance
app = Flask(__name__)

# The following allows for cross-origin resource sharing. It's can increase
# security risks, and should be removed if the frontend is also running on 
# the same origin.
CORS(app)

# This is a test route, and can be removed.
@app.route('/hello', methods=['GET'])
def hello():
    return "Hi there"

# Allows for access to the GraphQL playground (useful for getting the call correctly).
@app.route('/graphql', methods=['GET'])
def graphql_playground():
    return PLAYGROUND_HTML, 200

# How we serve the GraphQL endpoint. Upon succesful sync, return response.
@app.route('/graphql', methods=['POST'])
def graphql_server():
    
    data = request.get_json()

    success, result = graphql_sync(
        schema,
        data,
        context_value = request,
        debug = app.debug
    )

    status_code = 200 if success else 400
    
    return jsonify(result), status_code


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug = True
    )
