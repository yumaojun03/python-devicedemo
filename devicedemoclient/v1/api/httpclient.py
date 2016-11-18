import requests


class HTTPClient(object):

    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token

    def get(self, url):
        return requests.get(self.base_url + url, headers={'x-auth-token': self.token})

    def post(self, url, body, json=True):
        headers = {'x-auth-token': self.token}
        if json:
            headers['content-type'] = 'application/json'
        return requests.post(self.base_url + url, body, headers=headers)

    def put(self, url, body, json=True):
        headers = {'x-auth-token': self.token}
        if json:
            headers['content-type'] = 'application/json'
        return requests.put(self.base_url + url, body, headers=headers)

    def delete(self, url):
        return requests.delete(self.base_url + url, headers={'x-auth-token': self.token})
