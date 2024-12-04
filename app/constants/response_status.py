
class Response:
    """Returns a successful response with a given message and data.

    :param data: The data of the response. Default is None.
    :type data: object
    :param message: The message of the response. Default is "Operation successful.".
    :type message: str
    :param code: The HTTP status code of the response. Default is 200.
    :type code: int
    :return: A tuple containing a dictionary with the status, message and data, and the HTTP status code.
    :rtype: tuple
    """
    @staticmethod
    def success(data=None, message="Operation successful.", code=200):
        return {
            "status": "success",
            "message": message,
            "data": data
        }, code

    @staticmethod
    def error(message="An error occurred.", code=400):
        return {
            "status": "error",
            "message": message,
            "data": None
        }, code
