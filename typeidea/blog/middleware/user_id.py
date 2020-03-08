import uuid

USER_KEY = 'uid'
EXPIRED_TIME = 24 * 60 * 60 * 365

class UseridMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):
        uid = self.generate_uid(request)
        request.uid = uid
        response = self.get_response(request)
        response.set_cookie(USER_KEY,uid,max_age=EXPIRED_TIME,httponly=True)
        return response

    def generate_uid(self,request):
        try:
            uid = request.COOKIES[USER_KEY]
        except KeyError:
            uid = uuid.uuid4().hex
        return uid