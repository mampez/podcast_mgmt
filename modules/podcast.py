"""
----------------------------------------
  - Developed by Mencho: 24/10/2017

  - Last Update: 02/11/2017
----------------------------------------

"""
import os
import datetime
import warnings
import unicodedata
import socket
from dateutil import parser
import feedparser
import requests
import requests.packages.urllib3
from mutagen.easyid3 import EasyID3
import mutagen


## Timeout Requests
TIMEOUT = 120


class Podcast(object):
    """Podcast class"""
    
    def __init__(self, url):
        if not url:
            raise Exception('Podcast class needs a url')
        self.url = url
        self.rss = self.get_rss()
        self.podcast_list = []

        ## Create folders
        if not os.path.exists('downloads'):
            os.makedirs('downloads')
        if not os.path.exists('logs'):
            os.makedirs('logs')
        self.download_log = os.path.join('logs', 'log_download.csv')
        if not os.path.exists(self.download_log):    
            file(self.download_log, 'w').close()
            line_file = str('podcast_date' + ';' + 'podcast_title' + 'Name' + ';' + 'Link' + ';')
            write_file(self.download_log, line_file.encode("UTF-8"))   

    def get_rss(self):
        """Donwload and parse rss file

        Return arguments:
        RSS list 
        """
        rssfiles = []
        rssfiles.append(feedparser.parse(self.url))
        return rssfiles

    def get_links_filter(self, keyword, number_links):
        """Generate podcast_list with a number_links
           for download in based on a specific keyword 
           and rss list. 

           keyword arguments:
           keyword               --  Filter links by keyword 
           number_links          --  Number of links

           Return arguments:
           podcast_list          --  list with 'podcast_data' elements

           Each element of the list contains a unique podcast_data:

           entry.published = u'Thu, 3 Aug 2017 11:09:51 +0100' --> '2017-08-03'
           publishedDate = str(parser.parse(entry.published))[:10]

           podcast_data = [publishedDate, 
                          entry.enclosures[0]['href'], 
                          rss.feed.title
                          ]
        
           podcast_data = [u'Thu, 3 Aug 2017 11:09:51 +0100', 
                           u'Tertulia de Federico: M\xe1s ataques de las CUP contra el turismo', 
                           u'http://audios.esradio.fm/espana/17/08/03/
                             tertulia-de-federico-mas-ataques-de-las-cup-contra-el-turismo-116287', 
                           u'Es la Ma\xf1ana de Federico'
                          ]
        """
        podcast_data = []

        for entry in self.rss[0].entries:
            if keyword in entry.title:      
                try:
                    podcast_data = [entry.published, entry.title, 
                                    entry.enclosures[0]['href'], 
                                    self.rss[0].feed.title
                                   ]
                except IOError as error:
                    print 'Error' + (error) + ': File - ' + str(entry.title)
                self.podcast_list.append(podcast_data)
                if number_links != 0:
                    if len(self.podcast_list) == number_links: 
                        return self.podcast_list
        return self.podcast_list

    def get_links_all(self, number_links):
        """Generate podcast_list with a number_links
           for download in based on a rss list. 

           keyword arguments:
           number_links          --  Number of links

           Return arguments:
           podcast_list          --  list with 'podcast_data' elements

           Each element of the list contains 
           a unique podcast_data:

           entry.published = u'Thu, 3 Aug 2017 11:09:51 +0100' --> '2017-08-03'

           podcast_data = [publishedDate, 
                          entry.enclosures[0]['href'], 
                          rss.feed.title
                          ]
        
           podcast_data = [u'Thu, 3 Aug 2017 11:09:51 +0100', 
                           u'Tertulia de Federico: M\xe1s ataques de las CUP contra el turismo', 
                           u'http://audios.esradio.fm/espana/17/08/03/
                             tertulia-de-federico-mas-ataques-de-las-cup-contra-el-turismo-116287', 
                           u'Es la Ma\xf1ana de Federico'
                          ]
        """
        podcast_data = []

        for entry in self.rss[0].entries: 
            try:
                podcast_data = [entry.published, entry.title, 
                                entry.enclosures[0]['href'], 
                                self.rss[0].feed.title
                               ]
            except IOError as error:
                print 'Error' + (error) + ': File - ' + str(entry.title)
            self.podcast_list.append(podcast_data)
            if number_links != 0:
                if len(self.podcast_list) == number_links: 
                    return self.podcast_list
        return self.podcast_list

    def podcast_download(self):
        """Manage the podcast donwload, record in a 
           log file and convert the file to a tagged mp3

           keyword arguments:
           self.downlinks      --  podcast data

           Return arguments:
           None

           podcast_data = [u'Thu, 3 Aug 2017 11:09:51 +0100', 
                           u'Tertulia de Federico: M\xe1s ataques de las CUP contra el turismo', 
                           u'http://audios.esradio.fm/espana/17/08/03/
                             tertulia-de-federico-mas-ataques-de-las-cup-contra-el-turismo-116287, 
                           u'Es la Ma\xf1ana de Federico']
        """
        warnings.filterwarnings("ignore", category=UnicodeWarning)
        now = datetime.datetime.now()

        for podcast_file in self.podcast_list:
            published, name, link, title = podcast_file
            if self.podcast_list != []:
                line_file = (published + ';' + title + ';' + name + ';' + link).encode("utf-8") 
                if line_file in open(self.download_log).read():
                    pass
                else:
                    title = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore')
                    download_folder = os.path.join('downloads', title)
                    if not os.path.exists(download_folder): 
                        os.makedirs(download_folder)
                    try:
                        published = str(parser.parse(published))[:10]
                    except IOError as error:
                        print 'Error' + (error) + ': File - ' + str(title)
                    download_folder = os.path.join(download_folder, published)
                    if not os.path.exists(download_folder): 
                        os.makedirs(download_folder)
                    namefile_unicode = link[link.rfind('/')+1:]
                    namefile_str = unicodedata.normalize('NFKD', 
                                                         namefile_unicode).encode('ascii', 'ignore')
                    namefile_str = namefile_str.decode('utf-8', 'ignore').encode("utf-8")
                    if '.mp3' in namefile_str:
                        len_name = namefile_str.index('.mp3')
                    elif '.MP3' in namefile_str:
                        len_name = namefile_str.index('.MP3')
                    namefile_str = namefile_str[:len_name + 4]
                    fileoutput = os.path.join(download_folder, namefile_str)
                    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
                    print  '-' + str(published) + '; ' + name
                    ## downlink
                    download_file(link, fileoutput) 
                    ## tagging
                    mp3_tagging(fileoutput, podcast_file)
                    ## write log
                    write_file(self.download_log, line_file)
                    end = datetime.datetime.now()
                    print 'Download Time = ' + str(end-now) + '\r'
        return None


def write_file(file_name, line):
    """ Writing File

        keyword arguments:
        file_input      --  log file
        line            --  podcast log line

        Return arguments:
        None
    """
    try:
        with open(file_name, "a") as filename:
            filename.write(line)
            filename.write('\n')
    except IOError as error:
        print error
    return None

def mp3_tagging(file_input, podcast_list):

    """Tagging mp3 files
       
       keyword arguments:
       file_input      --  podcast filename
       podcast_list    --  podcast data

       Return arguments:
       None
    """
    try:
        tag = EasyID3(file_input)
    except mutagen.id3.ID3NoHeaderError:
        tag = mutagen.File(file_input, easy=True)
        tag.add_tags()
    tag['title'] = unicodedata.normalize('NFKD', podcast_list[1]).encode('ascii', 'ignore')
    tag['album'] = unicodedata.normalize('NFKD', podcast_list[3]).encode('ascii', 'ignore')
    tag['genre'] = 'Podcast'
    tag.save(v2_version=3)

    return None

def download_file(url, outputfile):
    """Download file (GET URL)

       keyword arguments:
       url               --  podcast url
       outputfile        --  output file

       Return arguments:
       None
    """
    try:
        req = requests.get(url, stream=True, timeout=TIMEOUT)
        try:
            with open(outputfile, 'wb') as file_download:
                for chunk in req.iter_content(chunk_size=1024): 
                    if chunk: 
                        file_download.write(chunk)
        except IOError as error:
            print error
    except requests.exceptions.RequestException as err:
        print err
    except socket.error as err:
        print err
    return None
