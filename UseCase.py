#summary Things to do with Factory

Note: I haven't tried many of these.

= Factory =

== Alarm Clock ==
Here's a sketch of an alarm clock.  We can inspect & even modify the Factory's argument binding's after creating it - something that cannot be done with a lambda.

{{{
def run_at_time(func, time):
    """run callable func some time in the future"""
    # register func w/ event loop, etc..
    pass

@attributeFactory
def play_mp3(fname):
    """play mp3 file at fname"""
    pass

# create new alarm
my_alarm = play_mp3.factory("Beatles.mp3", time(2, 25, 00)
run_at_time(my_alarm)

# show the alarm
print "At", alarm.time, "you'll hear the sweet sounds of" alarm.fname[:-4]

# change the song we're going to play
alarm.fname = "Hendrix.mp3"
}}}


== Django-style URLConf ==
Factories should play nicely with Django-style URL conf:

[http://docs.djangoproject.com/en/dev/ref/contrib/syndication/#ref-contrib-syndication  Based on Django Docs]
{{{

# from django docs: 
(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),

# using factory:
attributeFactory(django.contrib.syndication.views.feed) # add .factory(..) to existing django func
(r'^feeds/(?P<url>.*)/$', django.contrib.syndication.views.feed.factory(feed_dict=feeds),
}}}

== Twisted Callbacks ==

{{{

class WebPageMonitor(object):
    def __init__(self, sysadmin_email):
        self.sysadmin_email = sysadmin_email
    
    @factoryDescriptor
    def alert(self, x, url, status):
        msg = "Things at", url, "are", status, "because", x
        SMTP.mail(msg, to=self.sysadmin_email)

monitor = WebPageMonitor("root@host.com")

def checkPage(url):
    """check on page at URL.  Returns deferred"""

def twisted_closure_style(urls_to_check):
    for url in urls_to_check:
        d = checkPage(url) 
        
        def callBack(x):
            monitor.alert(x, url=url, status="all cool") 

        def errBack(x):
            monitor.alert(x, url=url, status="on fire")

        d.addCallback(callBack))
        d.addErrback(errBack)

def factory_style(urls_to_check):
    for url in urls_to_check:
        d = checkPage(url)
        d.addCallback(monitor.alert.factory(status="all cool", url=url))
        d.addErrback(monitor.alert.factory(status="on fire", url=url))

def lambda_style(urls_to_check):
    for url in urls_to_check:
        d = checkPage(url)
        d.addCallback(lambda x: monitor.alert(x, status="all cool", url=url))
        d.addErrback(lambda x: monitor.alert(x, status="on fire", url=url))
}}}



= ObjectTemplate=

ObjectTemplate can be used for configuration:

{{{
config = ObjectTemplate()

# in production
config.path = "/var/myapp/"
config.debug_level = logging.WARN

# in tests
config.path = Factory(tempfile.mktemp)
config.debug_level = logging.DEBUG

# app code
def do_stuff_with_config(config):
     config = config() # call any factories
     
     output = file(config.path)
     logging.setLevel(config.debug_level)
}}}
