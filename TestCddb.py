#!/usr/bin/python3

import Cddb, os, sys

multiple = "E512640F 15 150 23780 56867 73962 96577 124515 141320 156755 178960 204585 236400 259287 289755 315007 338777 4710"
exact1 = "610ADF09 9 150 25620 49322 78800 100775 125492 154060 174270 189407 2785"
exact2 = "760D8B0A 10 150 32087 55987 85822 113087 142505 159912 183780 204622 228625 3469"
longtitle = "A507FD0E 14 150 13694 20250 31112 44578 54994 66087 75909 88501 98088 108243 116112 132029 143056 2047"
longtrack = "FD096E14 20 150 7337 18658 27494 37765 46752 56217 66153 78005 83493 92709 102300 110874 120177 130618 145099 152388 155617 164602 169465 2416"
nomatch = "82096E09 9 150 5845 18944 49318 73204 92959 112434 134294 154710 2416"

cddb = Cddb.CddbServer()

#discs = cddb.getDiscs(multiple)
#discs = cddb.getDiscs(exact1)
discs = cddb.getDiscs(exact2)
#discs = cddb.getDiscs(longtitle)
#discs = cddb.getDiscs(longtrack)
#discs = cddb.getDiscs(nomatch)
#discs = cddb.getDiscs() # requires a cd to be loaded in the drive

discentries = []
artistentries = []
albumentries = []

if discs:

	for disc in discs:
		di = cddb.getDiscInfo(disc)

		if di:
			if di.discid not in discentries and di.artist[0] not in artistentries and di.album not in albumentries:
				print("ID: ", di.discid)
				discentries.append(di.discid)
				artistentries.append(di.artist[0])
				albumentries.append(di.album)
			else:
				continue

			(40 * '-')
			print("Artist: %s" % di.artist[0])
			print("Album: %s" % di.album)
			i = 1
			print("Tracks:")
			for t in di.tracks:
				print("%02d: %s" % (i, t) )
				i = i + 1

			print(40 * '-')