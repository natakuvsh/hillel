from datetime import date
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from api.utils import create_date


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        today = create_date(date.today())

        if created:
            token.created = today
            token.save()
            print(f'Changed {token.created}')
        else:
            if (today - token.created).days >= 1:
                token.delete()
                self.post(self, request)

        return Response({'token': token.key})
