#!/usr/bin/python3
from __future__ import print_function
from __future__ import unicode_literals

import urllib.error
from dataclasses import fields

from musicbrainzngs import search_releases, search_artists, browse_releases, browse_recordings, set_useragent, \
    musicbrainz, ResponseError
from requests import HTTPError

rec = {"id": None,
          "name": None,
          "genre": None,
          "albums": dict(id="", album="", tracks=[]),
          "country": None,
          }

id = ""

set_useragent(
    "py_mb_update",
    "Dev-0.9",
    "https://github.com/dabartmess/py_mb_update/"
)

def get_genre(resultfac: {}):
    tmp_dict = {}

    #print(resultfac)
    name = resultfac["name"]
    if resultfac:
        if resultfac['name'].lower() == name.lower():
            tmp = 0
            for n in resultfac['tag-list']:
                if int(n['count']) > tmp:
                    tmp = int(n['count'])
                    tmp_dict = n['name']
        else:
            print("NO RESULTFAC", resultfac)
    return tmp_dict

def get_metadata(artist, results: {}):
    print("Entering get_metadata")
    results = search_artists(query=artist)['artist-list'][0]
    rec["id"] = results['id']
    rec["name"] = results['name']
    rec["genre"] = get_genre(results)
    releases = []
    try:
        releases = search_releases(query="discids", artist=rec["name"])
    except musicbrainz.InvalidFilterError as exc:
        print("Invalid Filter Error: ", exc.msg)
    except urllib.error.HTTPError as exc:
        print("HTTP Error: ", exc.reason)
    except musicbrainz.ResponseError as exc:
        if "Bad Request" not in str(exc.cause):
            print("Response Error: ", exc.cause)
    recordings = {}
    try:
        recordings = browse_recordings(artist)
    except musicbrainz.InvalidFilterError as exc:
        print("Invalid Filter Error: ", exc.msg)
    except urllib.error.HTTPError as exc:
        print("HTTP Error: ", exc.reason)
    except musicbrainz.ResponseError as exc:
        if "Bad Request" not in str(exc.cause):
            print("Response Error: ", exc.cause)
    print("Got Recordings", recordings)
    print("Disc Info:")
    for discname in releases["release-list"]:
        #print(discname)
        discid = discname["id"]
        print(discid, "/", discname['title'], "/", rec["name"])
        genrename = get_genre(results)
        try:
            result = musicbrainz.get_releases_by_discid(discid, includes=["discids","artists","recordings"],
            media_format ="all")
        except urllib.error.HTTPError as exc:
            print("HTTPError: ", exc.reason)
        except musicbrainz.ResponseError as exc:
            if "Bad Request" not in str(exc.cause):
                print("Response Error: ", exc.cause)


def search_by_artist(artist, entity_type='artist'):
    print("Entering search_by_artist")
    set_useragent(
        "py_mb_update",
        "Dev-0.9",
        "https://github.com/dabartmess/py_mb_update/"
    )
    artist_list = search_artists(query=artist)['artist-list']
    structure = artist_list[0]
    genre = get_genre(structure)
    return structure, genre


def search_by_genre(genre, artist, entity_type='artist'):
    print("Entering search_by_genre")
    genre = None
    if entity_type == 'artist':
        result = search_artists(query={artist})['artist-list'][0]
        print(result)
        genre = get_genre(result['name'])
    elif entity_type == 'release':
        result = search_releases(query="{artist}")['release-list'][0]
        print("result: ", result[0])
        genre = get_genre(result[0])
    else:
        raise ValueError("Invalid entity type. Choose 'artist' or 'release'.")
    print("release-list: ", result['release-list'])
    return result, genre


if __name__ == '__main__':
    ### get first release
    # if len(sys.argv) > 1:
    # artist, album = [sys.argv[1], sys.argv[2]]

    results,genre = search_by_artist("Louis Armstrong", 'artist')
    set_useragent(
        "py_mb_update",
        "Dev-0.9",
        "https://github.com/dabartmess/py_mb_update/"
    )
    get_metadata(results["name"], results)
    results, genre = search_by_genre(genre, "Louis Armstrong", "artist")
    print(results)