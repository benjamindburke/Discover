import requests
from requests.exceptions import HTTPError
import subprocess
import time

class DiscoverApi:
    def __init__(self):
        """
        Create a new API instance via DiscoverApi().
        """
        self.token = self.requestAccessToken()
        self.header = { 'Authorization': 'Bearer {0}'.format(self.token), 'Content-Type': 'application/json' }

    def handleResponseCode(self, response):
        """
        Awaits Spotify's Status Code 429: Too Many Requests. Waits a length of time in seconds until requests can be made again.
        Raises exception with Spotify Status and JSON Body if not Status Code 200: OK
        @param response Spotify Reponse object
        """
        try:
            if (response.status_code == 429):         # Status Code 429 is Spotify's 'Too Many Requests' code
                timeDelay = response.headers['Retry-After']
                time.sleep(timeDelay)   # Wait until Spotify will take requests
                return 200              # Return OK
            
            response.raise_for_status() # Raise an error for specific HTTP codes that aren't 429
            return 200                  # Return 200 if exception not caught
        except HTTPError as http_error:
            raise Exception(f'HTTP error occured: {http_error}')
        
    def requestAccessToken(self):
        """
        Requests an access token from Spotify's services.
        """
        headers = { 'Authorization': 'Basic ZDczODYxOTZmODA3NDk4MjlmYzViMWFiNzVkNWUzZjU6MDIxZTEwNzM5OTdmNDg4MGE5Y2JiYzk3OWZlMmZkYTg=' }
        data = { 'grant_type': 'client_credentials' }
        response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
        status = self.handleResponseCode(response)

        token = response.json()['access_token']
        if (token):
            return token
        else:
            raise Exception('Token could not be requested from Spotify')

    def getTrackAttributes(self, songIds):
        """
        Requests the track attributes for a list of given songIds.  
        @param songIds a list of songIds to request track attributes for
        """
        results = requests.get('https://api.spotify.com/v1/audio-features/?ids={0}'.format(songIds[0]), headers=self.header)
        status = self.handleResponseCode(results) # handl;e response code, error if not success
        
        callCount = 0
        attributes = []
        songIdBatches = [songIds[x:x+100] for x in range(0, len(songIds), 100)] # splits songIds into lists of 100, spotify's max id query limit
        while (callCount < len(songIdBatches) and status == 200):
            nextUrl = 'https://api.spotify.com/v1/audio-features?ids={0}'.format(','.join(songIdBatches[callCount]))
            results = requests.get(nextUrl, headers=self.header)
            status = self.handleResponseCode(results)
            attributes.concat(results.json()['audio_features'])
            callCount += 1

        if (len(attributes) != len(songIds)): # make sure num. attribute items == num song items
            raise Exception('The number of received song attribute items does not match the number of requested song item attributes.')
        
        return attributes