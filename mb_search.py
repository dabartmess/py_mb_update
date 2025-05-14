#!/usr/bin/python3
from __future__ import print_function
from __future__ import unicode_literals

import json
import sys
import urllib.error
from dataclasses import fields

from musicbrainzngs import search_releases, search_artists, browse_releases, browse_recordings, set_useragent, \
    musicbrainz, ResponseError
from requests import HTTPError

# track
trackrec = [{"id": "", "title": ""}]
# release
subrec = [{"id":"", "title":"", "country": "", "date": "", "tracks":[]}]
# main record
rec = {"id": "", "name": "", "genre": "", "albums": []}

id = ""
name_record = {}

set_useragent(
    "py_mb_update",
    "Dev-0.9",
    "https://github.com/dabartmess/py_mb_update/"
)

def get_genre(resultfac: {}):
    tmp_dict = {}

    #print("resultfac: ",resultfac)
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

    #print("Genre: ", tmp_dict)
    return tmp_dict

def get_metadata(artist, results: {}):
    global subrec
    print("Entering get_metadata")
    results = search_artists(query=artist)['artist-list'][0]
    rec["id"] = results['id']
    rec["name"] = results['name']
    rec["genre"] = get_genre(results)

    print("Artist Info:")
    print(rec["id"], "/", rec["name"], "/", rec["genre"])

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
    print(releases)

    subrec2 = {}
    for album in releases["release-list"]:
        subrec2 = {album["id"], album["title"]}
        if "release-event-list" in album:
            subrec2 = {"id":album["id"], "title":album["title"], "date":album["release-event-list"][0]["date"],
                       "country": album["release-event-list"][0]["area"]["name"], "tracks":[]}
        else:
            subrec2 = {"id":album["id"], "title":album["title"], "date": "", "country": "", "tracks":[]}

        recordings = {}
        try:
    #        print(releases["release-list"][0]["title"])
            recordings = browse_recordings(release=releases["release-list"][0]["id"])
        except musicbrainz.InvalidFilterError as exc:
            print("Invalid Filter Error: ", exc.msg)
        except urllib.error.HTTPError as exc:
            print("HTTP Error: ", exc.reason)
        except musicbrainz.ResponseError as exc:
            if "Bad Request" not in str(exc.cause):
                print("Response Error: ", exc.cause)
        print("Got Recordings", recordings)
        print("Disc Info:")
        print("Tracks:")

        tracks = []
        for recording in recordings["recording-list"]:
            print("Recording: ",recording)
            trackrec.append({"id": recording["id"], "title": recording["title"]})

        subrec2["tracks"].append(trackrec)

    subrec = subrec2

    rec["albums"].append(subrec)

    return rec

def search_by_artist(artist, entity_type='artist'):
    print("Entering search_by_artist")
    set_useragent(
        "py_mb_update",
        "Dev-0.9",
        "https://github.com/dabartmess/py_mb_update/"
    )
    artist_list = search_artists(query=artist)['artist-list'][0]
#    structure = artist_list[0]
#    genre = get_genre(artist_list)
    return artist_list


def search_by_genre(genre, artist, entity_type='artist'):
    print("Entering search_by_genre")
    genre = None
    if entity_type == 'artist':
        result = search_artists(query={artist})['artist-list'][0]
        print("release-list: ", result['release-list'])
        #genre = get_genre(result)
    elif entity_type == 'release':
        result = search_releases(query="{release}")
        #print("result: ", result)
        print("release-list: ", result)
        #genre = get_genre(rec["name"])
    else:
        raise ValueError("Invalid entity type. Choose 'artist' or 'release'.")
    return result

if __name__ == '__main__':
    ### get first release
    # if len(sys.argv) > 1:
    # artist, album = [sys.argv[1], sys.argv[2]]

    results = search_by_artist("Louis Armstrong", 'artist')
    set_useragent(
        "py_mb_update",
        "Dev-0.9",
        "https://github.com/dabartmess/py_mb_update/"
    )
    record_tmp = get_metadata(results["name"], results)

    json_obj = json.dumps(record_tmp, indent=3)

    #results, genre = search_by_genre(genre, "Louis Armstrong", "release")
    print(json_obj)