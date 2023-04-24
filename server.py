from flask import Flask, request, jsonify
from operations_reg import operators as operations
from calculator import Calculator
from flask_cors import CORS
from response_builder_reg import build_response

app = Flask(__name__)
CORS(app)


@app.route('/calculate', methods=['GET'])
def calculate():
    expression = request.args.get('expression').replace('a', '+').replace('b', '^')
    print(f'expression a to +: {expression}')
    restype = request.args.get('restype')
    if restype is None:
        restype = 'default'
    print(f'restype: {restype}')

    try:
        calculator = Calculator(operations=operations)
        result = calculator.process_expression(expression)

        if result is not None:
            return jsonify(build_response(response_type=restype, result=result))
        else:
            return jsonify({'error': 'Invalid expression'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/operations', methods=['GET'])
def get_operations():
    return jsonify({'result': [key for key in operations.keys()]})    


if __name__ == '__main__':
    app.run(debug=True)
