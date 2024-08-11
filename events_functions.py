import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from info_functions import get_all_events

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_creds():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


def get_events():
    creds = get_creds()

    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        print("Getting the upcoming 10 events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])

    except HttpError as error:
        print(f"An error occurred: {error}")


def create_event():
    creds = get_creds()
    service = build("calendar", "v3", credentials=creds)
    event_info = {
        "summary": "Surf Calendar",
        "start": {
            "dateTime": "2024-08-12T12:00:00-07:00",
            "timeZone": "Europe/Paris",
        },
        "end": {
            "dateTime": "2024-08-12T13:00:00-07:00",
            "timeZone": "Europe/Paris",
        },
    }
    event = service.events().insert(calendarId="primary", body=event_info).execute()
    print(f"Event created: {event['htmlLink']}")


def create_all_events():

    creds = get_creds()
    service = build("calendar", "v3", credentials=creds)

    # Step 1: Create a new calendar called "Surf Calendar"
    calendar = {"summary": "Surf Calendar", "timeZone": "Europe/Paris"}
    created_calendar = service.calendars().insert(body=calendar).execute()
    calendar_id = created_calendar["id"]

    print(f"Calendar created: {created_calendar['summary']} with ID: {calendar_id}")

    event_infos = get_all_events()

    # Step 3: Loop through the list and create events
    for event in event_infos:
        created_event = (
            service.events().insert(calendarId=calendar_id, body=event).execute()
        )
        print(f"Event created: {created_event['htmlLink']}")
