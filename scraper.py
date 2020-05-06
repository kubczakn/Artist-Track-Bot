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


def create_artist_list(playlist):
    artist_lst = []
    for num in range(0, playlist['total']):
        artists = {}
        artist_id = playlist['items'][num]['track']['id']
        artist_name = sp.track(artist_id)['album']['artists'][0]['name']
        artists[artist_name] = artist_id
        artist_lst.append(artists)
    return artist_lst


def print_artists(artists):
    printed_artists = []
    for artist in artists:
        for key in artist.keys():
            if key not in printed_artists:
                print(key)
                printed_artists.append(key)


def create_new_playlist(obj, plst_name):
    playlist_name = plst_name
    playlist_description = 'Test Playlist Creation'
    return obj.user_playlist_create(username, playlist_name, description=playlist_description)


def add_artist_songs(new_plst_uri, art_name, art_lst, obj):
    added_track_uris = []
    for artist in art_lst:
        for key in artist:
            if key == art_name:
                added_track_uris.append(artist[key])
    obj.user_playlist_add_tracks(username, new_plst_uri, added_track_uris)


if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    # Create new playlist
    new_plst_name = 'New Playlist'
    created_playlist = create_new_playlist(sp, new_plst_name)
    # Create a dict of playlists names with their respective ids
    playlists = sp.current_user_playlists(limit=50)
    playlist_dict = {}
    for i, item in enumerate(playlists['items']):
        playlist_dict[item['name']] = item['id']

    # Print names of all playlist and have user choose a playlist
    chosen_playlist = create_playlist_dict(playlist_dict)
    # Go through chosen playlist and create a dict of track names with their respective ids
    artist_list = create_artist_list(chosen_playlist)
    print(artist_list)
    # Print all artist names and have user choose an artist
    print_artists(artist_list)
    chosen_artist = input('Choose an artist: ')

    # Create new playlist and add artist tracks from old playlist to new playlist
    add_artist_songs(playlist_dict[new_plst_name], chosen_artist, artist_list, sp)


else:
    print("Can't get token for", username)

# print(sp.track(artist_dict[chosen_artist]))
# artist_data = sp.track(artist_dict[chosen_artist])
# chosen_artist_uri = 'spotify:artist:' + artist_data['album']['artists'][0]['id']
