# -*- coding: utf-8 -*-
from pymongo import MongoClient
import mechanize
from BeautifulSoup import BeautifulSoup

client = MongoClient()
db = client.kenesh


def scraper():
    # load kenesh page
    br = mechanize.Browser()
    br.set_handle_robots(False)   # ignore robots
    br.set_handle_refresh(False)  # can sometimes hang without this
    br.addheaders = [('User-agent', 'Firefox')]  # User-Agent
    #browsing links of loaded page previously
    br1 = mechanize.Browser()
    br1.set_handle_robots(False)   # ignore robots
    br1.set_handle_refresh(False)  # can sometimes hang without this
    br1.addheaders = [('User-agent', 'Firefox')]  # User-Agent

    url = "http://www.kenesh.kg/RU/Folders/4258-Uchastie_deputatov_v_zasedaniyax_ZHogorku_Kenesha.aspx"
    br.open(url)

    for link in br.links(text_regex="Сведения об участии депутатов в заседаниях"):
        link_url = "http://www.kenesh.kg" + link.url
        # Open absentees link
        respose = br1.open(link_url)
        # Read content of the link and load it in endrit_soup
        html_content = respose.read()
        endrit_soup = BeautifulSoup(html_content)
        if endrit_soup.find('table', style=lambda x: x and x.startswith('width:102.84')):
            table = endrit_soup.find('table', style=lambda x: x and x.startswith('width:102.84'))
        elif endrit_soup.find('table', style=lambda x: x and x. startswith('border-bottom: medium none; border-left')):
            table = endrit_soup.find('table', style=lambda x: x and x. startswith('border-bottom: medium none; border-left'))
        table_soup = table
        table_rows = table_soup.findAll('tr')

        for row in table_rows:
            if row != 0:
                for cell in row.findAll('td'):
                    if cell.findAll('div'):
                        cell_soup = cell.findAll('div')
                        print cell_soup[0].text
                    else:
                        cell_soup = cell.find('ol')
                        for attr, val in cell_soup.attrs:
                            if attr == "start":
                                print val
                print "----------------------"
        print '----------------------------------------'

scraper()
