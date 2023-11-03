from flask import Flask, request
import os
import subprocess
import sys
import threading

app = Flask(__name__)
app.config["DEBUG"] = False

post_script = os.getenv("POST_SCRIPT")
webhook_token = os.getenv("WEBHOOK_TOKEN")


def deploy():
  try:
      output = subprocess.check_output(
          post_script, executable='/bin/bash', shell=True,
          stderr=subprocess.STDOUT, universal_newlines=True)
      print("Deploy completed", flush=True)
  except subprocess.CalledProcessError as er:
      print(er.output, file=sys.stderr)
      return False, er.output
  else:
      print(output, file=sys.stderr)
      return True, output


@app.route("/", methods=["POST"])
def root():
    global webhook_token
    request_token = request.headers.get('X-Gitlab-Token')

    if not request_token or request_token != webhook_token:
        return "Unauthorized", 401

    data = request.get_json()

    event_type = request.headers.get('X-Gitlab-Event')

    if event_type == 'Push Hook':
        print("Received push event", flush=True)
        t = threading.Thread(target=deploy)
        print("Starting deploy", flush=True)
        t.start()

    return "Ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
