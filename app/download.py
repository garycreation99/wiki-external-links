from ftplib import FTP
import gzip
import re
import os
import urllib.request
import os
import time


class WikiDownloader:
    _url = 'https://dumps.wikimedia.org/{0}/latest/{0}-latest-externallinks.sql.gz'
    _gz = './wiki-files/{0}-latest-externallinks.sql.gz'
    _sql = './wiki-files/{0}-latest-externallinks.sql'
    _links = './wiki-files/{0}-{1}-links.txt'

    def __init__(self, wiki):
        """ :param wiki: ex. 'plwiki' or 'enwiki' """
        self.wiki = wiki

    @property
    def file_gz(self):
        return self._gz.format(self.wiki)

    @property
    def file_sql(self):
        return self._sql.format(self.wiki)

    @property
    def download_url(self):
        return self._url.format(self.wiki)

    @property
    def file_links(self):
        return self._links.format(self.wiki, time.strftime("%Y-%m-%d"))

    def download(self):
        urllib.request.urlretrieve(self.download_url, self.file_gz)

    def unzip(self):
        # open files
        f_in = gzip.open(self.file_gz)
        f_out = open(self.file_sql, 'wb')
        # write to output
        for l in f_in:
            f_out.write(l)
        # close files
        f_in.close()
        f_out.close()

    def parse(self):
        sql_file = open(self.file_sql, 'r', encoding='utf-8', errors='ignore')
        links_file = open(self.file_links, 'a', encoding='utf-8', errors='ignore')
        for l in sql_file:
            if l.startswith('INSERT INTO'):
                for x in re.finditer(r'\((.*?)\)', l):
                    need = x.group(1).split(',')
                    if len(need) >= 4:
                        links_file.write(need[3].replace("'", '') + '\n')
        # close files
        sql_file.close()
        links_file.close()

    def clean_up(self):
        os.remove(self.file_sql)
        os.remove(self.file_gz)

    @staticmethod
    def save_error(err):
        with open('errors.txt', 'a', encoding='utf8', errors='ignore') as f:
            f.write(err)


def main():
    # read wiki-links file
    with open('./wiki-files/wiki-links.input', 'r') as f:
        wiki_links = f.read().split('\n')
    # iterate tru each wiki langauge
    for wiki in wiki_links:
        d = WikiDownloader(wiki)
        print('=================\n', wiki)
        try:
            print('Downloading')
            d.download()
            print('Unzipping')
            d.unzip()
            print('Parsing')
            d.parse()
            print('Removing files')
            d.clean_up()
        except Exception as error:
            WikiDownloader.save_error(f'{wiki}:{error}\n')
            print('Ups...', error)
            try:
                print('Removing files')
                d.clean_up()
            except Exception as error:
                print(error)