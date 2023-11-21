from flask import Flask, request
import os
import subprocess
import sys
import threading
import queue
from monitor import monitor, condition, entry

app = Flask(__name__)
app.config["DEBUG"] = False

post_script = os.getenv("POST_SCRIPT")
webhook_token = os.getenv("WEBHOOK_TOKEN")

class coda(monitor):
    def __init__(self, size=1):
        super().__init__()
        self.ok2pop = condition(self)
        self.deploy_ongoing = False

    @entry
    def deploy(self):
        if self.deploy_ongoing:
            print("Waiting for previous deploy to end",flush=True)
            self.ok2pop.wait()
        print("Deploying", flush=True)
        self.deploy_ongoing = True
        try:
            output = subprocess.check_output(
                post_script, executable='/bin/bash', shell=True,
                stderr=subprocess.STDOUT, universal_newlines=True)
        except subprocess.CalledProcessError as er:
            print(er.output, file=sys.stderr)
        else:
            print(output, file=sys.stderr)
        self.deploy_ongoing = False
        print("Deploy ended", flush=True)
        self.ok2pop.signal()

coda = coda()

@app.route("/", methods=["POST"])
def root():
    global webhook_token
    request_token = request.headers.get('X-Gitlab-Token')

    if not request_token or request_token != webhook_token:
        return "Unauthorized", 401

    event_type = request.headers.get('X-Gitlab-Event')

    if event_type == 'Push Hook':
        print("Received push event", flush=True)
        t = threading.Thread(target=coda.deploy)
        print("Add event to queue", flush=True)
        t.start()

    return "Ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
