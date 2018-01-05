
class StringTokenSingleton(type):
    """ The ShEx spec uses a number of literal tokens, such as the string 'START'.  This implements
    a StringToken class
    see: https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python Method 3 for pattern used
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

    def __init__(cls, name: str, *args, **kwargs):
        super().__init__(name, *args, **kwargs)


class StringToken(metaclass=StringTokenSingleton):
    def __str__(self):
        return self.__class__.__name__
