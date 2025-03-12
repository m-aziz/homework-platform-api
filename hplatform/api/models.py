from django.db import models
from django.contrib.auth.models import User

# Student Model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

# Teacher Model
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


# Assignment Model
class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.created_by.user.username}"


# Submission Model
class Submission(models.Model):
    GRADE_CHOICES = [
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'),
        ('incomplete', 'Incomplete'), ('ungraded', 'Ungraded')
    ]
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='submissions')
    submission_date = models.DateTimeField(auto_now_add=True)
    homework_text = models.TextField(blank=True, null=True)
    grading_date = models.DateTimeField(null=True, blank=True)
    final_grade = models.CharField(max_length=20, choices=GRADE_CHOICES, default='ungraded')
    teacher_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.assignment.title}"