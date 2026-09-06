from django.urls import path

from . import views


urlpatterns = [
    path("", views.landing_page, name="landing"),

    path(
        'register/',
        views.register_view,
        name='register'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    # TEACHERS

    path(
        'teachers/',
        views.teacher_list,
        name='teacher_list'
    ),

    path(
        'add-teacher/',
        views.add_teacher,
        name='add_teacher'
    ),

    path(
        'view-teacher/<int:id>/',
        views.view_teacher,
        name='view_teacher'
    ),

    path(
        'update-teacher/<int:id>/',
        views.update_teacher,
        name='update_teacher'
    ),

    path(
        'delete-teacher/<int:id>/',
        views.delete_teacher,
        name='delete_teacher'
    ),
     path(
        'api/teachers/',
        views.TeacherListCreationAPI.as_view(),
        name='teacher_api'
    ),

    path(
        'api/teachers/<int:pk>/',
        views.TeacherRetrieveUpdateDestroyAPI.as_view(),
        name='teacher_update_delete_api'
    ),

]