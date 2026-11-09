# Generous boxes around known Cenozoic volcanic fields that sit inside the scanned deserts (lat0,lat1,lon0,lon1)
V = {
 "Harrat Ash Shaam": (31, 33.8, 35.8, 39.8), "Harrat Uwayrid": (26.3, 27.6, 37.2, 38.6), "Harrat Lunayyir": (24.9, 25.7, 37.3, 38.1),
 "Harrat Khaybar/Ithnayn": (24.4, 27.6, 39.2, 41.2), "Harrat Rahat": (21.4, 24.5, 39.2, 40.7), "Harrat Kishb/Hadan/Buqum": (21.0, 23.7, 40.9, 42.7),
 "Harrat Hutaymah": (26.6, 27.4, 41.9, 42.7), "Harrat al Birk": (17.4, 19.2, 41.2, 42.4), "Yemen volcanics": (12.5, 16.5, 43.0, 46.5),
 "Haruj": (25.3, 28.6, 15.8, 19.2), "Jabal as Sawda": (28.0, 29.6, 14.0, 16.6), "Gharyan": (31.4, 32.6, 12.4, 14.2),
 "Tibesti": (18.8, 22.6, 15.8, 20.2), "Eghei": (22.3, 24.2, 18.4, 20.3), "Hoggar/Atakor": (21.5, 24.6, 4.4, 7.2),
 "Air": (16.8, 20.2, 7.4, 10.2), "Jebel Marra": (12.4, 14.2, 23.4, 25.2), "Meidob": (14.7, 16.1, 25.7, 27.1),
 "Bayuda": (17.2, 19.0, 31.9, 33.9), "Pinacate": (31.4, 32.3, -114.0, -113.1), "Tres Virgenes/Gulf islands": (26.8, 28.0, -112.8, -111.5),
 "Central Andes arc": (-28.5, -16.0, -70.0, -65.5), "Gobi Dariganga": (44.5, 46.5, 112.5, 115.0),
 "Patagonia plateau basalts": (-50, -38, -72, -66.5), "Kenya/Eth rift": (-1, 14, 35, 43),
 "SE Australia Newer Volcanics": (-38.5, -36.5, 141.5, 144.5), "Durango/Chih maar fields": (24.5, 26.5, -105.5, -103.5),
 "SW USA fields": (32, 37.5, -114.5, -106.5), "Sinai/Arabia Hejaz minor": (28, 30, 34.5, 36),
}
def volc(lat, lon):
    for n, (a, b, c, d) in V.items():
        if a <= lat <= b and c <= lon <= d:
            return n
    return ""
