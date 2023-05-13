from rest_framework import generics
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from app.snippet.serializers import SnippetAddSerializer, SnippetListSerializer,\
      SnippetUpdateSerializer, SnippetSerializer, TagSerializer
from app.models import Tag, Snippet
from rest_framework.parsers import MultiPartParser, FormParser


# Create your views here.

class SnippetAddView(generics.CreateAPIView):
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = SnippetAddSerializer
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'Success': 'True',
            'StatusCode': status_code,
            'Message': 'Snippet Added',
            'Snippet': serializer.data,
        }
        return Response(response, status=status_code)
    
class SnippetListView(generics.ListAPIView):
    queryset = Snippet.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = SnippetListSerializer

    # def get_queryset(self):
    #     return Snippet.objects.all().order_by('created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count()

        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data
        response_data.append({'count': count})

        return Response(response_data)
    
class SnippetDetailView(generics.RetrieveAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetListSerializer
    lookup_field = 'id'

class SnippetUpdateView(generics.UpdateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetUpdateSerializer
    permission_classes = [IsAuthenticated,]
    lookup_field = 'id'

class SnippetDeleteView(generics.DestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [IsAuthenticated,]
    lookup_field = 'id'

class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = TagSerializer

class TagDetailView(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated,]
    lookup_field = 'id'