import json

with open("tests/resources/responses/album_get.json") as json_data:
    album_get_json = json.load(json_data)

with open("tests/resources/responses/album_search.json") as json_data:
    album_search_json = json.load(json_data)

with open("tests/resources/responses/album_featured.json") as json_data:
    album_featured_json = json.load(json_data)

with open("tests/resources/responses/artist_get_albums.json") as json_data:
    artist_get_albums_json = json.load(json_data)

with open("tests/resources/responses/artist_search.json") as json_data:
    artist_search_json = json.load(json_data)

with open("tests/resources/responses/user_login.json") as json_data:
    user_login_json = json.load(json_data)

with open("tests/resources/responses/user_playlist_create.json") as json_data:
    playlist_create_json = json.load(json_data)

with open("tests/resources/responses/user_fav_get_albums.json") as json_data:
    user_fav_get_albums_json = json.load(json_data)

with open("tests/resources/responses/track_search.json") as json_data:
    track_search_json = json.load(json_data)

with open("tests/resources/responses/playlist_get_tracks.json") as json_data:
    playlist_get_tracks_json = json.load(json_data)

with open("tests/resources/responses/playlist_add_tracks.json") as json_data:
    playlist_add_tracks_json = json.load(json_data)

with open("tests/resources/responses/playlist_search.json") as json_data:
    playlist_search_json = json.load(json_data)

with open("tests/resources/responses/get_file_url.json") as json_data:
    get_file_url_json = json.load(json_data)

with open("tests/resources/responses/playlist_get_user_playlists.json") as json_data:
    playlist_get_user_playlists_json = json.load(json_data)
