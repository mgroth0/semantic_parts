import urllib.request
import json
import base64

ProlificPID = "TEST"

contents = urllib.request.urlopen(
    f"https://www.wolframcloud.com/obj/57e6c253-77f4-4f4c-9148-d533ed5d302f?PID={ProlificPID}"
).read()
contents = contents.decode('utf-8')
contents = '[' + contents[1:-1] + ']'
codes = json.loads(str(contents))
for base64_string in codes:
    base64_bytes = base64_string.encode('ascii')
    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")
    sample_data = json.loads(sample_string)
    print(f"{sample_data=}")
