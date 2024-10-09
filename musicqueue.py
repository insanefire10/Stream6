import youtubeconv

class musicqueue:
    def __init__(self, url):
        song_url = url
        song_id = youtubeconv.convertURLtoID(url)
        song_thumbail = youtubeconv.getThumbail(url)

def queuePlayer(queueArray):
    while(len(queueArray) > 0):
        