from django.urls import path
from .views import (
    SubmissionCreateView,
    SubmissionListView,
    SubmissionUpdateView,
    AssignmentViewSet
)

urlpatterns = [
    path('submissions/create/', SubmissionCreateView.as_view(), name='submission-create'),
    path('submissions/', SubmissionListView.as_view(), name='submission-list'),
    path('submissions/<int:pk>/update/', SubmissionUpdateView.as_view(), name='submission-update'),
    path('assignments/', AssignmentViewSet.as_view(), name='assignment-list-create'),
]