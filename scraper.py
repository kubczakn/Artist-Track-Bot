import sys
import os
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


def create_playlist_dict(d):
    for key in d.keys():
        print(key)
    choose_playlist = input('Choose a playlist: ')
    choose_playlist_id = d[choose_playlist]
    return sp.playlist_tracks(choose_playlist_id, offset=0, fields='items.track.id,total')


def create_artist_dict(playlist):
    artists = {}
    for i in range(0, playlist['total']):
        artist_id = playlist['items'][i]['track']['id']
        artist_name = sp.track(artist_id)['album']['artists'][0]['name']
        artists[artist_name] = artist_id
    return artists


def print_artists(artists):
    for key in artists.keys():
        print(key)


if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False

    # Create a new playlist
    #    created_playlist = sp.user_playlist_create(username, playlist_name, description=playlist_description)
    playlists = sp.current_user_playlists(limit=50)
    print(type(playlists))
    # Create a dict of playlists names with their respective ids
    playlist_dict = {}
    for i, item in enumerate(playlists['items']):
        playlist_dict[item['name']] = item['id']

    # Print names of all playlist and have user choose a playlist
    chosen_playlist = create_playlist_dict(playlist_dict)

    # Go through chosen playlist and create a dict of track names with their respective ids
    artist_dict = create_artist_dict(chosen_playlist)

    # Print all artist names and have user choose an artist
    print_artists(artist_dict)
    chosen_artist = input('Choose an artist: ')
    print(chosen_artist)
else:
    print("Can't get token for", username)
