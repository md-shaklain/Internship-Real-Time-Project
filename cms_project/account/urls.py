from django.urls import path
from . import views

urlpatterns = [
    path('', views.role_select, name='role_select'),
    path('home/', views.home, name='home'),
    path('register/', views.register_view, name='register'),

    path('admin_login/', views.admin_login, name='admin_login'),
    path('teacher_login/', views.teacher_login, name='teacher_login'),
    path('student_login/', views.student_login, name='student_login'),

    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),

    path('students/', views.students_list, name='students_list'),
    path('student-list/', views.student_list, name='student_list'),
    path('add-student/', views.add_student, name='add_student'),
    path('edit-student/<int:id>/', views.edit_student, name='edit_student'),
    path('delete-student/<int:id>/', views.delete_student, name='delete_student'),

    path('teacher/', views.teacher_list, name='teacher_list'),
    path('add-teacher/', views.add_teacher, name='add_teacher'),
    path('edit-teacher/<int:id>/', views.edit_teacher, name='edit_teacher'),
    path('delete-teacher/<int:id>/', views.delete_teacher, name='delete_teacher'),

    path('course-list/', views.course_list, name='course_list'),
    path('add-course/', views.add_course, name='add_course'),
    path('edit-course/<int:id>/', views.edit_course, name='edit_course'),
    path('delete-course/<int:id>/', views.delete_course, name='delete_course'),

    path('departments/', views.departments_list, name='departments_list'),
    path('add-department/', views.add_department, name='add_department'),
    path('edit-department/<int:id>/', views.edit_department, name='edit_department'),
    path('delete-department/<int:id>/', views.delete_department, name='delete_department'),

    path('attendance/', views.attendance_list, name='attendance_list'),
    path('add-attendance/', views.add_attendance, name='add_attendance'),
    path('edit-attendance/<int:id>/', views.edit_attendance, name='edit_attendance'),
    path('delete-attendance/<int:id>/', views.delete_attendance, name='delete_attendance'),

    path('fees/', views.fees_list, name='fees_list'),
    path('add-fee/', views.add_fee, name='add_fee'),
    path('edit-fee/<int:id>/', views.edit_fee, name='edit_fee'),
    path('delete-fee/<int:id>/', views.delete_fee, name='delete_fee'),

    path('result-list/', views.result_list, name='result_list'),
    path('add-result/', views.add_result, name='add_result'),
    path('edit-result/<int:id>/', views.edit_result, name='edit_result'),
    path('delete-result/<int:id>/', views.delete_result, name='delete_result'),

    path('forget-password/', views.forget_password, name='forget_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('logout/', views.logout_user, name='logout'),

    path('class-timings/', views.class_timing_list, name='class_timing_list'),
    path('add-class-timing/', views.add_class_timing, name='add_class_timing'),
    path('edit-class-timing/<int:id>/', views.edit_class_timing, name='edit_class_timing'),
    path('delete-class-timing/<int:id>/', views.delete_class_timing, name='delete_class_timing'),

    path('teacher-schedule/', views.teacher_schedule_list, name='teacher_schedule_list'),
    path('add-teacher-schedule/', views.add_teacher_schedule, name='add_teacher_schedule'),
    path('edit-teacher-schedule/<int:id>/', views.edit_teacher_schedule, name='edit_teacher_schedule'),
    path('delete-teacher-schedule/<int:id>/', views.delete_teacher_schedule, name='delete_teacher_schedule'),

    path('exam-timetable_list/', views.exam_timetable_list, name='exam_timetable_list'),
    path('add-exam-timetable/', views.add_exam_timetable, name='add_exam_timetable'),
    path('edit-exam-timetable/<int:id>/', views.edit_exam_timetable, name='edit_exam_timetable'),
    path('delete-exam-timetable/<int:id>/', views.delete_exam_timetable, name='delete_exam_timetable'),

    path('about/', views.about, name='about'),
    path('courses/', views.courses, name='courses'),
    path('faculty/', views.faculty, name='faculty'),
    path('contact/', views.contact, name='contact'),
]
