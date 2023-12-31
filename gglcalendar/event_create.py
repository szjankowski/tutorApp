from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import uuid
from gglcalendar.utils import get_credentials_from_refresh_token
from django.contrib import messages


def create_calendar_event(lesson):
    # Load the tutor's credentials from the user model
    tutor_refresh_token = lesson.tutor.google_credentials["refresh_token"]

    refresh_token = tutor_refresh_token

    credentials = get_credentials_from_refresh_token(refresh_token)

    service = build("calendar", "v3", credentials=credentials)

    start_time = datetime.combine(lesson.date, lesson.start_time).isoformat()

    end_datetime = datetime.combine(lesson.date, lesson.start_time) + timedelta(
        minutes=lesson.duration
    )

    # Convert the lesson end time to RFC3339 format
    end_time = end_datetime.isoformat()

    event = {
        "summary": lesson.title,
        "description": lesson.description,
        "start": {
            "dateTime": start_time,
            "timeZone": "UTC",
        },
        "end": {
            "dateTime": end_time,
            "timeZone": "UTC",
        },
        "conferenceData": {
            "createRequest": {
                "requestId": str(uuid.uuid4()),  # Generate a unique ID for the request
                "conferenceSolutionKey": {"type": "hangoutsMeet"},
            }
        },
        "attendees": [
            {"email": lesson.student.email},  # Invite the student to the event
        ],
    }

    # Call the Calendar API to create the event
    event = (
        service.events()
        .insert(calendarId="primary", body=event, conferenceDataVersion=1)
        .execute()
    )
    # Save the Google Meet link in the lesson
    return event
