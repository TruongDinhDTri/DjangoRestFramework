from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import BookModel
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, AllowAny



class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookModel
        fields = "__all__"
        read_only_fields = ['id']
    
    def validate(self, data):
        self.price = data['price']
        if self.price  < 0:
            raise serializers.ValidationError("Price cannot be negative")
        return data



@api_view(['GET'])
def BookListApi(request):
    books = BookModel.objects.all()
    serializers = BookModelSerializer(books, many=True)
    return Response(serializers.data)

@api_view(['POST'])
def BookCreateApi(request):
    data = request.data
    serializer = BookModelSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Book created successfully",
            "data": serializer.data
        }, status=201)
    else:
        return Response(serializer.errors, status=400)


@api_view(['PUT'])
def BookUpdateApi(request, id):
    book = BookModel.objects.get(id=id)
    serializer = BookModelSerializer(instance = book, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Book updated successfully",
        })
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def BookDeleteApi(request, id):
    book = BookModel.objects.get(id=id)
    book.delete()
    return Response({
        "message": "Book deleted successfully",
    })

from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 7

class BookModelViewSet(ModelViewSet):
    queryset = BookModel.objects.all()
    serializer_class = BookModelSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    
    def list(self, request, *args, **kwargs):
        user = request.user
        books = BookModel.objects.filter(author=user)
        page = self.paginate_queryset(books)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        serializers = self.get_serializer(data=data)
        if serializers.is_valid():
            serializers.save(author=user)
            return Response({
                "message": "Book created successfully",
                "data": serializers.data
            }, status=201)
        else:
            return Response(serializers.errors, status=400)
        
    def update(self, request, *args, **kwargs):
        user = request.user
        pk = kwargs.pop('pk', False)
        instance = BookModel.objects.get(pk=pk, author=user)
        serializers = self.get_serializer(instance = instance, data=request.data)
        if serializers.is_valid():
            serializers.save(author=user)
            return Response({
                "message": "Book updated successfully",
                "data": serializers.data
            })
        return Response(serializers.errors, status=400)

    def destroy(self, request, *args, **kwargs):
        user = request.user

        pk = kwargs.get('pk')
        if not pk:
            return Response({"error": "Book ID is required"}, status=400)

        instance = BookModel.objects.get(pk=pk)
        print("instance", instance)
        # instance.delete()
        return Response({
            "message": "Book deleted successfully",
        }, status=200)
