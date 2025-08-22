from django.urls import path
from .views import group_list_create, group_detail, add_students_to_group

app_name = "groups"  

urlpatterns = [
    path("", group_list_create, name="group-list-create"),
    path("<int:pk>/", group_detail, name="group-detail"),
    path("<int:pk>/add-students/", add_students_to_group, name="add-students-to-group"),
]




# GET /groups/ → كل الجروبات

# POST /groups/ → إنشاء جروب

# GET /groups/<id>/ → تفاصيل جروب

# PUT /groups/<id>/ → تعديل جروب

# DELETE /groups/<id>/ → حذف جروب

# POST /groups/<id>/add-students/ → إضافة طلاب للجروب