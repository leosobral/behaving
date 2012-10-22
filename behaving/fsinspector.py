import os
import time
from shutil import rmtree


class FSInspector(object):

    def __init__(self, path, timeout=5):
        self.path = path
        self.timeout = timeout

    def messages_for_user(self, user):
        user_path = os.path.join(self.path, user)
        try:
            root, dirs, paths = os.walk(user_path).next()
        except StopIteration:
            return []

        if paths:
            paths.sort()

        messages = []
        for path in paths:
            path = os.path.join(user_path, path)
            with open(path, 'r') as f:
                messages.append(f.read())
        return messages

    def user_messages(self, user, f=None):
        messages = []
        start = time.time()
        while time.time() - start < self.timeout:
            messages = filter(f, self.messages_for_user(user))
            if messages:
                break
            time.sleep(0.2)
        return messages

    def clear(self):

        dirs = os.listdir(self.path)
        for dir_path in dirs:
            rmtree(os.path.join(self.path, dir_path))
