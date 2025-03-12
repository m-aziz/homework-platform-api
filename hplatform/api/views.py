import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.timezone import now
from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response

from .models import Assignment, Submission, Student, Teacher
from .serializers import AssignmentSerializer, SubmissionSerializer
from .permissions import IsStudent, IsTeacher


# Students can submit assignments
class SubmissionCreateView(generics.CreateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def perform_create(self, serializer):
        # Automatically set the student from the authenticated user
        serializer.save(student=self.request.user.student)

# Filter class used in SubmissionListView
class SubmissionFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="submission_date", lookup_expr="gte")
    end_date = django_filters.DateFilter(field_name="submission_date", lookup_expr="lte")
    student_name = django_filters.CharFilter(method='filter_by_student_name')

    class Meta:
        model = Submission
        fields = ['final_grade', 'assignment', 'start_date', 'end_date']

    def filter_by_student_name(self, queryset, name, value):
        return queryset.filter(student__user__username__icontains=value)

# Students & Teachers can view submissions
class SubmissionListView(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = SubmissionFilter  # Enables filtering by date range and student name
    search_fields = ['assignment__title']  # Enables search by assignment name

    def get_queryset(self):
        user = self.request.user
        # Students see only their own submissions
        if hasattr(user, 'student'):
            return Submission.objects.filter(student=user.student)
        # Teachers see all student submissions
        elif hasattr(user, 'teacher'):
            return Submission.objects.all()
        return Submission.objects.none()  # No access for other users


# Teachers can grade submissions
class SubmissionUpdateView(generics.UpdateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def update(self, request, *args, **kwargs):
        submission = self.get_object()

        # Ensure only teachers can grade the submission
        if not hasattr(request.user, 'teacher'):
            return Response({"error": "Only teachers can grade submissions."}, status=status.HTTP_403_FORBIDDEN)

        # Get the grade and teacher notes from request data
        final_grade = request.data.get("final_grade", submission.final_grade)
        teacher_notes = request.data.get("teacher_notes", submission.teacher_notes)

        # Validate that final_grade is within the allowed choices
        allowed_grades = ["A", "B", "C", "D", "E", "F", "incomplete", "ungraded"]
        if final_grade not in allowed_grades:
            return Response({"error": "Invalid grade. Must be A-F, incomplete, or ungraded."}, status=status.HTTP_400_BAD_REQUEST)

       # Update the submission with grading details
        submission.final_grade = final_grade
        submission.teacher_notes = teacher_notes
        submission.grading_date = now()
        submission.save()

        return Response(SubmissionSerializer(submission).data, status=status.HTTP_200_OK)

# Teachers can view and create assignments
class AssignmentViewSet(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        # Ensure the user is a teacher before assigning created_by
        if not hasattr(self.request.user, 'teacher'):
            raise serializers.ValidationError({"error": "Only teachers can create assignments."})

        serializer.save(created_by=self.request.user.teacher)