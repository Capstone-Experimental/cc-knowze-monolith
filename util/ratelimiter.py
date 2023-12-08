from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class MyMinuteThrottle(AnonRateThrottle):
    scope = 'minute'
    rate = '1/minute'

class MyDailyThrottle(UserRateThrottle):
    scope = 'day'
    rate = '10/day'  