import sys
import base64

temp_json = sys.argv[1]
temp_json = sys.argv[2]
temp_json = sys.argv[3]
print(base64.b64encode(temp_json.encode('utf-8')))