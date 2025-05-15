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

id = ""
name_record = {}
# track
trackrec = [{"id":"", "title":""}]
# release
subrec = [{"id":"", "title":"", "country":"", "date":"", "label":"", "tracks":[]}]
# main record
rec = {"id":"", "name":"", "genre":"", "albums":[]}

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
    global rec
    global subrec
    global tracks

    rec = {"id":"", "name":"", "genre":"", "albums":[]}

    print("Entering get_metadata")
    results = search_artists(query=artist)['artist-list'][0]
    rec["id"] = results['id']
    rec["name"] = results['name']
    rec["genre"] = get_genre(results)

    # main record
    print(rec["id"], "/", rec["name"], "/", rec["genre"])

    releases = []
    print("Artist Info:")
    try:
        #releases = search_releases(query='artist=rec["name"]')
        releases = search_releases(query="discids", artist=rec["name"])
    except musicbrainz.InvalidFilterError as exc:
        print("Invalid Filter Error: ", exc.msg)
    except urllib.error.HTTPError as exc:
        print("HTTP Error: ", exc.reason)
    except musicbrainz.ResponseError as exc:
        if "Bad Request" not in str(exc.cause):
            print("Response Error: ", exc.cause)
    print("Releases: ",releases)

    for f in releases["release-list"]:
        # release
        subrec = [{"id":"", "title":"", "country":"", "date":"", "label":"", "tracks":[]}]
        subrec2 = {}
        for album in releases["release-list"]:

            print()
            subrec2 = {album["id"], album["title"]}
            if "release-event-list" in album and "label-info-list" in album:
                subrec2 = {"id":album["id"], "title":album["title"], "country":album["release-event-list"][0]["area"]["name"],
                        "date":album["release-event-list"][0]["date"],
                        "label":album["label-info-list"][0]["label"]["name"], "tracks":[]}
                print("Disc: ", album["title"], "/", album["release-event-list"][0]["date"], "/",
                      album["release-event-list"][0]["area"]["name"], "/", album["id"])
            else:
                subrec2 = {"id":album["id"], "title":album["title"], "date": "", "country": "", "tracks":[]}
                print("Disc: ", album["title"], "/", album["id"])

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
            print("Tracks:")

            tracks = []
            # track
            trackrec = [{"id":"", "title":""}]

            for recording in recordings["recording-list"]:
                #print("Track: ",recording["title"], "/", recording["id"])
                trackrec.append({"id": recording["id"], "title": recording["title"]})

            subrec2["tracks"].append(trackrec)

        subrec = subrec2

        rec["albums"].append(subrec)

    return rec

if __name__ == '__main__':
    ### get first release
    # if len(sys.argv) > 1:
    # artist, album = [sys.argv[1], sys.argv[2]]

    artist = "Louis Armstrong"
    results = search_artists(query=artist)['artist-list'][0]
    record_tmp = get_metadata(results["name"], results)

    json_obj = json.dumps(record_tmp)

    #results, genre = search_by_genre(genre, "Louis Armstrong", "release")
    print(json_obj)
    with open("ography.json", "w+") as json_file:
        json.dump(json_obj, json_file)