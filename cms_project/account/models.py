from django.db import models
from django.contrib.auth.models import AbstractUser




class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name    


class Course(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    semester = models.CharField(max_length=20, blank=True, null=True)
    enrollment_no = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    useraccount = models.OneToOneField(
        'UserAccount',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='teacher_profile'
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class ClassTiming(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


class TeacherClassSchedule(models.Model):
    DAY_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    )
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    day = models.CharField(max_length=20)
    timing = models.ForeignKey(ClassTiming, on_delete=models.CASCADE)
    room_no = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.teacher.name} - {self.course.name} - {self.day}"
    

class ExamTimeTable(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    exam_date = models.DateField()
    timing = models.CharField(max_length=50)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    room_no = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.course.name} - {self.exam_date}"


class UserAccount(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    security_question = models.CharField(max_length=255, blank=True, null=True)
    security_answer = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username


class Attendance(models.Model):

    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent')
    ]

    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"


class Result(models.Model):

    GRADE_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('Fail', 'Fail')
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True, null=True)

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.IntegerField()
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES)

    # ✅ duplicate रोकने के लिए
    
    class Meta:
        unique_together = ('student', 'course', 'subject')

    def __str__(self):
        return f"{self.student.name} - {self.course.name} - {self.subject}"


class Fee(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    pending_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20)
    due_date = models.DateField()

    def __str__(self):
        return f"{self.student.name} - {self.amount}"