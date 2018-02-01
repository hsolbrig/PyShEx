import os
import requests


# Retrieve test data from the wikidata site
data_url = "http://www.wikidata.org/entity/Q18557112.ttl"
text = requests.get(data_url).text
out_file = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'data', 'Q18557122.ttl')
with open(out_file, 'w') as f:
    f.write(text)
print(f"{out_file} written")
