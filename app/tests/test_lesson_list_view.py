from django.test import TestCase
from users.models import CustomUser
from model_bakery import baker
from django.urls import reverse
from unittest.mock import patch
from tutors.models import Lesson
from datetime import time, date

GGC_HANGOUTLINK = "https://calendar.google.com/"


class LessonListViewTest(TestCase):
    def setUp(self):
        self.mock_create_calendar_event = patch(
            "tutors.models.create_calendar_event",
            return_value=dict(hangoutLink=GGC_HANGOUTLINK),
        )
        self.mock_create_calendar_event.start()

        self.student = baker.make(CustomUser, is_tutor=False)
        self.tutor = baker.make(CustomUser, is_tutor=True)
        self.lesson = baker.make(
            Lesson,
            student=self.student,
            tutor=self.tutor,
            date=date.today(),
            start_time=time(10, 0),
            duration=60,
        )
        self.other_lessons = baker.make(Lesson, _quantity=3)

    def tearDown(self):
        self.mock_create_calendar_event.stop()

    def test_lessons_list_for_student(self):
        self.assert_lessons_list(
            self.student, Lesson.objects.filter(student=self.student)
        )

    def test_lessons_list_for_tutor(self):
        self.assert_lessons_list(self.tutor, Lesson.objects.filter(tutor=self.tutor))

    def test_no_lessons_for_unassociated_student(self):
        unassociated_user = baker.make(CustomUser, is_tutor=False)
        self.assert_lessons_list(unassociated_user, Lesson.objects.none())

    def assert_lessons_list(self, user, expected_queryset):
        self.client.force_login(user)
        response = self.client.get(reverse("lesson-list"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["lessons"],
            expected_queryset,
            transform=lambda x: x,
            ordered=False,
        )
