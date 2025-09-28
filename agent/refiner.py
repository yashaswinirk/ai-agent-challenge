def refiner_node(state):
    state['attempt'] += 1
    if state['success']:
        state['next_step'] = 'end'
    elif state['attempt'] > state['max_attempts']:
        state['next_step'] = 'end'
    else:
        state['next_step'] = 'codegen'
    return state
