import DiscoverApi

# token  : spotify authentication token
# headers: spotify authentication header. send it with every response
(token, headers) = DiscoverApi.requestAccessToken()

seed_tracks = [
    '1u1YU1LE0FWHFOHpR2iXua',   # Sufjan Stevens - Casimir Pulaski Day
    '28cnXtME493VX9NOw9cIUh',   # Johnny Cash - Hurt
    '4kflIGfjdZJW4ot2ioixTB',   # Adele - Someone Like You
    '0Fao855T3klV3REFRFHRF3',   # David Bowie - Blackstar
    '3JOVTQ5h8HGFnDdp4VT3MP',   # Gary Jules - Mad World
]


DiscoverApi.getRecommendationsFromSpotify(headers, seed_tracks=seed_tracks)