from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_superset.schemas import ResponseSchema
from drf_superset.security import jwt
from drf_superset.serializers import LimitOffsetSerializer

from .models import Media
from .serializers import MediaListSerializer, MediaSerializer

# Create your views here.


class MediaUpload(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["media"],
        request_body=MediaSerializer,
        responses={200: ResponseSchema},
        security=[jwt],
    )
    def post(self, request, *args, **kwargs):
        serializer = MediaSerializer(data=request.data)
        serializer.is_valid(True)
        serializer.save()
        return Response({"detail": "ok"})


class MediaList(APIView):
    @swagger_auto_schema(
        tags=["media"],
        query_serializer=LimitOffsetSerializer,
        responses={200: MediaListSerializer(many=True)},
    )
    def get(self, request):
        serializer = LimitOffsetSerializer(data=request.GET)
        serializer.is_valid(True)
        query = serializer.validated_data
        limit = query.get("limit", None)
        offset = query.get("offset", None)
        data = Media.objects.all()[offset:limit]
        serializer = MediaListSerializer(data, many=True)
        data = serializer.data
        return Response(data)
