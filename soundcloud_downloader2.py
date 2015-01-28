import urllib2
import sys

bs4 = True
try:
    from bs4 import BeautifulSoup
except ImportError:
    import BeautifulSoup
    bs4 = False

MAIN_URL='https://api.soundcloud.com/tracks/'
TRACK_ID=''
STREAM='/stream?client_id='
CLIENT_ID='6862b458caa60ca20447985771260f7b'

def get_beautiful_soup(html):
    if bs4:
        return BeautifulSoup(html)
    else:
        return BeautifulSoup.BeautifulSoup(html)

def print_usage():
  print "python soundcloud_downloader2.py [url1] [url2] [url3] [...]"
  sys.exit(0)

def parse(string_parse):
    tmp_id=''
    p=0
    while string_parse[p] != '"':
        tmp_id+=string_parse[p]
        p+=1
    return tmp_id

def get_track_id(track_url):
    file_name=track_url.split('/')[-1]+'.mp3'
    track_url=track_url.split('soundcloud.com')[-1]
    track_url='https://soundcloud.com'+track_url
    print track_url
    track_id=''
    tempstr=str(urllib2.urlopen(track_url).read())
    track_id=parse(tempstr.split('sounds:')[-1])
    return (file_name, track_id)
    
def show_details(name, url):
    info=dict(urllib2.urlopen(url).info())
    if 'Content-Length' in info:
        size=int(info['Content-Length'])
    else:
        size=int(info['content-length'])
    Mem=['B', 'KB', 'MB', 'GB', 'TB']
    p=0
    while (size/1024)>1:
        size/=1024
        p+=1
    print '\nFile-Name: %s' %name
    print 'File-Size: %s %s' %(size, Mem[p]); print '\n'
    
def download_track(url, location):
    print '\nDownloading Track. . .'
    f=open(location, 'wb')
    q=urllib2.urlopen(url)
    buff_size=8192
    while True:
        buff=q.read(buff_size)
        if not buff:
            break
        f.write(buff)
    f.close()
    print 'Track Downloaded\n'
    
def is_playlist(uri):
    parts = uri.split('/')
    unusable = ['http:', 'https:', '', 'soundcloud.com']
    actual_parts = []
    for part in parts:
        if part not in unusable:
            actual_parts.append(part)

    if len(actual_parts) == 1:
        return True
    else:
        return False

def parse_playlist(url):
    playlist = []
    soup = get_beautiful_soup( urllib2.urlopen(url).read() )
    soup = soup.find_all('article')
    soup = soup[1:]
    for track in soup:
        url = 'http://soundcloud.com' + track.h1.a['href']
        playlist.append(url)

    return playlist

if __name__=='__main__':
    if len(sys.argv) == 1:
        print_usage()

    for track_url in sys.argv[1 : ]:

        url_to_download = []

        if is_playlist(track_url):
            url_to_download += parse_playlist(track_url)
        else:
            url_to_download.append(track_url)

        for track in url_to_download:
            (file_name, TRACK_ID) = get_track_id(track)
            download_url=MAIN_URL+TRACK_ID+STREAM+CLIENT_ID
            show_details(file_name, download_url)
            location=raw_input('Save to location(eg. ~/downloads): ')
            download_track(download_url, location+'/'+file_name)    


