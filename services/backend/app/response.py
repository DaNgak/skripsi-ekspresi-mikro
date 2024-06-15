from flask import jsonify, make_response
import json

def success(status_code=200, message=None, data=None):
    return make_response(json.dumps({
        'code': status_code, 
        'message': message,
        'data': data,
    }), status_code, {'Content-Type': 'application/json'})

def error(status_code=500, message=None, errors=[]):
    return make_response(json.dumps({
        'code': status_code, 
        'message': message,
        'errors': errors,
    }), status_code, {'Content-Type': 'application/json'})

# With jsonify (but auto sorting keys)
# def success(status_code=200, message=None, data=None):
#     return make_response(jsonify({
#         'code': status_code, 
#         'message': message,
#         'data': data,
#     }), status_code)

# def error(status_code=500, message=None, errors=[]):
#     return make_response(jsonify({
#         'code': status_code, 
#         'message': message,
#         'errors': errors,
#     }), status_code)
