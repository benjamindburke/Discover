import sqlite3

FILEPATH = './Discover.db'

class DiscoverDb:
    def __init__(self):
        """ Create a new database instance via DiscoverDb()  
        """
        self._db = sqlite3.connect(FILEPATH)
    
    def shutdown(self):
        """ Save all edits to the database and close the database connection.
        """
        self._db.commit()
        self._db.close()
        self._db = None

    def storeTrackData(self, songs):
        """ Adds new trackData objects to the database.  

        @param songs a list of trackData objects returned from Spotify
        """
        sql = "INSERT INTO tracKData (songId, key, mode, timeSignature, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, valence, tempo) VALUES "
        for song in songs:
            sql += "('{id}', {key}, {mode}, {timeSignature}, {acousticness}, {danceability}, {energy}, {instrumentalness}, {liveness}, {loudness}, {speechiness}, {valence}, {tempo})".format_map(song)
            if (songs.index(song) != len(songs) - 1):
                sql += ","
        
        conn = self._db.cursor()
        conn.execute(sql)
        self._db.commit()

    def storeLyricData(self, artist, name, lyrics, source):
        """ Adds new lyricData objects to the database.  

        @param artist the name of the artist  
        @param name the name of the song  
        @param lyrics a string of words representing the lyrics of a song  
        @param source where the lyrics were sourced from
        """
        sql = "INSERT INTO lyricData (artist, name, lyrics, source) VALUES ('{0}', '{1}', \"{2}\", '{3}')".format(artist, name, lyrics, source)
        conn = self._db.cursor()
        conn.execute(sql)
        self._db.commit()

    def storeSongData(self, trackDataId, lyricDataId, artist, name):
        """ Adds new songData objects to the database.  

        @param trackDataId the id of the trackData linked to the song   
        @param lyricDataId the id of the lyricData linked to the song  
        @param artist the name of the artist  
        @param name the name of the song
        """
        sql = "INSERT INTO songData (trackDataId, lyricDataId, artist, name) VALUES ('{0}', '{1}', \"{2}\", '{3}')".format(trackDataId, lyricDataId, artist, name)
        conn = self._db.cursor()
        conn.execute(sql)
        self._db.commit()