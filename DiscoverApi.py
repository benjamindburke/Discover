import json
import requests
from requests.exceptions import HTTPError
import subprocess
import time

def handleResponseCode(response):
    """ Awaits Spotify's Status Code 429: Too Many Requests. Waits a length of time in seconds until requests can be made again.  

    Raises exception with Spotify Status and JSON Body if not Status Code 200: OK  
    @param response Spotify Reponse object
    """
    try:
        if (response.status_code == 429):               # Status Code 429 is Spotify's 'Too Many Requests' code
            timeDelay = response.headers['Retry-After']
            time.sleep(timeDelay)                       # Wait until Spotify will take requests  
        return 200                                      # Return OK
        
        response.raise_for_status()                     # Raise an error for specific HTTP codes that aren't 429
        return 200                                      # Return 200 if exception not caught
    except HTTPError as http_error:
        raise Exception(f'HTTP error occured: {http_error}')
        
def requestAccessToken():
    """ Requests an access token from Spotify's services. 

    @returns (Spotify authentication token, Spotify authentication headers) dictionary. Send the headers with every API request.
    """
    headers = { 'Authorization': 'Basic ZDczODYxOTZmODA3NDk4MjlmYzViMWFiNzVkNWUzZjU6MDIxZTEwNzM5OTdmNDg4MGE5Y2JiYzk3OWZlMmZkYTg=' }
    data = { 'grant_type': 'client_credentials' }
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    status = handleResponseCode(response)

    token = response.json()['access_token']
    if (token):
        return (token, { 'Authorization': 'Bearer {0}'.format(token), 'Content-Type': 'application/json' })
    else:
        raise Exception('Token could not be requested from Spotify')

def getTrackAttributes(headers, spotifyId):
    """ Requests the track attributes for a given spotifyId  

    @param headers the Spotify authorization header and other header options  
    @param spotifyId a songId to request track attributes for  
    @returns a list of track attributes
    """
    results = requests.get('https://api.spotify.com/v1/audio-features/{0}'.format(spotifyId), headers=headers)
    status = handleResponseCode(results) # handle response code, error if not success
    
    return results.json()

def getRecommendationsFromSpotify(headers, **kwargs):
    """ Returns a Spotify-generated list of recommendations based on seed trackIds.  

    @param headers the Spotify authorization header and other header options  
    @kwargs seed_tracks a list of seed trackIds  
    @kwargs target_* search for songs around specified values of attributes  
        e.x. target_instrumentalness=0.35
    @kwargs min_* search for songs with min values of specified attributes  
        e.x. min_tempo=110
    @kwargs max_* search for songs with max values of specified attributes  
        e.x. max_tempo=160
    @returns a list of Spotify trackIds
    """
    queryString = ''
    if kwargs['seed_tracks']: # extract the array from kwargs to a valid query string
        queryString += '&seed_tracks=' + ','.join(song for song in kwargs['seed_tracks']) # join strings with ,

    for key, value in kwargs.items():
        if (key != 'seed_tracks'):
            queryString += '&{0}={1}'.format(key, value)

    queryString = '?' + queryString[1:] # replace leading & char from request with ?
    results = requests.get('https://api.spotify.com/v1/recommendations{0}'.format(queryString), headers=headers)
    status = handleResponseCode(results) # handle response code, error if not success

    trackIds = [track['id'] for track in results.json()['tracks']]
    return trackIds


def searchSpotifyForSongId(headers, *searchWords):
    """ Return the top Spotify search result for a search query.  

    @param searchWords a list of query words
    @returns spotifyId the spotifyId of the track
    """
    queryString = "?q=" + '+'.join(word for word in searchWords) + '&type=track'
    
    results = requests.get('https://api.spotify.com/v1/search{0}'.format(queryString), headers=headers)
    status = handleResponseCode(results) # handle response code, error if not success

    callCount = 0
    if (len(results.json()['tracks']['items']) > 0):
        spotifyId = results.json()['tracks']['items'][0]['id']
        return spotifyId
    else:
        while (callCount < 4 and status == 200):
            callCount += 1
            results = requests.get('https://api.spotify.com/v1/search{0}'.format(queryString), headers=headers)
            status = handleResponseCode(results) # handle response code, error if not success
            if (len(results.json()['tracks']['items']) > 0):
                spotifyId = results.json()['tracks']['items'][0]['id']
                return spotifyId

    return None