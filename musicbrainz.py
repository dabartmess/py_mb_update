#!/usr/bin/python3
from __future__ import print_function
from __future__ import unicode_literals
import musicbrainzngs
import sys


musicbrainzngs.set_useragent(
    "py_mb_update",
    "Dev-0.9",
    "https://github.com/dabartmess/py_mb_update/"
)


def get_tracklist(artist, album):
    result = musicbrainzngs.search_releases(artist=artist, release=album,
                                            limit=1)
    id = result["release-list"][0]["id"]

    #### get tracklist
    new_result = musicbrainzngs.get_release_by_id(id, includes=["recordings"])
    t = (new_result["release"]["medium-list"][0]["track-list"])
    for x in range(len(t)):
        line = (t[x])
        print(f'{line["number"]}. {line["recording"]["title"]}')
        print({line["recording"]["genre"]})


if __name__ == '__main__':
    ### get first release
    #if len(sys.argv) > 1:
        #artist, album = [sys.argv[1], sys.argv[2]]
        artist, album = ["Pink Floyd", "Dark Side of the Moon"]
        get_tracklist(artist, album)
    #else:
    #    artist = input("Artist: ")
    #    album = input("Album: ")
    #    if not artist == "" and not album == "":
    #        get_tracklist(artist, album)
    #    else:
    #        print("Artist or Album missing")