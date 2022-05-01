
def msg(m):
    return (chr(m[0]), m[2:])


# TODO: add complexity for turns when steering is implemented
def navi(m):
    if m == b'G' or m == b'T':
        return True
    else:
        return False


def binary(m):
    return m == b'1'
