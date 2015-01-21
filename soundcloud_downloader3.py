import urllib.request
import sys

MAIN_URL='https://api.soundcloud.com/tracks/'
TRACK_ID=''
STREAM='/stream?client_id='
CLIENT_ID='6862b458caa60ca20447985771260f7b'

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
    track_id=''
    tempstr=str(urllib.request.urlopen(track_url).read())
    track_id=parse(tempstr.split('sounds:')[-1])
    return (file_name, track_id)
    
def show_details(name, url):
    info=dict(urllib.request.urlopen(url).info())
    size=int(info['Content-Length'])
    Mem=['B', 'KB', 'MB', 'GB', 'TB']
    p=0
    while (size/1024)>1:
        size/=1024
        p+=1
    print('\nFile-Name:', end=' '); print(name);
    print('File-Size:', end=' '); print(size, end=' '); print(Mem[p]); print(end='\n')
    
def download_track(url, location):
    print('\nDownloading Track. . .')
    f=open(location, 'wb')
    q=urllib.request.urlopen(url)
    buff_size=8192
    while True:
        buff=q.read(buff_size)
        if not buff:
            break
        f.write(buff)
    f.close()
    print('Track Downloaded\n')
    
if __name__=='__main__':
    for track in sys.argv:
        if track==sys.argv[0]:
            continue
        (file_name, TRACK_ID)=get_track_id(track)
        download_url=MAIN_URL+TRACK_ID+STREAM+CLIENT_ID
        show_details(file_name, download_url)
        location=input('Save to location(eg. /bin): ')
        download_track(download_url, location+'/'+file_name)