from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied, ParseError
from rest_framework.permissions import IsAuthenticated
from .models import Category
from . import serializers
from django.shortcuts import get_object_or_404
from groups.models import Group


class Categories(APIView):
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="전체 카테고리 조회 api",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=serializers.CategorySerializer(),
            )
        },
    )
    def get(self, request):
        category = Category.objects.all()
        serializer = serializers.CategorySerializer(
            category,
            many=True,
        )
        return Response(serializer.data)


class GroupCategories(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="그룹 카테고리 조회 api",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=serializers.CategorySerializer(),
            )
        },
    )
    def get(self, request, group_pk):
        group = get_object_or_404(Group, pk=group_pk)
        category = Category.objects.filter(group=group)
        serializer = serializers.CategorySerializer(
            category,
            many=True,
        )
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="그룹 카테고리 생성 api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["name"],
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="카테고리명"),
            },
        ),
        responses={
            200: openapi.Response(description="OK"),
            400: openapi.Response(description="Invalid request data"),
            401: openapi.Response(description="The user is not authenticated"),
        },
    )
    def post(self, request, group_pk):
        serializer = serializers.CategorySerializer(data=request.data)
        if not request.user.is_coach:
            if not request.user.is_staff:
                raise PermissionDenied
        if serializer.is_valid():
            category = serializer.save(group=group_pk)
            serializer = serializers.CategorySerializer(category)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class GroupCategoryDetail(APIView):
    @swagger_auto_schema(
        operation_summary="그룹 카테고리 조회 api",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=serializers.CategorySerializer(),
            )
        },
    )
    def get(self, request, pk, group_pk):
        category = get_object_or_404(Category, pk=pk, group__pk=group_pk)
        serializer = serializers.CategorySerializer(category)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="그룹 카테고리 수정 api",
        request_body=serializers.CategorySerializer(),
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=serializers.CategorySerializer(),
            ),
            400: "Bad Request",
        },
    )
    def put(self, request, group_pk, pk):
        group = get_object_or_404(Group, pk=group_pk)
        category = get_object_or_404(Category, pk=pk, group=group)
        serializer = serializers.CategorySerializer(
            category,
            data=request.data,
            partial=True,
        )
        if request.user.group != group:
            if not request.user.is_staff:
                raise PermissionDenied

        if request.user.is_coach == False:
            if not request.user.is_staff:
                raise PermissionDenied

        if serializer.is_valid():
            category = serializer.save(group=group_pk)
            serializer = serializers.CategorySerializer(category)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_summary="그룹 카테고리 삭제 api",
        responses={
            204: openapi.Response(
                description="Successful response",
            )
        },
    )
    def delete(self, request, group_pk, pk):
        if request.user.group.pk != group_pk:
            if not request.user.is_staff:
                raise PermissionDenied
        if not request.user.is_coach:
            if not request.user.is_staff:
                raise PermissionDenied

        category = get_object_or_404(Category, pk=pk, group__pk=group_pk)
        category.delete()
        return Response({"result": "delete success"}, status=204)
