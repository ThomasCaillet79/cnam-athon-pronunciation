from requests_html import HTMLSession
import re
import pandas as pd
from bs4 import BeautifulSoup

class Scrapping:
    
    def scrap_from_longman(word):

        # requête http
        URL = 'https://www.ldoceonline.com/dictionary/'+word
        session = HTMLSession()
        response = session.get(URL)

        if (response.status_code == 200):

            # récupération du body
            html_doc = response.content
            body = BeautifulSoup(html_doc,'html.parser').find('body')

            # instanciation des listes de données à récupérer
            list_type = []
            list_pron = []
            list_audio_br = []
            list_audio_us = []

            # récupération des spans contenant les données recherchées
            frq_head = body.findAll('span', {'class': re.compile('(frequent )*Head')})

            for result in frq_head:
                # recherche des spans des valeurs POS et PRON dans les sous-arbres
                if result.find('span', {'class':'POS'}) is not None:
                    list_type.append(result.find('span', {'class':'POS'}).text.strip())
                if result.find('span', {'class':'PRON'}) is not None:
                    list_pron.append(result.find('span', {'class':'PRON'}).text.strip())

                spans_of_freq_head = result.findAll('span')

                # recherche des spans ayant comme attribut data-src-mp3
                for span in spans_of_freq_head:
                    if span.has_attr('data-src-mp3'):
                        if 'British' in span['title']:
                            list_audio_br.append(span['data-src-mp3'])
                        elif 'American' in span['title']:
                            list_audio_us.append(span['data-src-mp3'])

            # nombre d'homonymes
            nb_hom = len(list_type)

            # création du dataframe final
            list_mots = nb_hom * [mot]
            while (len(list_pron) < nb_hom):
                list_pron.append(list_pron[0])

            df_result = pd.DataFrame(list(zip(list_mots, list_type, list_pron, list_audio_br, list_audio_us)),
                            columns = ['mot', 'type', 'pron', 'audio_br', 'audio_us'])
        else:
            # on retourne quand même un tableau vide concatenable
            df_result = pd.DataFrame(columns = ['mot', 'type', 'pron', 'audio_br', 'audio_us'])

        return df_result