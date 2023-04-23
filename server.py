from flask import Flask, request, jsonify
import calculator
from flask_cors import CORS
from response_builder_reg import res_type_map

app = Flask(__name__)
CORS(app)

#rgx = calculator.operations_to_rgx(calculator.operations)


@app.route('/calculate', methods=['GET'])
def calculate():
    print(f'url: {request.url}')
    print(f'args: {request.args}')
    print(f'expression origianl: {request.args.get("expression")}')
    expression = request.args.get('expression').replace('a', '+').replace('b', '^')
    print(f'expression a to +: {expression}')
    restype = request.args.get('restype')
    if restype is None:
        restype = 'default'
    print(f'restype: {restype}')

    try:

        result = calculator.process_expression(expression)

        if result is not None:
            #return jsonify({'result': result})
            return jsonify(res_type_map.get(restype, res_type_map.get('default'))(result))
        else:
            return jsonify({'error': 'Invalid expression'}), 400

    except ZeroDivisionError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/operations', methods=['GET'])
def get_operations():
    return jsonify({'result': [key for key in calculator.operations.keys()]})    


if __name__ == '__main__':
    app.run(debug=True)
