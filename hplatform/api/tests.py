from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from api.models import Student, Teacher, Assignment, Submission
from rest_framework.authtoken.models import Token
from django.utils.timezone import now

class HomeworkSubmissionTests(APITestCase):

    def setUp(self):
        # Create Users
        self.student_user = User.objects.create_user(username="student1", password="password123")
        self.teacher_user = User.objects.create_user(username="teacher1", password="password123")

        # Create Student & Teacher Profiles
        self.student = Student.objects.create(user=self.student_user)
        self.teacher = Teacher.objects.create(user=self.teacher_user)

        # Generate Auth Tokens
        self.student_token = Token.objects.create(user=self.student_user)
        self.teacher_token = Token.objects.create(user=self.teacher_user)

        # Create Assignments
        self.assignment1 = Assignment.objects.create(title="Math Homework", description="Solve algebra problems", created_by=self.teacher)
        self.assignment2 = Assignment.objects.create(title="Science Project", description="Write a science report", created_by=self.teacher)

        # Create a Submission
        self.submission = Submission.objects.create(
            assignment=self.assignment1,
            student=self.student,
            submission_date=now(),
            homework_text="x = 5, y = 10",
            final_grade="ungraded",
            teacher_notes=None
        )

    def test_student_can_submit_homework(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.student_token.key)
        response = self.client.post("/api/submissions/create/", {
            "assignment": self.assignment1.id,
            "homework_text": "Here is my answer"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_teacher_cannot_submit_homework(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.teacher_token.key)
        response = self.client.post("/api/submissions/create/", {
            "assignment": self.assignment1.id,
            "homework_text": "I am a teacher trying to submit"
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_can_view_own_submissions(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.student_token.key)
        response = self.client.get("/api/submissions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should only see their own submission

    def test_student_cannot_view_other_students_submissions(self):
        another_student_user = User.objects.create_user(username="student2", password="password123")
        another_student = Student.objects.create(user=another_student_user)
        another_student_token = Token.objects.create(user=another_student_user)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + another_student_token.key)
        response = self.client.get("/api/submissions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Should see no submissions

    def test_student_can_filter_by_grade(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.student_token.key)
        response = self.client.get(f"/api/submissions/?final_grade=ungraded")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_student_can_filter_by_assignment(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.student_token.key)
        response = self.client.get(f"/api/submissions/?search=Math")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_teacher_can_view_all_submissions(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.teacher_token.key)
        response = self.client.get("/api/submissions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)  # Teacher sees all students' submissions

    def test_teacher_can_filter_by_student_name(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.teacher_token.key)
        response = self.client.get(f"/api/submissions/?student_name=student1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_teacher_can_filter_by_date_range(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.teacher_token.key)
        response = self.client.get(f"/api/submissions/?start_date=2024-01-01&end_date=2025-12-31")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_teacher_can_grade_submission(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.teacher_token.key)
        response = self.client.patch(f"/api/submissions/{self.submission.id}/update/", {
            "final_grade": "A",
            "teacher_notes": "Excellent work!"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["final_grade"], "A")
        self.assertEqual(response.data["teacher_notes"], "Excellent work!")

    def test_student_cannot_grade_submission(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.student_token.key)
        response = self.client.patch(f"/api/submissions/{self.submission.id}/update/", {
            "final_grade": "B",
            "teacher_notes": "Good effort"
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Only teachers can grade