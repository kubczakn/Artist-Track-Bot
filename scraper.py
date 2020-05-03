import sys
import os
import spotipy
import spotipy.util as util

# Adds tracks to a playlist

if len(sys.argv) < 3:
    username = sys.argv[1]
    playlist_id = sys.argv[2]
    track_ids = sys.argv[3]
else:
    print("Usage: %s username playlist_id track_id ..." % (sys.argv[0],))
    sys.exit()


scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username,
                                   scope,
                                   client_id=os.environ.get('SPOTIPY_CLIENT_ID'),
                                   client_secret=os.environ.get('SPOTIPY_CLIENT_SECRET'),
                                   redirect_uri=os.environ.get('SPOTIPY_REDIRECT_URL'))

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    results = sp.user_playlist_add_tracks(username, playlist_id, track_ids)
    print(results)
else:
    print("Can't get token for", username)
