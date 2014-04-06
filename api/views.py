import datetime

from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from social_auth.models import UserSocialAuth

from backend.models import *
from api.serializers import *

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


from social.apps.django_app.utils import strategy
@strategy()
def auth_by_token(request, backend):
    backend = request.strategy.backend

    try:
        user = backend.do_auth(
            access_token=request.POST.get('access_token', '').strip()
            )
    except Exception as err:
        print err
        user = None

    if user and user.is_active:
        return user# Return anything that makes sense here
    else:
        return None


@csrf_exempt
def check_binding(request):
    """
    Test if a social user has authendicated
    """
    if request.method == 'POST':
        uid = request.POST.get('uid', '').strip()
        provider = request.POST.get('provider', '').strip()
        access_token = request.POST.get('access_token', '').strip()
        print "access_token is :"
        print access_token

        auths = UserSocialAuth.objects.filter(uid=uid, provider=provider)

        if auths.count() != 0:
            user_social_auth = auths[0]
            bindings = Binding.objects.filter(user=user_social_auth.user)
        else:
            user = auth_by_token(request, provider)
            print user
            # if user:
                # strategy = load_strategy(request=request, backend=backend)
                # _do_login(strategy, user)
            bindings = Binding.objects.filter(user=user)

        serializer = BindingSerializer(bindings, many=True)
        print serializer.data
        return JSONResponse(serializer.data)


@csrf_exempt
def post_location(request):
    '''
    Add a new user location entry
    '''

    if request.method == 'POST':
        print request.POST
        bindingId = request.POST.get('bindingId', '').strip()
        longitude = request.POST.get('longitude', '').strip()
        latitude = request.POST.get('latitude', '').strip()

        try:
            binding = Binding.objects.get(id=bindingId)
        except Binding.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        except Exception,e:
            return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        location = Location(
                    binding=binding,
                    longitude=longitude,
                    latitude=latitude
                )
        location.save()

        ### get related users and return to clients
        users = []
        for binding in Binding.objects.all():
            nearby_user = binding.user
            social_auth = UserSocialAuth.objects.get(user=nearby_user)
            attendances = Attendance.objects.filter(binding=binding)
            data = {
                    'bindingId': str(binding.id),
                    'uid': str(social_auth.uid),
                    'first_name': nearby_user.first_name,
                    'last_name': nearby_user.last_name,
                    'provider': social_auth.provider,
                    'attendances': attendances,
                    'associated_attendances': attendances,
                    'distance': '0.5km',
                    'appear_time': datetime.datetime.now()
                    }
            users.append(data)

        nearby_serializer = UserNearbySerializer(users, many=True)
        return JSONResponse(nearby_serializer.data)
