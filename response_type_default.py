import response_builder_reg


@response_builder_reg.register('default')
def default_builder(result):
    return {'result': result}