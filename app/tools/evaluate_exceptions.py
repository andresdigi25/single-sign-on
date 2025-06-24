def fatal_code(e):
    if e.response.get('message') == 'Too many requests':
        return False
    return True
