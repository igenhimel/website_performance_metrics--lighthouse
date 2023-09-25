import requests
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.middleware.csrf import get_token
from django.http import HttpRequest

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'default')
    register_events(scheduler)

    def auto_hello():
        # Create a dummy request object
        request = HttpRequest()

        # Get the CSRF token
        csrf_token = get_token(request)

        # Add the CSRF token to the request headers
        request.META['HTTP_X_CSRFTOKEN'] = csrf_token

        response = requests.post('http://localhost:8000')  # Include the scheme (http://) in the URL
        if response.status_code == 200:
            print("SEO checker called successfully")

    scheduler.add_job('module:start.auto_hello', 'interval', seconds=1, id='auto_hello', name='start:auto_hello')
    scheduler.start()