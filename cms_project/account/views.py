from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.db import IntegrityError, transaction
from datetime import datetime
import random
import json

from .models import (
    Student, Teacher, Course, Department, UserAccount, Attendance,
    Result, Fee, ClassTiming, TeacherClassSchedule, ExamTimeTable
)


# =========================================================
# PUBLIC / STATIC PAGES
# =========================================================

def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def courses(request):
    return render(request, "courses.html")


def faculty(request):
    return render(request, "faculty.html")


def contact(request):
    return render(request, "contact.html")


# =========================================================
# AUTH / LOGIN / REGISTER / LOGOUT / PASSWORD RESET
# =========================================================

def _render_role_select(request, selected_role=None, error=None):
    return render(request, "login.html", {
        "selected_role": selected_role or "",
        "error": error or "",
    })


def role_select(request):
    return _render_role_select(request)


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        role = request.POST.get("role", "").strip()
        password = request.POST.get("password", "").strip()
        security_question = request.POST.get("security_question", "").strip()
        security_answer = request.POST.get("security_answer", "").strip()

        if not username or not email or not role or not password or not security_question or not security_answer:
            return render(request, "login.html", {
                "signup_error": "All fields are required.",
                "show_signup": True
            })

        if UserAccount.objects.filter(username=username).exists():
            return render(request, "login.html", {
                "signup_error": "Username already exists.",
                "show_signup": True
            })

        if UserAccount.objects.filter(email=email).exists():
            return render(request, "login.html", {
                "signup_error": "Email already exists.",
                "show_signup": True
            })

        department = Department.objects.first()
        course = Course.objects.first()

        if role == "student":
            if not department or not course:
                return render(request, "login.html", {
                    "signup_error": "Student signup failed. Please add Department and Course first.",
                    "show_signup": True
                })

        if role == "teacher":
            if not department:
                return render(request, "login.html", {
                    "signup_error": "Teacher signup failed. Please add Department first.",
                    "show_signup": True
                })

        try:
            with transaction.atomic():
                UserAccount.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    role=role,
                    security_question=security_question,
                    security_answer=security_answer,
                )

                if role == "student":
                    Student.objects.create(
                        name=username,
                        email=email,
                        department=department,
                        course=course,
                    )

                elif role == "teacher":
                    Teacher.objects.create(
                        name=username,
                        email=email,
                        department=department,
                    )

            return render(request, "login.html", {
                "success": "Account created successfully. Please login.",
                "show_signup": False
            })

        except IntegrityError:
            return render(request, "login.html", {
                "signup_error": "Account already exists.",
                "show_signup": True
            })

        except Exception as e:
            return render(request, "login.html", {
                "signup_error": f"Something went wrong: {str(e)}",
                "show_signup": True
            })

    return render(request, "login.html")


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and getattr(user, "role", None) == "admin":
            login(request, user)
            request.session["username"] = user.username
            request.session["role"] = user.role
            return redirect("admin_dashboard")

        return _render_role_select(request, "admin", "Your User ID or Password is incorrect")

    return _render_role_select(request, "admin")


def teacher_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            return _render_role_select(request, "teacher", "Invalid username or password")

        if getattr(user, "role", None) != "teacher":
            return _render_role_select(request, "teacher", "This account is not a teacher account")

        teacher, _ = Teacher.objects.get_or_create(
            useraccount=user,
            defaults={
                "name": user.username,
                "email": user.email,
                "department": Department.objects.first(),
            },
        )

        login(request, user)
        request.session["teacher_id"] = teacher.id
        request.session["role"] = "teacher"
        return redirect("teacher_dashboard")

    return _render_role_select(request, "teacher")


def student_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and getattr(user, "role", None) == "student":
            login(request, user)
            request.session["username"] = user.username
            request.session["role"] = user.role
            return redirect("student_dashboard")

        return _render_role_select(request, "student", "Your User ID or Password is incorrect")

    return _render_role_select(request, "student")


def logout_user(request):
    logout(request)
    request.session.flush()
    return redirect('role_select')


def forget_password(request):
    if request.method == "POST":
        email = request.POST.get('email')

        user = UserAccount.objects.filter(email=email).first()

        if user:
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.otp_verified = False
            user.save()

            send_mail(
                subject='OTP for Password Reset',
                message=f'Your 6 digit OTP is: {otp}',
                from_email=None,
                recipient_list=[email],
                fail_silently=False,
            )

            request.session['reset_email'] = email
            return redirect('verify_otp')

        return render(request, 'forget_password.html', {'error': 'Email not found'})

    return render(request, 'forget_password.html')


def verify_otp(request):
    email = request.session.get('reset_email')

    if not email:
        return redirect('forget_password')

    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        user = UserAccount.objects.filter(email=email).first()

        if user and user.otp == entered_otp:
            user.otp_verified = True
            user.save()
            return redirect('reset_password')

        return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})

    return render(request, 'verify_otp.html')


def reset_password(request):
    email = request.session.get('reset_email')

    if not email:
        return redirect('forget_password')

    user = UserAccount.objects.filter(email=email, otp_verified=True).first()

    if not user:
        return redirect('forget_password')

    if request.method == "POST":
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            return render(request, 'reset_password.html', {'error': 'Passwords do not match'})

        user.set_password(new_password)
        user.otp = None
        user.otp_verified = False
        user.save()

        request.session.pop('reset_email', None)
        return redirect('role_select')

    return render(request, 'reset_password.html')


# =========================================================
# STUDENT SECTION
# =========================================================

def student_dashboard(request):
    if request.session.get('role') != 'student':
        return redirect('/')

    username = request.session.get('username')
    student_user = UserAccount.objects.filter(username=username, role='student').first()

    student = Student.objects.filter(email=student_user.email).first() if student_user else None
    attendance = Attendance.objects.filter(student=student) if student else Attendance.objects.none()
    results = Result.objects.filter(student=student) if student else Result.objects.none()
    fees = Fee.objects.filter(student=student) if student else Fee.objects.none()

    total_classes = attendance.count()
    present_classes = attendance.filter(status='Present').count()

    attendance_percentage = 0
    if total_classes > 0:
        attendance_percentage = (present_classes / total_classes) * 100

    can_give_exam = attendance_percentage >= 75

    attendance_chart_labels = ['Present', 'Absent']
    attendance_chart_data = [0, 0]

    result_labels = []
    result_marks_data = []

    fee_status_labels = ['Paid', 'Pending']
    fee_status_data = [0, 0]

    subject_labels = []
    subject_marks_data = []

    if student:
        absent_classes = total_classes - present_classes
        attendance_chart_data = [present_classes, absent_classes]

        recent_results = results.order_by('-id')[:6]
        for result in reversed(recent_results):
            result_labels.append(f"{result.subject}")
            result_marks_data.append(result.marks)

        paid_fees = fees.filter(status__iexact='Paid').count()
        pending_fees = fees.filter(status__iexact='Pending').count()
        fee_status_data = [paid_fees, pending_fees]

        all_results = results.order_by('id')
        for result in all_results:
            subject_labels.append(result.subject)
            subject_marks_data.append(result.marks)

    context = {
        'student_user': student_user,
        'student': student,
        'attendance': attendance,
        'results': results,
        'fees': fees,
        'total_classes': total_classes,
        'present_classes': present_classes,
        'attendance_percentage': round(attendance_percentage, 2),
        'can_give_exam': can_give_exam,
        'attendance_chart_labels': attendance_chart_labels,
        'attendance_chart_data': attendance_chart_data,
        'result_labels': result_labels,
        'result_marks_data': result_marks_data,
        'fee_status_labels': fee_status_labels,
        'fee_status_data': fee_status_data,
        'subject_labels': subject_labels,
        'subject_marks_data': subject_marks_data,
    }

    return render(request, 'student_dashboard.html', context)


def students_list(request):
    if request.session.get('role') != 'admin':
        return redirect('/')

    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})


def student_list(request):
    students = Student.objects.all().order_by('-id')
    return render(request, 'student_list.html', {'students': students})


def add_student(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        enrollment_no = request.POST.get('enrollment_no')
        department_id = request.POST.get('department')
        course_id = request.POST.get('course')
        semester = request.POST.get('semester')
        section = request.POST.get('section', 'studentsSection')

        if all([name, email, phone, enrollment_no, department_id, course_id, semester]):
            Student.objects.create(
                name=name,
                email=email,
                phone=phone,
                enrollment_no=enrollment_no,
                department_id=department_id,
                course_id=course_id,
                semester=semester
            )

        if request.session.get('role') == 'teacher':
            return redirect(f'/teacher_dashboard/?section={section}')
        return redirect('/students/')

    return redirect('/teacher_dashboard/?section=addStudentSection')


def edit_student(request, id):
    if request.session.get('role') != 'admin':
        return redirect('/')

    student = get_object_or_404(Student, id=id)
    departments = Department.objects.all()
    courses = Course.objects.all()
    users = UserAccount.objects.filter(role='student')

    if request.method == 'POST':
        student.useraccount_id = request.POST.get('useraccount') or None
        student.name = request.POST.get('name')
        student.email = request.POST.get('email')
        student.phone = request.POST.get('phone')
        student.department_id = request.POST.get('department')
        student.course_id = request.POST.get('course')
        student.semester = request.POST.get('semester')
        student.enrollment_no = request.POST.get('enrollment_no')
        student.save()
        return redirect('students_list')

    return render(request, 'edit_student.html', {
        'student': student,
        'departments': departments,
        'courses': courses,
        'users': users,
    })


def delete_student(request, id):
    if request.session.get('role') != 'admin':
        return redirect('/')

    student = Student.objects.get(id=id)
    student.delete()
    return redirect('students_list')


# =========================================================
# TEACHER SECTION
# =========================================================

def teacher_dashboard(request):
    if request.session.get('role') != 'teacher':
        return redirect('/')

    teacher_id = request.session.get('teacher_id')

    teacher = None
    teachers = Teacher.objects.all()
    students = Student.objects.none()
    courses = Course.objects.none()
    attendance_records = Attendance.objects.none()
    results = Result.objects.none()
    class_timings = ClassTiming.objects.none()
    exam_timetables = ExamTimeTable.objects.none()
    teacher_schedules = TeacherClassSchedule.objects.none()
    low_attendance_students = []

    attendance_present_count = 0
    attendance_absent_count = 0

    result_labels = []
    result_marks_data = []

    course_labels = []
    course_student_counts = []

    exam_labels = []
    exam_counts = []

    if teacher_id:
        try:
            teacher = Teacher.objects.get(id=teacher_id)

            if request.method == "POST":
                teacher_post_id = request.POST.get('teacher')
                course_id = request.POST.get('course')
                schedule_date = request.POST.get('date')
                day = request.POST.get('day')
                timing_id = request.POST.get('timing')
                room_no = request.POST.get('room_no')

                if teacher_post_id and course_id and day and timing_id and room_no:
                    TeacherClassSchedule.objects.create(
                        teacher_id=teacher_post_id,
                        course_id=course_id,
                        date=schedule_date if schedule_date else None,
                        day=day,
                        timing_id=timing_id,
                        room_no=room_no
                    )
                    return redirect('/teacher_dashboard/?section=teacherScheduleSection')

            students = Student.objects.all().order_by('id')
            courses = Course.objects.filter(department=teacher.department)
            attendance_records = Attendance.objects.all().order_by('id')
            results = Result.objects.all().order_by('id')

            class_timings = ClassTiming.objects.all()
            exam_timetables = ExamTimeTable.objects.filter(course__in=courses)
            teacher_schedules = TeacherClassSchedule.objects.filter(
                teacher__department=teacher.department
            ).order_by('-date')

            for student in students:
                student_attendance = Attendance.objects.filter(student=student)
                total_classes = student_attendance.count()
                present_classes = student_attendance.filter(status='Present').count()

                attendance_percentage = 0
                if total_classes > 0:
                    attendance_percentage = (present_classes / total_classes) * 100

                if attendance_percentage < 75:
                    low_attendance_students.append({
                        'student': student,
                        'total_classes': total_classes,
                        'present_classes': present_classes,
                        'attendance_percentage': round(attendance_percentage, 2),
                    })

            attendance_present_count = attendance_records.filter(status='Present').count()
            attendance_absent_count = attendance_records.filter(status='Absent').count()

            recent_results_for_chart = results[:6]
            for result in reversed(recent_results_for_chart):
                label = f"{result.student.name} - {result.course.name}"
                result_labels.append(label)
                result_marks_data.append(result.marks)

            for course in courses:
                course_labels.append(course.name)
                course_student_counts.append(Student.objects.filter(course=course).count())

            for course in courses:
                exam_labels.append(course.name)
                exam_counts.append(ExamTimeTable.objects.filter(course=course).count())

        except Teacher.DoesNotExist:
            teacher = None

    active_section = request.GET.get('section', 'dashboardSection')

    context = {
        'teacher': teacher,
        'teachers': teachers,
        'total_students': students.count(),
        'total_courses': courses.count(),
        'total_attendance': attendance_records.count(),
        'total_results': results.count(),
        'recent_students': students.order_by('-id')[:5],
        'recent_attendance': attendance_records.order_by('-id')[:5],
        'low_attendance_students': low_attendance_students,
        'students': students,
        'courses': courses,
        'attendance_records': attendance_records,
        'results': results,
        'departments': Department.objects.all(),
        'class_timings': class_timings,
        'exam_timetables': exam_timetables,
        'teacher_schedules': teacher_schedules,
        'active_section': active_section,
        'attendance_present_count': attendance_present_count,
        'attendance_absent_count': attendance_absent_count,
        'result_labels': result_labels,
        'result_marks_data': result_marks_data,
        'course_labels': course_labels,
        'course_student_counts': course_student_counts,
        'exam_labels': exam_labels,
        'exam_counts': exam_counts,
    }

    return render(request, 'teacher_dashboard.html', context)


def teacher_list(request):
    if request.session.get('role') != 'admin':
        return redirect('/')

    teachers = Teacher.objects.all()
    return render(request, 'teacher_list.html', {'teachers': teachers})


def add_teacher(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        department_id = request.POST.get('department')

        print("name =", name)
        print("email =", email)
        print("department_id =", department_id)

        if name and email and department_id:
            try:
                department = Department.objects.get(id=department_id)
                teacher = Teacher.objects.create(
                    name=name,
                    email=email,
                    department=department
                )
                print("TEACHER SAVED:", teacher.id, teacher.name, teacher.email, teacher.department.name)
                return redirect('admin_dashboard')
            except Department.DoesNotExist:
                print("Department not found")
        else:
            print("Name or Email or Department missing")

    return redirect('admin_dashboard')


def edit_teacher(request, id):
    if request.session.get('role') != 'admin':
        return redirect('/')

    teacher = get_object_or_404(Teacher, id=id)
    departments = Department.objects.all()
    users = UserAccount.objects.filter(role='teacher')

    if request.method == 'POST':
        teacher.useraccount_id = request.POST.get('useraccount') or None
        teacher.name = request.POST.get('name')
        teacher.email = request.POST.get('email')
        teacher.department_id = request.POST.get('department')
        teacher.save()
        return redirect('teacher_list')

    return render(request, 'edit_teacher.html', {
        'teacher': teacher,
        'departments': departments,
        'users': users,
    })


def delete_teacher(request, id):
    if request.session.get('role') != 'admin':
        return redirect('/')

    teacher = Teacher.objects.get(id=id)
    teacher.delete()
    return redirect('teacher_list')


def teacher_schedule_list(request):
    schedules = TeacherClassSchedule.objects.all()
    return render(request, 'teacher_schedule_list.html', {'schedules': schedules})


# =========================================================
# ADMIN SECTION
# =========================================================

def admin_dashboard(request):
    if request.session.get('role') != 'admin':
        return redirect('/')

    students = Student.objects.all().order_by('id')
    teachers = Teacher.objects.all().order_by('id')
    courses = Course.objects.all().order_by('id')
    departments = Department.objects.all().order_by('id')
    attendances = Attendance.objects.all().order_by('id')
    fees = Fee.objects.all().order_by('id')
    results = Result.objects.all().order_by('id')
    exams = ExamTimeTable.objects.all().order_by('id')
    class_timings = ClassTiming.objects.all().order_by('id')
    teacher_schedules = TeacherClassSchedule.objects.all().order_by('id')

    total_students = students.count()
    total_teachers = teachers.count()
    total_courses = courses.count()
    total_departments = departments.count()
    total_attendance = attendances.count()
    total_fees = fees.count()
    total_results = results.count()
    total_exams = exams.count()

    low_attendance_students = []

    attendance_present_count = 0
    attendance_absent_count = 0

    course_labels = []
    course_student_counts = []

    result_labels = []
    result_marks_data = []

    fee_status_labels = ['Paid', 'Pending']
    fee_status_counts = [0, 0]

    exam_labels = []
    exam_counts = []

    department_labels = []
    department_teacher_counts = []

    for student in students:
        student_attendance = Attendance.objects.filter(student=student)
        total_classes = student_attendance.count()
        present_classes = student_attendance.filter(status='Present').count()

        attendance_percentage = 0
        if total_classes > 0:
            attendance_percentage = (present_classes / total_classes) * 100

        if attendance_percentage < 75:
            low_attendance_students.append({
                'student': student,
                'total_classes': total_classes,
                'present_classes': present_classes,
                'attendance_percentage': round(attendance_percentage, 2),
            })

    attendance_present_count = attendances.filter(status='Present').count()
    attendance_absent_count = attendances.filter(status='Absent').count()

    for course in courses:
        course_labels.append(course.name)
        course_student_counts.append(Student.objects.filter(course=course).count())

    recent_results_for_chart = results.order_by('-id')[:6]
    for result in reversed(recent_results_for_chart):
        label = f"{result.student.name} - {result.course.name}"
        result_labels.append(label)
        result_marks_data.append(result.marks)

    paid_count = fees.filter(status__iexact='Paid').count()
    pending_count = fees.filter(status__iexact='Pending').count()
    fee_status_counts = [paid_count, pending_count]

    for course in courses:
        exam_labels.append(course.name)
        exam_counts.append(ExamTimeTable.objects.filter(course=course).count())

    for department in departments:
        department_labels.append(department.name)
        department_teacher_counts.append(Teacher.objects.filter(department=department).count())

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_courses': total_courses,
        'total_departments': total_departments,
        'total_attendance': total_attendance,
        'total_fees': total_fees,
        'total_results': total_results,
        'total_exams': total_exams,
        'students': students,
        'teachers': teachers,
        'courses': courses,
        'departments': departments,
        'attendances': attendances,
        'fees': fees,
        'results': results,
        'exams': exams,
        'class_timings': class_timings,
        'teacher_schedules': teacher_schedules,
        'low_attendance_students': low_attendance_students,
        'attendance_present_count': attendance_present_count,
        'attendance_absent_count': attendance_absent_count,
        'course_labels': course_labels,
        'course_student_counts': course_student_counts,
        'result_labels': result_labels,
        'result_marks_data': result_marks_data,
        'fee_status_labels': fee_status_labels,
        'fee_status_counts': fee_status_counts,
        'exam_labels': exam_labels,
        'exam_counts': exam_counts,
        'department_labels': department_labels,
        'department_teacher_counts': department_teacher_counts,
    }

    return render(request, 'admin_dashboard.html', context)


def charts_dashboard(request):
    if request.session.get('role') != 'admin':
        return redirect('/')

    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_courses = Course.objects.count()
    total_departments = Department.objects.count()
    total_fees = Fee.objects.count()
    total_results = Result.objects.count()
    total_attendance = Attendance.objects.count()

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_courses': total_courses,
        'total_departments': total_departments,
        'total_fees': total_fees,
        'total_results': total_results,
        'total_attendance': total_attendance,
    }

    return render(request, 'charts_dashboard.html', context)


# =========================================================
# DEPARTMENT SECTION
# =========================================================

def departments_list(request):
    if request.session.get('role') != 'admin':
        return redirect('/')

    departments = Department.objects.all()
    return render(request, 'department_list.html', {'departments': departments})


def add_department(request):
    if request.session.get('role') != 'admin':
        return redirect('/')

    if request.method == 'POST':
        Department.objects.create(
            name=request.POST.get('name')
        )
        return redirect('departments_list')

    return render(request, 'add_department.html')


def edit_department(request, id):
    if request.session.get('role') != 'admin':
        return redirect('/')

    department = get_object_or_404(Department, id=id)

    if request.method == 'POST':
        department.name = request.POST.get('name')
        department.save()
        return redirect('departments_list')

    return render(request, 'edit_department.html', {
        'department': department
    })


def delete_department(request, id):
    if request.session.get('role') != 'admin':
        return redirect('/')

    department = get_object_or_404(Department, id=id)
    department.delete()
    return redirect('departments_list')


# =========================================================
# COURSE SECTION
# =========================================================

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})


def add_course(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        department_id = request.POST.get('department')

        print("name =", name)
        print("department_id =", department_id)

        if name and department_id:
            try:
                department = Department.objects.get(id=department_id)

                if Course.objects.filter(name__iexact=name, department=department).exists():
                    print("Course already exists")
                    return redirect('admin_dashboard')

                course = Course.objects.create(
                    name=name,
                    department=department
                )

                print("COURSE SAVED:", course.id, course.name, course.department.name)
                return redirect('admin_dashboard')

            except Department.DoesNotExist:
                print("Department not found")
            except Exception as e:
                print("Error while saving course:", e)
        else:
            print("Name or Department missing")

    return redirect('admin_dashboard')


def edit_course(request, id):
    course = get_object_or_404(Course, id=id)
    departments = Department.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        department_id = request.POST.get('department')

        if name and department_id:
            department = Department.objects.get(id=department_id)
            course.name = name
            course.department = department
            course.save()
            return redirect('course_list')

    return render(request, 'edit_course.html', {
        'course': course,
        'departments': departments
    })


def delete_course(request, id):
    course = get_object_or_404(Course, id=id)
    course.delete()
    return redirect('course_list')


# =========================================================
# ATTENDANCE SECTION
# =========================================================

def attendance_list(request):
    attendance = Attendance.objects.all()
    return render(request, 'attendance_list.html', {'attendance': attendance})


def add_attendance(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        course_id = request.POST.get('course')
        date = request.POST.get('date')
        status = request.POST.get('status')
        section = request.POST.get('section', 'attendanceSection')

        if student_id and course_id and date and status:
            Attendance.objects.create(
                student_id=student_id,
                course_id=course_id,
                date=date,
                status=status
            )

        if request.session.get('role') == 'teacher':
            return redirect(f'/teacher_dashboard/?section={section}')
        return redirect('/attendance/')

    return redirect('/teacher_dashboard/?section=addAttendanceSection')


def edit_attendance(request, id):
    attendance = get_object_or_404(Attendance, id=id)
    courses = Course.objects.all()

    if request.method == 'POST':
        course_id = request.POST.get('course')
        date = request.POST.get('date')
        status = request.POST.get('status')

        attendance.date = date
        attendance.status = status

        if course_id:
            attendance.course = get_object_or_404(Course, id=course_id)
        else:
            attendance.course = None

        attendance.save()
        return redirect('attendance_list')

    return render(request, 'edit_attendance.html', {
        'attendance': attendance,
        'courses': courses
    })


def delete_attendance(request, id):
    attendance_obj = get_object_or_404(Attendance, id=id)
    attendance_obj.delete()
    return redirect('attendance_list')


# =========================================================
# RESULT SECTION
# =========================================================

def result_list(request):
    results = Result.objects.all().order_by('id')
    return render(request, 'admin_dashboard.html', {'results': results})


def add_result(request):
    students = Student.objects.all()
    courses = Course.objects.all()

    if request.method == "POST":
        student_id = request.POST.get('student')
        subject = request.POST.get('subject')
        course_id = request.POST.get('course')
        marks = request.POST.get('marks')
        grade = request.POST.get('grade')

        if not student_id or not subject or not course_id or not marks or not grade:
            return render(request, 'add_result.html', {
                'students': students,
                'courses': courses,
                'error': 'All fields are required'
            })

        student = get_object_or_404(Student, id=student_id)
        course = get_object_or_404(Course, id=course_id)

        if Result.objects.filter(student=student, course=course, subject=subject).exists():
            return render(request, 'add_result.html', {
                'students': students,
                'courses': courses,
                'error': 'This student result for the selected course and subject already exists.'
            })

        Result.objects.create(
            student=student,
            subject=subject,
            course=course,
            marks=marks,
            grade=grade
        )

        return redirect('result_list')

    return render(request, 'add_result.html', {
        'students': students,
        'courses': courses
    })


def edit_result(request, id):
    result = get_object_or_404(Result, id=id)
    students = Student.objects.all()
    courses = Course.objects.all()

    if request.method == "POST":
        student_id = request.POST.get('student')
        course_id = request.POST.get('course')
        subject = request.POST.get('subject')
        marks = request.POST.get('marks')
        grade = request.POST.get('grade')

        if not student_id or not course_id or not subject or not marks or not grade:
            return render(request, 'edit_result.html', {
                'result': result,
                'students': students,
                'courses': courses,
                'error': 'All fields are required'
            })

        student = get_object_or_404(Student, id=student_id)
        course = get_object_or_404(Course, id=course_id)

        duplicate = Result.objects.filter(
            student=student,
            course=course,
            subject=subject
        ).exclude(id=result.id).exists()

        if duplicate:
            return render(request, 'edit_result.html', {
                'result': result,
                'students': students,
                'courses': courses,
                'error': 'This student result for the selected course and subject already exists.'
            })

        result.student = student
        result.course = course
        result.subject = subject
        result.marks = marks
        result.grade = grade
        result.save()

        return redirect('result_list')

    return render(request, 'edit_result.html', {
        'result': result,
        'students': students,
        'courses': courses
    })


def delete_result(request, id):
    result = get_object_or_404(Result, id=id)
    result.delete()
    return redirect('result_list')


# =========================================================
# FEES SECTION
# =========================================================

def fees_list(request):
    if request.session.get('role') != 'admin':
        return redirect('/')

    fees = Fee.objects.all()
    return render(request, 'fees_list.html', {'fees': fees})


def add_fee(request):
    students = Student.objects.all()
    courses = Course.objects.all()

    if request.method == 'POST':
        student_id = request.POST.get('student')
        course_id = request.POST.get('course')
        amount = request.POST.get('amount')
        pending_amount = request.POST.get('pending_amount')
        status = request.POST.get('status')
        due_date = request.POST.get('due_date')

        if not student_id or not course_id or not amount or not status or not due_date:
            return render(request, 'add_fee.html', {
                'students': students,
                'courses': courses,
                'error': 'Please fill all required fields'
            })

        student = Student.objects.get(id=student_id)
        course = Course.objects.get(id=course_id)

        Fee.objects.create(
            student=student,
            course=course,
            amount=amount,
            pending_amount=pending_amount or 0,
            status=status,
            due_date=due_date
        )

        return redirect('fees_list')

    return render(request, 'add_fee.html', {
        'students': students,
        'courses': courses
    })


def edit_fee(request, id):
    if request.session.get('role') != 'admin':
        return redirect('/')

    fee = get_object_or_404(Fee, id=id)
    students = Student.objects.all()

    if request.method == 'POST':
        fee.student_id = request.POST.get('student')
        fee.amount = request.POST.get('amount')
        fee.status = request.POST.get('status')
        fee.due_date = request.POST.get('due_date')
        fee.save()
        return redirect('fees_list')

    return render(request, 'edit_fee.html', {
        'fee': fee,
        'students': students,
    })


def delete_fee(request, id):
    if request.session.get('role') != 'admin':
        return redirect('/')

    fee = get_object_or_404(Fee, id=id)
    fee.delete()
    return redirect('fees_list')


# =========================================================
# EXAM TIMETABLE SECTION
# =========================================================

def exam_timetable_list(request):
    exams = ExamTimeTable.objects.all()
    return render(request, 'exam_timetable_list.html', {'exams': exams})


def add_exam_timetable(request):
    courses = Course.objects.all()
    teachers = Teacher.objects.all()

    subjects = [
        "Data Structures",
        "DBMS",
        "Operating System",
        "Computer Networks",
        "Software Engineering",
        "Python Programming",
        "Java",
        "Artificial Intelligence",
        "Machine Learning",
        "Compiler Design"
    ]

    if request.method == "POST":
        course_id = request.POST.get('course')
        subject = request.POST.get('subject')
        exam_date = request.POST.get('exam_date')
        timing = request.POST.get('timing')
        teacher_id = request.POST.get('teacher')
        room_no = request.POST.get('room_no')

        if not course_id or not subject or not exam_date or not timing or not room_no:
            return render(request, 'add_exam_timetable.html', {
                'courses': courses,
                'teachers': teachers,
                'subjects': subjects,
                'error': 'Please fill all required fields.'
            })

        course = Course.objects.get(id=course_id)
        teacher = Teacher.objects.get(id=teacher_id) if teacher_id else None

        ExamTimeTable.objects.create(
            course=course,
            subject=subject,
            exam_date=exam_date,
            timing=timing,
            teacher=teacher,
            room_no=room_no
        )

        return redirect('exam_timetable_list')

    return render(request, 'add_exam_timetable.html', {
        'courses': courses,
        'teachers': teachers,
        'subjects': subjects
    })


def edit_exam_timetable(request, id):
    exam = get_object_or_404(ExamTimeTable, id=id)
    courses = Course.objects.all()
    teachers = Teacher.objects.all()

    if request.method == 'POST':
        course_id = request.POST.get('course')
        exam_date = request.POST.get('exam_date')
        timing = request.POST.get('timing')
        teacher_id = request.POST.get('teacher')
        room_no = request.POST.get('room_no')

        if course_id and exam_date and timing and teacher_id and room_no:
            exam.course = Course.objects.get(id=course_id)
            exam.exam_date = exam_date
            exam.timing = timing
            exam.teacher = Teacher.objects.get(id=teacher_id)
            exam.room_no = room_no
            exam.save()

            return redirect('exam_timetable_list')

    return render(request, 'edit_exam_timetable.html', {
        'exam': exam,
        'courses': courses,
        'teachers': teachers,
    })


def delete_exam_timetable(request, id):
    exam = get_object_or_404(ExamTimeTable, id=id)
    exam.delete()
    return redirect('exam_timetable_list')


# =========================================================
# CLASS TIMING SECTION
# =========================================================

def class_timing_list(request):
    timings = ClassTiming.objects.all()
    return render(request, 'class_timing_list.html', {'timings': timings})


def add_class_timing(request):
    if request.session.get('role') != 'admin':
        return redirect('/')

    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        if start_time and end_time:
            ClassTiming.objects.create(
                start_time=start_time,
                end_time=end_time
            )
            return redirect('admin_dashboard')

    return render(request, 'add_class_timing.html')


def edit_class_timing(request, id):
    if request.session.get('role') != 'admin':
        return redirect('/')

    timing = ClassTiming.objects.get(id=id)

    if request.method == 'POST':
        timing.start_time = request.POST.get('start_time')
        timing.end_time = request.POST.get('end_time')
        timing.save()
        return redirect('admin_dashboard')

    return render(request, 'edit_class_timing.html', {'timing': timing})


def delete_class_timing(request, id):
    if request.session.get('role') != 'admin':
        return redirect('/')

    timing = ClassTiming.objects.get(id=id)
    timing.delete()
    return redirect('admin_dashboard')


# =========================================================
# TEACHER SCHEDULE SECTION
# =========================================================

def add_teacher_schedule(request):
    if request.session.get('role') != 'admin':
        return redirect('/')

    teachers = Teacher.objects.all()
    courses = Course.objects.all()
    class_timings = ClassTiming.objects.all()

    if request.method == 'POST':
        teacher_id = request.POST.get('teacher')
        course_id = request.POST.get('course')
        date = request.POST.get('date')
        day = request.POST.get('day')
        timing_id = request.POST.get('timing')
        room_no = request.POST.get('room_no')

        teacher = Teacher.objects.get(id=teacher_id)
        course = Course.objects.get(id=course_id)
        timing = ClassTiming.objects.get(id=timing_id)

        TeacherClassSchedule.objects.create(
            teacher=teacher,
            course=course,
            date=date,
            day=day,
            timing=timing,
            room_no=room_no
        )
        return redirect('admin_dashboard')

    context = {
        'teachers': teachers,
        'courses': courses,
        'class_timings': class_timings,
    }
    return render(request, 'add_teacher_schedule.html', context)


def edit_teacher_schedule(request, id):
    if request.session.get('role') != 'admin':
        return redirect('/')

    schedule = TeacherClassSchedule.objects.get(id=id)
    teachers = Teacher.objects.all()
    courses = Course.objects.all()
    class_timings = ClassTiming.objects.all()

    if request.method == 'POST':
        teacher_id = request.POST.get('teacher')
        course_id = request.POST.get('course')
        date = request.POST.get('date')
        day = request.POST.get('day')
        timing_id = request.POST.get('timing')
        room_no = request.POST.get('room_no')

        schedule.teacher = Teacher.objects.get(id=teacher_id)
        schedule.course = Course.objects.get(id=course_id)
        schedule.date = date
        schedule.day = day
        schedule.timing = ClassTiming.objects.get(id=timing_id)
        schedule.room_no = room_no
        schedule.save()

        return redirect('admin_dashboard')

    context = {
        'schedule': schedule,
        'teachers': teachers,
        'courses': courses,
        'class_timings': class_timings,
    }
    return render(request, 'edit_teacher_schedule.html', context)


def delete_teacher_schedule(request, id):
    if request.session.get('role') != 'admin':
        return redirect('/')

    schedule = TeacherClassSchedule.objects.get(id=id)
    schedule.delete()
    return redirect('admin_dashboard')