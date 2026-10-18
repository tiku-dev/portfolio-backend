from rest_framework.throttling import AnonRateThrottle


class ContactSubmissionThrottle(AnonRateThrottle):
    scope = 'contact'

