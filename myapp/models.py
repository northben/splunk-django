import json
import os
import threading

import requests

from django.core import serializers
from django.db import models


HEADERS = {
    "Authorization": "Splunk {}".format(os.environ['AUTH_TOKEN'])
}


class MyModel(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)
    foo = models.CharField(max_length=255, default='')


def after_save(sender, **kwargs):

    serialized_queryset = serializers.serialize("json", [kwargs['instance']])
    this_instance = json.loads(serialized_queryset)[0]

    args = {
        'url': os.environ['SPLUNK_URL'],
        'headers': HEADERS,
        'data': json.dumps({'event': this_instance}),
        'verify': False,
    }

    PostAsync(args).start()

models.signals.post_save.connect(after_save, sender=MyModel)


class PostAsync(threading.Thread):

    def __init__(self, args, **kwargs):
        self.args = args
        super(PostAsync, self).__init__(**kwargs)

    def run(self):
        requests.post(**self.args)
