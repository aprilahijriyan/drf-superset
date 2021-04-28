from rest_framework.views import exception_handler


def handler(exc, context):
    """
    Reference: https://www.django-rest-framework.org/api-guide/exceptions/#exception-handling-in-rest-framework-views
    """

    response = exception_handler(exc, context)
    if response is not None:
        data = response.data
        if not isinstance(data, dict):
            data = {"results": data}

        data["status"] = response.status_code
    else:
        data = None

    return response
