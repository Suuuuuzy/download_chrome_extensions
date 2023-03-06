import os
import json
crxDir = "extensions"
crx = os.listdir(crxDir)
zero_list = [i for i in crx if os.path.getsize(os.path.join(crxDir, i))==0]
with open('zero_file.txt', 'w') as f:
    json.dump(zero_list, f)
    print("zero:", len(zero_list))
    print("others:", len(crx)-len(zero_list))
