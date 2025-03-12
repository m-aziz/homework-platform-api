from django.contrib import admin
from .models import Student, Teacher, Assignment, Submission

# Registering the models
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Assignment)
admin.site.register(Submission)