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

    def storeTrackData(self, trackAttributes):
        """ Adds a new trackData object to the database.  

        @param trackAttributes a trackData object returned from Spotify
        """
        spotifyId = trackAttributes['id']
        key = trackAttributes['key']
        mode = trackAttributes['mode']
        timeSignature = trackAttributes['time_signature']
        acousticness = trackAttributes['acousticness']
        danceability = trackAttributes['danceability']
        energy = trackAttributes['energy']
        instrumentalness = trackAttributes['instrumentalness']
        liveness = trackAttributes['liveness']
        loudness = trackAttributes['loudness']
        speechiness = trackAttributes['speechiness']
        valence = trackAttributes['valence']
        tempo = trackAttributes['tempo']

        sql = "INSERT INTO trackData (spotifyId, key, mode, timeSignature, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, valence, tempo) VALUES " \
            + "('{0}', {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12})".format(spotifyId, key, mode, timeSignature, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, valence, tempo)
        
        conn = self._db.cursor()
        conn.execute(sql)
        self._db.commit()

    def storeLyricData(self, spotifyId, lyrics):
        """ Adds new lyricData objects to the database.  

        @param spotifyId the song id  
        @param lyrics a string of words representing the lyrics of a song  
        """
        sql = "INSERT INTO lyricData (spotifyId, word, position) VALUES "
        for i in range(len(lyrics)):
            sql += "('{0}', \"{1}\", {2})".format(spotifyId, lyrics[i], i)
            if (i != len(lyrics) - 1):
                sql += ","
        
        conn = self._db.cursor()
        conn.execute(sql)
        self._db.commit()

    def storeSongData(self, spotifyId, name, artist, lyricDataId, lyricSource):
        """ Adds new songData objects to the database.  

        @param spotifyId the spotify id of the song object
        @param name the name of the song  
        @param artist the name of the artist  
        @param lyricDataId the id of the lyricData linked to the song  
        @param lyricSource the source of the lyrics
        """
        sql = "INSERT INTO songData (spotifyId, name, artist, lyricDataId, lyricSource) VALUES ('{0}', '{1}', '{2}', {3}, '{4}')".format(spotifyId, name, artist, lyricDataId, lyricSource)
        
        conn = self._db.cursor()
        conn.execute(sql)
        self._db.commit()