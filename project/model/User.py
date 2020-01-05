
import json

class User(object):

    def __init__(self, name, email, password):
        self.email = email
        self.name = name
        self.password = password
        self.dbs = []

    def toJson(self):
        output = {
            "email": self.email,
            "name": self.name,
            "dbs": self.dbs,
        }
        return json.dumps(output)

