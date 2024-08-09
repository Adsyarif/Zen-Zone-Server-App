from flask import jsonify

def api_response(status_code, data=None, message=''):
    return jsonify({
        'status': {
            'code': status_code,
            'message': message
        },
        'data': data
    }), status_code