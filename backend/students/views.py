from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Student
from .serializers import StudentSerializer

# GET list students
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def student_list(request):
    students = Student.objects.all()

    # search
    search = request.query_params.get("search")
    if search:
        students = students.filter(
            full_name__icontains=search
        ) | students.filter(
            email__icontains=search
        ) | students.filter(
            phone__icontains=search
        ) | students.filter(
            notes__icontains=search
        )

    # ordering
    ordering = request.query_params.get("ordering")
    if ordering:
        students = students.order_by(ordering)

    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)


# POST create student
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def student_create(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# GET / PUT / DELETE single student
@api_view(["GET", "PUT", "DELETE"])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def student_detail(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response({"detail": "الطالب غير موجود"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
