""" Testing podcast downloader"""
from modules import podcast


LINKS_ALL = ['http://www.ondacero.es/rss/podcast/8805/podcast.xml',
             'http://esradio.libertaddigital.com/cowboys-de-medianoche/podcast.xml',
             'http://www.ivoox.com/feed_fg_f167429_filtro_1.xml'
            ]

LINKS_FILTER = ['http://esradio.libertaddigital.com/es-la-manana-de-federico/podcast.xml',
                'http://www.ondacero.es/rss/podcast/8272/podcast.xml'
               ]


def main():
    """ Testing podcast downloader"""
    
    ## All podcast
    for link in LINKS_ALL:
        podcast_obj = podcast.Podcast(link)
        podcast_obj.get_links_all(10)
        podcast_obj.podcast_download()

    ## Filter podcast
    podcast_obj = podcast.Podcast(LINKS_FILTER[0])
    podcast_obj.get_links_filter('Federico', 5)
    podcast_obj.podcast_download()

    podcast_obj = podcast.Podcast(LINKS_FILTER[1])
    podcast_obj.get_links_filter('Tertulia', 2)
    podcast_obj.podcast_download()


if __name__ == "__main__":
    main()