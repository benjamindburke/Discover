import glob
import os
import re
from multiprocessing import Process
from DiscoverDb import DiscoverDb
path = 'c:\\bin\\Discover\\lyrics-master\\database\\'

files = [f for f in glob.glob(path + "**/*", recursive=True)]
wordRgx = r"([A-Za-z0-9']+(\b[\,\.?!])?)"
infoRgx = r"_{2,}"

def processFile(filepath):
    db = DiscoverDb()
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
        db.storeLyricData(song['artist'], song['name'], ' '.join(song['lyrics']), 'lyrics-master')
        # db.storetrackData( #, #, song['artist'], song['name'])
    db.shutdown()

if __name__ == '__main__':
    for file in files:
        if not os.path.isdir(file):
            p = Process(target=processFile, args=(file,))
            p.start()
            p.join()

