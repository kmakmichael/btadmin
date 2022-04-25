
def msg(m):
    return (chr(m[0]), m[2:])


# TODO: add complexity for turns when steering is implemented
def navi(m):
    if m == b'GO':
        return False
    else:
        return True


def binary(m):
    if m == b'1':
        return True
    else:
        return False
