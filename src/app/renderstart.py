import subprocess

subprocess.call(["python", "reset-db.py"])
subprocess.call(["webpy", "run"])