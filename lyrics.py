import glob
import os
import re
from multiprocessing import Process
import DiscoverApi
from DiscoverDb import DiscoverDb

dbPath = 'c:\\bin\\Discover\\database\\'
files = [f for f in glob.glob(dbPath + "**/*", recursive=True)]
wordRgx = r"([A-Za-z0-9']+(\b[\,\.?!])?)"
infoRgx = r"_{2,}"

def processFile(filepath, lyricObjIndex):
    db = DiscoverDb()
    (_, headers) = DiscoverApi.requestAccessToken()
    with open(filepath, 'r') as f:
        song = { 'artist': '', 'name': '', 'lyrics': [] }
        for line in f:
            if re.match(infoRgx, line): # finished processing lyrics, now process song metadata
                _, name = [word.strip() for word in f.readline().split('  ')]
                _, artist = [word.strip() for word in f.readline().split('  ')]
                while (_ != "Artist"):
                    _, artist = [word.strip() for word in f.readline().split('  ')]
                song['name'] = name
                song['artist'] = artist
                break
            else:
                for word in re.findall(wordRgx, line):
                    song['lyrics'].append(word[0])
        f.close()
        name = song['name']
        artist = song['artist']
        lyrics = song['lyrics']
        spotifyId = DiscoverApi.searchSpotifyForSongId(headers, name, artist)
        if (spotifyId is not None):
            trackAttributes = DiscoverApi.getTrackAttributes(headers, spotifyId)
            db.storeLyricData(spotifyId, lyrics)
            db.storeSongData(spotifyId, name, artist, lyricObjIndex, 'lyrics-master')
            db.storeTrackData(trackAttributes)
            print(name, 'by', artist, 'stored')
        else:
            print(name, 'by', artist, 'could not be found on spotify.')
    db.shutdown()

if __name__ == '__main__':
    lyricObjIndex = 0
    for file in files:
        if not os.path.isdir(file):
            lyricObjIndex += 1
            p = Process(target=processFile, args=(file, lyricObjIndex))
            p.start()
            p.join()