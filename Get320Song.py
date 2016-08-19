import urllib2
from bs4 import BeautifulSoup
from os import path


def search_song_links(name = None):
    if name is None:
        song_name = raw_input("Please input the song name: ")
    else:
        song_name = name
    song_name = song_name.split(' ')
    search_link = "http://search.chiasenhac.vn/search.php?s="
    for aString in song_name:
        search_link = search_link + aString + "+"
    search_link = search_link[:-1]
    print "     The link is:  " + search_link
    response = urllib2.urlopen(search_link)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    all_song = soup.find_all('div', attrs={'class' : 'tenbh'})
    all_link = []
    for div in all_song:
        link = div.find('a')
        all_link.append("http://chiasenhac.vn/" + str(link['href'])[:-5] + "_download.html")
    return all_link


def get_song(a_link):
    response = urllib2.urlopen(a_link)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find_all('div', attrs={'id': 'downloadlink'})[0]
    div = str(div)
    links = []
    i = 0
    while True:
        link = 'http://'
        if div[i:i+6] == 'data16':
            while True:
                link += div[i]
                i += 1
                if i >= len(div) - 10:
                    break
                if div[i:i+4] == '.mp3':
                    link += '.mp3'
                    links.append(link)
                    break
        if i >= len(div) - 10:
            break
        i += 1

    the_link = None
    # find 320kb
    for a_link in links:
        if "[MP3 320kbps]" in a_link:
            the_link = a_link
            break
    if the_link is None:
        for a_link in links:
            if "[MP3 128kbps]" in a_link:
                the_link = a_link
            break

    if the_link is None and len(links) > 0:
            the_link = links[0]
    return the_link

def download_file(url):
    file_name = url.split('/')[-1]
    file_name = file_name.replace("%20"," ")
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8) * (len(status) + 1)
        print status,
    f.close()

def get_song_name_from_file():
    file = raw_input("Enter file with all song names you want to find: ")
    song_names = []
    with open(file, 'r') as f:
        song_names = f.readlines()
    return song_names


if __name__ == '__main__':
    songs = get_song_name_from_file()
    print "There are " + str(len(songs)) + " songs to process."
    i = 0
    for a_song in songs:
        i += 1
        a_song = a_song.replace("\n",'')
        print "Processing song " + str(i)+ ": "+ a_song + ''
        try:
            links = search_song_links(a_song)
            print "     Getting download link..."
            for a_link in links:
                the_song = get_song(a_link)
                if the_song is not None:
                    break
            if the_song is not None:
                download_file(the_song)
            else:
                print "     Can't find song to download"
        except:
            print "     Can't find song to download"











