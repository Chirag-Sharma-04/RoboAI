import subprocess
import select
import sys

env_name = "ros2_env"
cmd = f"conda activate ros && \
    ros2 topic echo /chatter"

# Start zsh interactive shell running the command
process = subprocess.Popen(
    f"zsh -i -c '{cmd}'",
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1  # line buffered
)

# Use select to wait for data on either stdout or stderr
while True:
    reads = [process.stdout.fileno(), process.stderr.fileno()]
    ret = select.select(reads, [], [])

    for fd in ret[0]:
        if fd == process.stdout.fileno():
            line = process.stdout.readline()
            if line:
                print(line, end='')
        if fd == process.stderr.fileno():
            line = process.stderr.readline()
            if line:
                print("ERR:", line, end='')

    # Check if process has ended
    if process.poll() is not None:
        break

# Read any remaining output after process ends
for line in process.stdout:
    print(line, end='')
for line in process.stderr:
    print("ERR:", line, end='')

process.stdout.close()
process.stderr.close()
