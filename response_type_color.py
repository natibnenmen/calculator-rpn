import response_builder_reg


@response_builder_reg.register('color')
def color_builder(result):
    if result % 2 == 0:
        return {'result': result, 'color': 'red'}
    else:
        return {'result': result, 'color': 'green'}