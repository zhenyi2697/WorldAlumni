from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from social_auth.models import UserSocialAuth

from backend.models import *
from api.serializers import BindingSerializer

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

# @csrf_exempt
# def binding_list(request, format=None):
    # """
    # List all bindins, or create a new snippet.
    # """
    # if request.method == 'GET':
        # bindings = Binding.objects.all()
        # serializer = BindingSerializer(bindings, many=True)
        # print serializer.data
        # return JSONResponse(serializer.data)

    # elif request.method == 'POST':
        # data = JSONParser().parse(request)
        # serializer = BindingSerializer(data=data)
        # if serializer.is_valid():
            # serializer.save()
            # return JSONResponse(serializer.data, status=status.HTTP_201_CREATED)
        # return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def check_binding(request):
    """
    Test if a social user has authendicated
    """
    if request.method == 'POST':
        uid = request.POST.get('uid', '').strip()
        provider = request.POST.get('provider', '').strip()

        auths = UserSocialAuth.objects.filter(uid=uid, provider=provider)

        if auths.count() != 0:
            user_social_auth = auths[0]
            bindings = Binding.objects.filter(user=user_social_auth.user)
        else:
            bindings = []

        serializer = BindingSerializer(bindings, many=True)
        return JSONResponse(serializer.data)

# @csrf_exempt
# def binding_detail(request, pk):
    # """
    # Retrieve, update or delete a code snippet.
    # """
    # try:
        # binding = Binding.objects.get(pk=pk)
    # except Binding.DoesNotExist:
        # return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    # if request.method == 'GET':
        # serializer = BindingSerializer(binding)
        # return JSONResponse(serializer.data)

    # elif request.method == 'PUT':
        # serializer = BindingSerializer(snippet, data=request.DATA)
        # if serializer.is_valid():
            # serializer.save()
            # return JSONResponse(serializer.data)
        # return JSONResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # elif request.method == 'DELETE':
        # binding.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)

