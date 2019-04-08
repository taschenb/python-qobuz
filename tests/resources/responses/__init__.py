import json

with open("tests/resources/responses/album_get.json") as json_data:
    album_get_json = json.load(json_data)

with open("tests/resources/responses/album_search.json") as json_data:
    album_search_json = json.load(json_data)

with open("tests/resources/responses/artist_get_albums.json") as json_data:
    artist_get_albums_json = json.load(json_data)

with open("tests/resources/responses/artist_search.json") as json_data:
    artist_search_json = json.load(json_data)
