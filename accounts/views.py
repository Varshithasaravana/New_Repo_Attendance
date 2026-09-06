from django.shortcuts import render, redirect

from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import login, logout

from django.contrib.auth.models import User

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .forms import RegisterForm

from .forms import TeacherForm

from .models import Teacher
from django.http import HttpResponse

from django.shortcuts import get_object_or_404

from .serializers import TeacherSerializer
from .decorators import admin_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# REGISTER VIEW
from .forms import RegisterForm, TeacherForm
from .models import Teacher



# ADMIN ONLY TEACHER REGISTRATION

# accounts/views.py



def register_view(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        teacher_form = TeacherForm(request.POST)

        if form.is_valid() and teacher_form.is_valid():

            email = form.cleaned_data['email']

            phone = teacher_form.cleaned_data['phone']

            subject = teacher_form.cleaned_data['subject']

            # VERIFY TEACHER DETAILS

            teacher = Teacher.objects.filter(

                email=email,

                phone=phone,

                subject=subject,

                is_registered=False

            ).first()

            # IF DETAILS NOT FOUND

            if not teacher:

                messages.error(

                    request,

                    "Teacher details not verified."

                )

                return redirect('register')

            # CREATE USER ACCOUNT

            user = form.save()

            # CONNECT USER WITH TEACHER

            teacher.user = user

            teacher.is_registered = True

            teacher.save()

            messages.success(

                request,

                "Registration successful."

            )

            return redirect('login')

    else:

        form = RegisterForm()

        teacher_form = TeacherForm()

    context = {

        'form': form,

        'teacher_form': teacher_form

    }

    return render(

        request,

        'accounts/register.html',

        context

    )


def is_teacher(user):

    return Teacher.objects.filter(user=user).exists()



#LANDING VIEW

def landing_page(request):
    return render(request, 'landing.html')


# LOGIN VIEW

def login_view(request):

    form = AuthenticationForm(
        request,
        data=request.POST or None
    )

    if form.is_valid():

        user = form.get_user()

        login(request, user)

        return redirect('/attendance/')

    else:

        print(form.errors)

    return render(
        request,
        'accounts/login.html',
        {'form': form}
    )

# LOGOUT VIEW
def logout_view(request):

    logout(request)

    return redirect('/accounts/login/')

@login_required(login_url='/accounts/login/')
@admin_required
def teacher_list(request):
    teachers = Teacher.objects.all()

    return render(

        request,

        'accounts/teacher_list.html',

        {

            'teachers': teachers

        }

    )

@login_required(login_url='/accounts/login/')
@admin_required
def view_teacher(request, id):

    teacher = get_object_or_404(
        Teacher,
        id=id
    )

    return render(

        request,

        'accounts/view_teacher.html',

        {

            'teacher': teacher

        }

    )

@login_required(login_url='/accounts/login/')
@admin_required
def add_teacher(request):
    if request.method == 'POST':

        name = request.POST.get('name')

        email = request.POST.get('email')

        password = request.POST.get('password')

        phone = request.POST.get('phone')

        subject = request.POST.get('subject')

        role = request.POST.get('role')

        # CHECK DUPLICATE EMAIL

        if User.objects.filter(
            username=email
        ).exists():

            return render(

                request,

                'accounts/add_teacher.html',

                {

                    'error':

                    'Email already exists'

                }

            )

        # CREATE DJANGO USER

        user = User.objects.create_user(

            username=name,

            email=email,

            password=password,

            first_name=name

        )

        # CREATE TEACHER PROFILE

        Teacher.objects.create(

            user=user,

            phone=phone,

            subject=subject,

            role=role,
            email=email

        )

        return redirect(
            '/accounts/teachers/'
        )

    return render(

        request,

        'accounts/add_teacher.html'
    )


@login_required(login_url='/accounts/login/')
@admin_required
def update_teacher(request, id):
    teacher = get_object_or_404(
        Teacher,
        id=id
    )

    if request.method == 'POST':

        teacher.user.first_name = request.POST.get(
            'name'
        )

        teacher.user.email = request.POST.get(
            'email'
        )

        teacher.phone = request.POST.get(
            'phone'
        )

        teacher.subject = request.POST.get(
            'subject'
        )

        teacher.role = request.POST.get(
            'role'
        )

        teacher.user.save()

        teacher.save()

        return redirect(
            '/accounts/teachers/'
        )

    return render(

        request,

        'accounts/update_teacher.html',

        {

            'teacher': teacher

        }

    )


@login_required(login_url='/accounts/login/')
@admin_required
def view_teacher(request, id):

    teacher = get_object_or_404(
        Teacher,
        id=id
    )

    return render(

        request,

        'accounts/view_teacher.html',

        {

            'teacher': teacher

        }

    )

@login_required(login_url='/accounts/login/')
@admin_required
def delete_teacher(request, id):
    teacher = get_object_or_404(
        Teacher,
        id=id
    )

    teacher.user.delete()

    return redirect(
        '/accounts/teachers/'
    )

#API CREATION FOR Teacher
class TeacherListCreationAPI(APIView):
        def get(self, request):
                teachers=Teacher.objects.all()
                serializer=TeacherSerializer(teachers,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
        
        def post(self,request):
                serializer=TeacherSerializer(data=request.data)
                if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data,status=status.HTTP_201_CREATED)
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# class TeacherRetriveUpdateDestroyAPI(APIView):
#      def patch(self,request,pk):
#           teachers=get_object_or_404(TeacherSerializer,pk)
#           serializer=Teacher(teachers,data=request.data,partial=True)
#           if serializer.is_valid():
#                serializer.save()
#                return Response(serializer.data,status=status.HTTP_200_Ok)
#           return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class TeacherRetrieveUpdateDestroyAPI(APIView):

    def get(self, request, pk):

        teacher = get_object_or_404(Teacher, pk=pk)

        serializer = TeacherSerializer(teacher)

        return Response( serializer.data, status=status.HTTP_200_OK)


    def patch(self, request, pk):

        teacher = get_object_or_404( Teacher, pk=pk)

        serializer = TeacherSerializer(teacher,data=request.data,partial=True)

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):

        teacher = get_object_or_404(Teacher,pk=pk)

        teacher.delete()

        return Response(
            {
                'message': 'Teacher deleted successfully'
            },
            status=status.HTTP_200_OK
        )