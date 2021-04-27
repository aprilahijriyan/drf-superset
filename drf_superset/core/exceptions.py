class RestAPIException(Exception):
    pass


class TokenExpiredException(RestAPIException):
    pass
