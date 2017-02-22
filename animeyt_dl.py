"""Funciones para descarga de animeyt."""
import sys
import os
sys.path.append("externals/pynet")
sys.path.append("externals/pynet/modules/")

import pynet as net
import colors as clrs
import re
from bs4 import BeautifulSoup as Bs


BASE_LINK = 'http://www.animeyt.tv/'
DOWNLOAD_PATH = 'descargas'
RE_LINK_URL_JS = re.compile('.*url = \"(.*?)\";.*')

# ---------------------------------------------------
# scrapping por serie

def get_chapters_from_html(h_text):
    b_text = Bs(h_text, 'lxml')
    l_chapters = b_text.findAll(
        'div', {'class': 'serie-capitulos__list__item'})
    l_d_chapters = map(get_chapter_from_div, l_chapters)
    l_d_chapters.reverse()
    return l_d_chapters


def get_chapter_from_div(chapter_div):
    d_chapter = {}
    d_chapter.update({'title': get_chapter_title(chapter_div)})
    d_chapter.update({'link': get_chapter_link(chapter_div)})
    return d_chapter


def get_chapter_title(chapter_div):
    chapter_title = chapter_div.find('a').getText()
    return chapter_title


def get_chapter_link(chapter_div):
    chapter_link = chapter_div.find('a').get('href')
    return chapter_link


# ---------------------------------------------------------
# Scrapping en capitulo


def download_chapter(path_anime, d_chapter):
    path_chapter = "%s/%s.mp4" % (path_anime, d_chapter['title'])
    if os.path.exists(path_chapter):
        print "Ya existe %s" % path_chapter
    else:
        download_url = get_download_link(d_chapter['link'])
        try:
            clrs.m_aviso("using native wget")
            status = os.system('wget -O "%s" "%s"' % (path_chapter, download_url))
            if (status != 0):
                clrs.m_interr('\nCancelado wget')
                os.system('rm "%s"' % path_chapter)
        except Exception as e:
            clrs.m_aviso("wget failed, trying requests package mode")
            net.download_file(download_url, path_chapter)


def get_download_link(chapter_link):
    b_text = Bs(net.request_get(chapter_link).text, 'lxml')
    download_url_redir = b_text.find(
        'a', {'target': '_blank'}, text='Descarga').get('href')
    ## ubico enlace generado de descarga
    download_url = get_link_by_link_page(download_url_redir)
    return download_url

def get_link_by_link_page(dl_link):
    b_text = Bs(net.request_get(dl_link).text, 'lxml')
    script_tag = b_text.findAll('script')[1]
    text_url = script_tag.string.split('\n')[8]
    url_real = RE_LINK_URL_JS.match(text_url).groups()[0]
    return url_real



# -------------------------------------------------------------
# EN BUSQUEDA

BUSQUEDA_LINK = BASE_LINK + 'busqueda'


def search(criterio):
    req_obj = net.request_get(
        '%s?terminos=%s' % (BUSQUEDA_LINK, criterio.replace(' ', '+')))
    l_d_anime = get_animes_from_html(req_obj.text)
    return l_d_anime

# --------------------------------------------------------------
# GENERAL


def get_animes_from_html(h_text):
    b_text = Bs(h_text, 'lxml')
    l_anime_divs = b_text.findAll('article', {'class': 'anime'})
    l_d_animes = map(get_anime_from_div, l_anime_divs)
    return l_d_animes


def get_anime_from_div(anime_div):
    d_anime = {}
    d_anime.update({'title': get_title(anime_div)})
    d_anime.update({'poster': get_poster_link(anime_div)})
    d_anime.update({'synopsis': get_synopsis(anime_div)})
    d_anime.update({'link': get_link(anime_div)})
    d_anime.update({'date': get_date(anime_div)})
    d_anime.update({'status': get_status(anime_div)})
    d_anime.update({'genres': get_genres(anime_div)})
    d_anime.update({'tags': get_tags(anime_div)})
    return d_anime


def get_poster_link(anime_div):
    poster_link = anime_div.find('img', {'class': 'anime__img'}).get('src')
    return poster_link


def get_title(anime_div):
    anime_title = anime_div.find('h3', {'class': 'anime__title'}).getText()
    return anime_title


def get_synopsis(anime_div):
    anime_synopsis = anime_div.find(
        'p', {'class': 'anime__synopsis js-synopsis-reduce'}).getText()
    return anime_synopsis


def get_link(anime_div):
    anime_link = anime_div.find('a', {'anime__synopsis-container'}).get('href')
    return anime_link


def get_date(anime_div):
    anime_date = anime_div.find('span', {'class': 'icon-fecha'}).getText()
    return anime_date


def get_status(anime_div):
    anime_status = anime_div.find('span', {'class': 'anime__status'}).getText()
    return anime_status


def get_genres(anime_div):
    l_span_genre = anime_div.findAll('span', {'class': 'anime__genre'})
    l_genres = map(get_genre, l_span_genre)
    return l_genres


def get_genre(genre_span):
    genre = genre_span.getText()
    return genre


def get_tags(anime_div):
    l_span_tag = anime_div.findAll('span', {'class': 'anime__tag'})
    l_tags = map(get_tag, l_span_tag)
    return l_tags


def get_tag(tag_span):
    tag = tag_span.getText()
    return tag


def download_anime_from_url(anime_url, desde=None):
    req_obj = net.request_get(anime_url)
    if desde is None:
        l_d_chapters = get_chapters_from_html(req_obj.text)
    else:
        l_d_chapters = get_chapters_from_html(req_obj.text)[desde:]
    for ch in l_d_chapters:
        print 'descargando %s' % ch['title']
        download_chapter('%s/%s' % (DOWNLOAD_PATH, ch['title']), ch)

def download_anime_from_dict(anime_dict, desde=None):
    path_serie = "%s/%s" % (DOWNLOAD_PATH, anime_dict['title'])
    make_if_not_exists(path_serie)
    req_obj = net.request_get(anime_dict['link'])
    if desde is None:
        l_d_chapters = get_chapters_from_html(req_obj.text)
    else:
        l_d_chapters = get_chapters_from_html(req_obj.text)[desde:]
    for ch in l_d_chapters:
        print 'descargando %s' % ch['title']
        download_chapter(path_serie, ch)

def make_if_not_exists(dir_path):
    if os.path.exists(dir_path):
        print "Ya existe %s" % dir_path
    else:
        print "No existe %s" % dir_path
        os.mkdir(dir_path)

make_if_not_exists(DOWNLOAD_PATH)
print "Usar funcion download_anime_from_dict"
