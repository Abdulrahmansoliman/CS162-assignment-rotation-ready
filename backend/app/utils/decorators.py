from functools import wraps
from flask import request, jsonify

def require_params(*required_parameters):
    """Decorator to validate required parameters in request JSON body.
    
    Checks that all specified parameters are present in the request body.
    Returns 400 error with helpful message if any are missing.
    
    Args:
        *required_parameters: Variable number of parameter names (strings)
                             that must be present in request JSON
    
    Returns:
        Decorated function that validates parameters before execution
        
    Example:
        @app.route('/endpoint', methods=['POST'])
        @require_params('email', 'password')
        def my_endpoint():
            # email and password guaranteed to exist in request.get_json()
            ...
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = request.get_json()

            if not data:
                return jsonify({'error': 'Request body is required'}), 400
            
            missing_fields = [field for field in required_parameters if field not in data]
            if missing_fields:
                return jsonify({
                    'error': f'Missing required fields: {", ".join(missing_fields)}'
                }), 400
            
            return f(*args, **kwargs)
        return wrapper
    return decorator