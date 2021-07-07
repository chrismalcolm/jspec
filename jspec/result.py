""""Module for the defining the Result."""

class Result:
    """
        This class defines the result of a JSPEC check
        for a JSON.

        Attributes:
        > _result (bool) - whether the JSON matches the JSPEC
        > _message (str) - reason why the JSON didn't match if
            it didn't, else this is any empty string
    """

    def __init__(self, result=False, message=""):
        self._result = bool(result)
        self._message = str(message)

    def result(self):
        """Return the result"""
        return self._result

    def message(self):
        """Return the message"""
        return self._message 