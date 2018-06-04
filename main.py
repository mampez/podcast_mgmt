""" Testing podcast downloader"""
from podcast import podcast


MAX_DOWNLOADS = 5

LINKS_ALL = ['http://feeds.99percentinvisible.org/99percentinvisible',
             'http://www.ivoox.com/podcast-retronautas_fg_f157575_filtro_1.xml']


def main():
    """ Testing podcast downloader"""

    for link in LINKS_ALL:
        podcast_obj = podcast.Podcast(link)
        podcast_obj.get_links_all(MAX_DOWNLOADS)
        podcast_obj.podcast_download()


if __name__ == "__main__":
    main()
