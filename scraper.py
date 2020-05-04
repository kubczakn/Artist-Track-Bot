import sys
import os
import json
import spotipy
import spotipy.util as util

# Create a new playlist of songs from a specified artist, given another playlist

if len(sys.argv) > 3:
    username = sys.argv[1]
    user = sys.argv[2]
    playlist_id = sys.argv[3]
    track_ids = sys.argv[4:]
else:
    print("Usage: %s username playlist_id track_id ..." % (sys.argv[0],))
    sys.exit()

scope_private = 'playlist-modify-private'
scope_public = 'playlist-modify-public'

playlist_name = 'New Playlist'
playlist_description = 'Test Playlist Creation'

token = util.prompt_for_user_token(username=username,
                                   scope=scope_public,
                                   client_id=os.environ.get('SPOTIPY_CLIENT_ID'),
                                   client_secret=os.environ.get('SPOTIPY_CLIENT_SECRET'),
                                   redirect_uri=os.environ.get('SPOTIPY_REDIRECT_URL'))


# functions stubs
def add_songs_to_playlist():
    print('')


def search_playlist_for_track():
    print('')


if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    #    created_playlist = sp.user_playlist_create(username, playlist_name, description=playlist_description)
    playlists = sp.current_user_playlists(limit=50)
    playlist_dict = {}
    for i, item in enumerate(playlists['items']):
        playlist_dict[item['name']] = item['id']
    playlist_tracks = []
    first_playlist = list(playlist_dict.keys())[0]
    print(first_playlist)
    first_playlist_tracks = sp.playlist_tracks(playlist_dict[first_playlist], offset=0, fields='items.track.id,total')
    print(first_playlist_tracks)
    # work on show_tracks.py, which will show artist and track name, given a list of track IDs

#    for track in first_playlist_tracks:

else:
    print("Can't get token for", username)
