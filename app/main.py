from download import main as DownloadWikis
from rm_dups import Application as RemoveDuplicates
import os
import sys


dir_ = './wiki-files/'


def output_file(f):
    return f.replace('links.txt', 'links_toplevel_domains.txt')


if __name__ == '__main__':
    DownloadWikis()
    wiki_files = [x for x in os.listdir(dir_) if x.endswith('-links.txt')]

    for file in wiki_files:
        print(f'Removing duplicates in {file}')
        app = RemoveDuplicates()
        app.args.input_files = [open(dir_+file, 'r', encoding='utf-8', errors='ignore')]
        app.args.output_file = open(dir_+output_file(file), 'a', encoding='utf-8', errors='ignore')
        app.remove_duplicates()
