from rest_framework.authtoken.models import Token


def get_user_id_by_token(token):
    return Token.objects.get(key=token).user.id

def get_token_from_request(request):
    return request.headers.get('Authorization')[6:]