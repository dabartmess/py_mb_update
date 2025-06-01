#!/usr/bin/python3
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
from pathlib import Path
import urllib.error

import eyed3
import eyed3 as id3
import json

from eyed3 import AudioFile
from tinytag import TinyTag

import mb_search as mb
from musicbrainzngs import (search_releases, search_artists, browse_releases, browse_artists, browse_recordings,
                            set_useragent, get_recording_by_id, \
                            musicbrainz, ResponseError, InvalidFilterError)

filelist = []

set_useragent(
    "py_mb_update",
    "Dev-0.9",
    "https://github.com/dabartmess/py_mb_update/"
)


def modify_audio_file(artist: str, path: str):
    tmpnames = []
    filelist = []

    #print("PATH: ", path)
    for (root, _, files) in os.walk(path[0], oserror_o):
        if len(files) > 0:
            for file2 in files:
                if file2.lower().endswith(".mp3") or file2.lower().endswith('flac'):
                    file_in = os.path.join(root, file2)
                    # print("file_in: ", file_in)
                    filelist.append(file_in)

    # print(filelist)

    for f in filelist:
        print("File: ", f)
        a_tag = TinyTag.get(f)

        audio = AudioFile
        # print("Audio: ", f)
        try:
            if os.path.exists(f):
                audio = id3.core.load(f)
            else:
                print("Path does not exist: ", f)
        except IOError as exc:
            print("IOError: ", exc)

        result2 = {}
        files = []
        if (audio.tag):
            if (audio.tag.artist == None or audio.tag.album_artist == None):
                print("NO Album or Artist")
            else:
                print(audio.tag.artist)
                record_tmp = mb.get_metadata([audio.tag.artist], silent=False)
                print("Left get_metadata")
                if len(record_tmp) > 0:
                    print("ID: ",record_tmp["id"])
                    try:
                        result2 = get_recording_by_id(record_tmp["id"], includes=["artists", "releases"])
                    except InvalidFilterError as exc:
                        print("Invalid Filter Error: ", exc.msg)
                    except urllib.error.HTTPError as exc:
                        print("HTTP Error: ", exc.reason)
                    except musicbrainz.WebServiceError as exc:
                        print("WebServiceErrorL: ", exc)
                    except ResponseError as exc:
                        print("Response Error: ", exc)
                        if "Bad Request" not in str(exc.cause):
                            print("Response Error: ", exc.cause)
                            break
                    except Exception as exc:
                        print("Non-specific exception: ", exc)

                print("Result2: ", result2)
                files.append(result2)
        else:
            print("No Audio Tags")

    print("No of Filelist: ", len(filelist))
    print("No of Files: ", len(files))

    return files

def oserror_o(error: OSError):
    print(error.strerror)

if __name__ == '__main__':
    artist = "*"
    if len(sys.argv) > 1:
        artist = [sys.argv[1]]
        print(artist)

    if len(sys.argv) > 2:
        path = [sys.argv[2]]
        print(path)
    else:
        path = os.getcwd()
        print("CurrDir")

    modify_audio_file(artist, path);