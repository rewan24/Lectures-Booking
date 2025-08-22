from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Group
from students.models import Student
from .serializers import GroupSerializer, AddStudentToGroupSerializer


@api_view(['GET', 'POST'])
def group_list_create(request):
    if request.method == 'GET':
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)

    if request.method == 'GET':
        serializer = GroupSerializer(group)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = GroupSerializer(group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def add_students_to_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    serializer = AddStudentToGroupSerializer(data=request.data)
    if serializer.is_valid():
        student_ids = serializer.validated_data["student_ids"]
        students = Student.objects.filter(id__in=student_ids)

        group.students.add(*students)
        group.save()

        return Response(GroupSerializer(group).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
