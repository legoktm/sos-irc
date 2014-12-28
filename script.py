#!/usr/bin/env python
from __future__ import print_function

import json
import os
import requests
import time
import twitter
import ur1

fname = os.path.expanduser('~/.sos-irc.json')
if not os.path.exists(fname):
    raise Exception('Error: %s does not exist.' % fname)
with open(fname, 'r') as f:
    conf = json.load(f)

ircnotifier_key = conf.pop('ircnotifier_key')
api = twitter.Api(**conf)


def build_url(_id):
    return ur1.shorten('https://twitter.com/swiftonsecurity/status/%s' % _id)


def send(msg):
    print(msg)
    requests.post('http://ircnotifier-test-01/v1/send', data={
        'token': ircnotifier_key,
        'channels': '#mediawiki-core',
        'message': msg
    })
    pass

last_id = None
first_run = True
while True:
    statuses = api.GetUserTimeline(screen_name='swiftonsecurity', exclude_replies=True, since_id=last_id)
    for status in statuses:
        print(status.id)
        if status.id > last_id:
            last_id = status.id
        if not first_run:
            send(
                status.text.replace('\n', ' ').replace('\r', ' ')
                + ' '.join(u.url for u in status.urls)
                + ' - ' + build_url(status.id)
            )
    first_run = True
    time.sleep(60)
