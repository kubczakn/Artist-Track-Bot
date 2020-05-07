import sys
import os
import spotipy
import spotipy.util as util

# Create a new playlist of songs from a specified artist, given another playlist

if len(sys.argv) > 1:
    username = sys.argv[1]
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


# Creates a dictionary of user playlists with a playlist/URI key/value combination
def create_playlist_dict(obj):
    playlists = obj.current_user_playlists(limit=50)
    playlist_dict = {}
    for i, item in enumerate(playlists['items']):
        playlist_dict[item['name']] = item['id']
    return playlist_dict


# Prompts user to choose a playlist
def choose_playlist(d, obj):
    print_playlists(d)
    choose_plst = input('Please choose a playlist to take artist tracks from: ')
    while choose_plst not in d:
        choose_plst = input('Playlist not found, please choose another: ')
    choose_plst_id = d[choose_plst]
    return obj.playlist_tracks(choose_plst_id, offset=0, fields='items.track.id,total')


def choose_playlist_to_modify(d):
    print_playlists(d)
    choose_plst = input('Please choose a playlist to modify: ')
    while choose_plst not in d:
        choose_plst = input('Playlist not found, please choose another: ')
    return choose_plst


# Prints all of user playlists
def print_playlists(d):
    for key in d.keys():
        print(key)


# Creates a list of dictionaries that have artist/URI key/value combinations
def create_artist_list(playlist, obj):
    artist_lst = []
    for num in range(0, len(playlist['items'])):
        artists = {}
        artist_id = playlist['items'][num]['track']['id']
        artist_name = obj.track(artist_id)['album']['artists'][0]['name']
        artists[artist_name] = artist_id
        artist_lst.append(artists)
    return artist_lst


# Prints out all of the unique artists in the playlist
def print_artists(artists):
    printed_artists = []
    for artist in artists:
        for key in artist.keys():
            if key not in printed_artists:
                print(key)
                printed_artists.append(key)
    return printed_artists


# Creates input for user to choose an artist
def choose_artist(lst):
    lst_artists = print_artists(lst)
    artist_chosen = input('Please choose an artist to take tracks from: ')
    while artist_chosen not in lst_artists:
        artist_chosen = input('Artist not found, please choose another: ')
    return artist_chosen


# Creates a new playlist for the user
def create_new_playlist(obj, plst_name):
    playlist_name = plst_name
    playlist_description = input('Please make a description for this playlist: ')
    return obj.user_playlist_create(username, playlist_name, description=playlist_description)


# Adds tracks from the chosen playlists that are by the chosen artist into the newly created playlist
def add_artist_songs(new_plst_uri, art_name, art_lst, obj):
    added_track_uris = []
    for artist in art_lst:
        for key in artist:
            if key == art_name:
                added_track_uris.append(artist[key])
    obj.user_playlist_add_tracks(username, new_plst_uri, added_track_uris)
    print('Tracks have been added, enjoy!')


def main():
    if token:
        loop = True
        while loop:
            sp = spotipy.Spotify(auth=token)
            sp.trace = False
            initial_input = input("Type 1 to create a new playlist, 2 to modify an existing playlist: ")
            while initial_input != '1' and initial_input != '2':
                initial_input = input('Invalid input, please try again: ')
            if initial_input == '1':
                plst_name = input("Please name this new playlist:  ")
                create_new_playlist(sp, plst_name)
                playlist_dict = create_playlist_dict(sp)
            else:
                playlist_dict = create_playlist_dict(sp)
                plst_name = choose_playlist_to_modify(playlist_dict)
            chosen_playlist = choose_playlist(playlist_dict, sp)
            artist_list = create_artist_list(chosen_playlist, sp)
            chosen_artist = choose_artist(artist_list)
            add_artist_songs(playlist_dict[plst_name], chosen_artist, artist_list, sp)
            end_input = input('Continue modifying? Please input Y/N: ')
            while end_input != 'Y' and end_input != 'N':
                end_input = input('Invalid input, please try again: ')
            if end_input == 'N':
                loop = False

    else:
        print("Can't get token for", username)


if __name__ == '__main__':
    main()

# Unused code that obtains data from a given artist
# print(sp.track(artist_dict[chosen_artist]))
# artist_data = sp.track(artist_dict[chosen_artist])
# chosen_artist_uri = 'spotify:artist:' + artist_data['album']['artists'][0]['id']
