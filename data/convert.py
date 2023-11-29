# %%
import codecs
import osm2geojson
import json

with codecs.open('hcmute.osm', 'r', encoding='utf-8') as data:
    xml = data.read()

geojson = osm2geojson.xml2geojson(xml, filter_used_refs=False, log_level='INFO')
# Serializing json
def dumpToJson(data):
    json_object = json.dumps(data, indent=4)
 
    # Writing to sample.json
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)

# >> { "type": "FeatureCollection", "features": [ ... ] }

dumpToJson(geojson)
# %%
