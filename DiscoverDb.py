import sqlite3

FILEPATH = './Discover.db'

class DiscoverDb:
    def __init__(self):
        """
        Create a new database instance via DiscoverDb(access_token, username)  
        @param token user's authentication token  
        @param username user's username  
        @param weekId the id of the week during which results are collected
        """
        self._db = sqlite3.connect(FILEPATH)
    
    def shutdown(self):
        """
        Save all edits to the database and close the database connection.
        """
        self._db.commit()
        self._db.close()
        self._db = None

    def addSongsToDatabase(self, songs):
        """
        Adds new songs to the database and creates a relationship between the user and the songs in their library.  
        @param songs a list of songs returned from spotify
        """
        sql = "INSERT INTO songs (songId, key, mode, timeSignature, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, valence, tempo) VALUES "
        for song in songs:
            sql += "('{id}', {key}, {mode}, {timeSignature}, {acousticness}, {danceability}, {energy}, {instrumentalness}, {liveness}, {loudness}, {speechiness}, {valence}, {tempo})".format_map(song)
            if (songs.index(song) != len(songs) - 1):
                sql += ","
        
        conn = self._db.cursor()
        conn.execute(sql)
        self._db.commit()