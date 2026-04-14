from django.contrib import admin
from .models import Department, Course, Student, Teacher, Attendance, Result, Fee, UserAccount, ClassTiming, TeacherClassSchedule, ExamTimeTable


@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'get_student_name', 'get_student_course', 'get_student_semester')

    def get_student_name(self, obj):
        return obj.student_profile.name if hasattr(obj, 'student_profile') and obj.student_profile else "-"
    get_student_name.short_description = 'Student Name'

    def get_student_course(self, obj):
        if hasattr(obj, 'student_profile') and obj.student_profile and obj.student_profile.course:
            return obj.student_profile.course.name
        return "-"
    get_student_course.short_description = 'Course'

    def get_student_semester(self, obj):
        return obj.student_profile.semester if hasattr(obj, 'student_profile') and obj.student_profile else "-"
    get_student_semester.short_description = 'Semester'


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status')



@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'marks', 'grade']

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'status', 'due_date')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone', 'department', 'course']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'department']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'department']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    
admin.site.register(ClassTiming)
admin.site.register(TeacherClassSchedule)
admin.site.register(ExamTimeTable)    