import urllib
import bs4
from bs4 import BeautifulSoup
import re
import lxml
from lxml import html
import requests

prefix = "https://www.law.cornell.edu"
xml_prefix = "https://www.federalregister.gov/documents/full_text/xml/"
def get_urls(filename):
    proposed_rule, final_rule = [], []
    f = open(filename, 'r+')
    for line in f:
        s = line.split('\t')
        if s[0] == 'Agency' or s[0][0] == 'M': continue
        proposed_rule.append(s[8])
        final_rule.append(s[9])
    print str(len(proposed_rule))
    return proposed_rule, final_rule


def clean_id(url_id):
    if url_id[len(url_id)-1] != '/':
        new_id = url_id[:-1]
        clean_id(new_id)
    else:
        return url_id

def recursive_scrape(proposed, final):
    count = 1
    for url in proposed:
        index = url[:64].rfind('/')
        xml_url = xml_prefix + url[42:index] + '.xml'
        page = requests.get(xml_url)
        tree = html.fromstring(page.content)
        rin = tree.xpath('//rin/text()')
        if len(rin) > 0:
            rin_text = rin[0][4:]
        else:
            rin_text = 'NA'
        print rin_text
        if rin_text == '1018-BA67':
            rin_text += '-' + str(count)
            count += 1
        filename = rin_text + '.txt'
        f = open(filename, 'w+')
        preamb1 = tree.xpath('//agency/text()')
        preamb2 = tree.xpath('//subagy/text()')
        preamb3 = tree.xpath('//cfr/text()')
        preamb4 = tree.xpath('//depdoc/text()')
        preamb = tree.xpath('//sum/p/text()')
        preamb5 = tree.xpath('//lstsub/hd/text()')
        preamb6 = tree.xpath('//lstsub/p/text()')
        preamb7 = tree.xpath('//amdpar/text() | //section/sectno/text()')
        preamb8 = tree.xpath('//section/p/text() | //section/p/e/text()')
        new6 = []
        for item in preamb6:
            new6.append(item.encode('ascii', 'ignore'))
        new7 = []
        for item in preamb7:
            new7.append(item.encode('ascii', 'ignore'))
        new8 = []
        for item in preamb8:
            new8.append(item.encode('ascii', 'ignore'))
        '''print preamb1
        print preamb2
        print preamb3
        print rin
        print preamb4
        print preamb
        print preamb5
        print new6
        print new7
        print new8'''
        f.write(str(preamb1) + '\n\n')
        f.write(str(preamb2) + '\n\n')
        f.write(str(preamb3) + '\n\n')
        f.write(str(rin) + '\n\n')
        f.write(str(preamb4) + '\n\n')
        f.write(str(preamb) + '\n\n')
        f.write(str(preamb5) + '\n\n')
        for item in new6:
            f.write(str(item) + '\n')
        f.write('\n')
        if rin_text == '1018-BA67-1' or rin_text == '1018-BA67-2':
            preamb6 = tree.xpath('//p/text()')
            for item in preamb6:
                f.write(str(item.encode('ascii', 'ignore')) + '\n')
        f.write('\n')
        for item in new7:
            if item[:9] == 'The rules':
                f.write(str(item) + '\n')
        f.write('\n')
        for item in new8:
            f.write(str(item) + '\n')

        '''page = urllib.urlopen(url).read()
        soup = BeautifulSoup(page, "html5lib")
        letters = soup.find_all("li", class_="tocitem")
        print(len(letters))

    dict = {}
    for element in letters:
        dict[element.a.get_text()] = {}

        link = prefix + element.a["href"]
        page = urllib.urlopen(link).read()
        soup = BeautifulSoup(page, "html5lib")
        print element.a.get_text()
        dict[element.a.get_text()] = chapter_scrape(soup)

    #print dict
    with open('jlist.txt', 'w+') as outfile:
        json.dump(dict, outfile)'''


if __name__ == '__main__':
    proposed, final = get_urls('reg_database.tsv')
    recursive_scrape(proposed, final)
