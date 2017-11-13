""" Testing podcast downloader"""
from modules import podcast


MAX_DOWNLOADS = 5

LINKS_ALL = ['http://www.ondacero.es/rss/podcast/8805/podcast.xml',
             #'http://esradio.libertaddigital.com/cowboys-de-medianoche/podcast.xml',
             'http://www.ivoox.com/feed_fg_f167429_filtro_1.xml',
             'https://www.npr.org/rss/podcast.php?id=510289',
             #'http://feeds.feedburner.com/freakonomicsradio',
             'http://feeds.99percentinvisible.org/99percentinvisible',
             'http://www.ivoox.com/podcast-retronautas_fg_f157575_filtro_1.xml',
             'http://www.ondacero.es/rss/podcast/220270/podcast.xml'
            ]

LINKS_FILTER = ['http://esradio.libertaddigital.com/es-la-manana-de-federico/podcast.xml',
                'http://www.ondacero.es/rss/podcast/8272/podcast.xml',
                'http://esradio.libertaddigital.com/en-casa-de-herrero/podcast.xml'
               ]


def main():
    """ Testing podcast downloader"""
    
    ## All podcast
    for link in LINKS_ALL:
        podcast_obj = podcast.Podcast(link)
        podcast_obj.get_links_all(MAX_DOWNLOADS)
        podcast_obj.podcast_download()
 
    ## Filter podcast

    # Federico
    podcast_obj = podcast.Podcast(LINKS_FILTER[0])
    podcast_obj.get_links_filter('Federico', MAX_DOWNLOADS)
    podcast_obj.podcast_download()

    # Mas de uno
    podcast_obj = podcast.Podcast(LINKS_FILTER[1])
    podcast_obj.get_links_filter('Tertulia', MAX_DOWNLOADS)
    podcast_obj.podcast_download()

    # En casa de Herrero
    podcast_obj = podcast.Podcast(LINKS_FILTER[2])
    podcast_obj.get_links_filter('Tertulia', MAX_DOWNLOADS)
    podcast_obj.podcast_download()

if __name__ == "__main__":
    main()
