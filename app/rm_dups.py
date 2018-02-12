import tldextract
import argparse


class Application:
    _parser = {
        'description': 'Removes duplicate domains/urls/sub-domains from single/multiple files'
    }

    def __init__(self):
        self.PARSER = argparse.ArgumentParser(**self._parser)

        self.PARSER.add_argument('-i', '--input',
                                 dest='input_files',
                                 help='input file(s)',
                                 type=argparse.FileType('r', encoding='utf-8', errors='ignore'),
                                 nargs='+'
                                 )
        self.PARSER.add_argument('-o', '--output',
                                 dest='output_file',
                                 help='output file',
                                 type=argparse.FileType('a', encoding='utf-8', errors='ignore')
                                 )
        self.PARSER.add_argument('-m', '--mode',
                                 dest='mode',
                                 help='on what level we want to perform removal of duplicates',
                                 type=str,
                                 choices=['top', 'sub-domain', 'url'],
                                 default='top',
                                 nargs='?'
                                 )
        self.PARSER.add_argument('-s', '--save',
                                 dest='save',
                                 help='save urls with given prefix',
                                 type=str,
                                 choices=['http', 'None'],
                                 default='http',
                                 nargs='?'
                                 )

        self.args = self.PARSER.parse_args()

    def remove_duplicates(self):
        _match = dict()

        for file in self.args.input_files:
            for line in file:
                line = line.strip()
                url = tldextract.extract(line)

                if url.domain != '':

                    if self.args.mode == 'top':
                        # match
                        if _match.get(url.registered_domain) is True:
                            pass
                        else:
                            _match[url.registered_domain] = True
                            # write
                            if self.args.save == 'http':
                                self.args.output_file.write(f'http://{url.registered_domain}\n')
                            elif self.args.save == 'None':
                                self.args.output_file.write(f'{url.registered_domain}\n')

                    elif self.args.mode == 'sub-domain':
                        non_www = self._remove_www(url.fqdn)
                        # match
                        if _match.get(non_www) is True:
                            pass
                        else:
                            _match[non_www] = True
                            # write
                            if self.args.save == 'http':
                                self.args.output_file.write(f'http://{non_www}\n')
                            elif self.args.save == 'None':
                                self.args.output_file.write(f'{non_www}\n')

                    elif self.args.mode == 'url':
                        url = self._parse_url(line)
                        # match
                        if _match.get(url) is True:
                            pass
                        else:
                            _match[url] = True
                            # write
                            if self.args.save == 'http':
                                self.args.output_file.write(f'http://{url}\n')
                            elif self.args.save == 'None':
                                self.args.output_file.write(f'{url}\n')

    @staticmethod
    def _remove_www(u: str):
        if u.startswith('www.'):
            return u.replace('www.', '', 1)
        return u

    @staticmethod
    def _parse_url(u: str):
        if u.endswith('/'):
            u = u[:u.rfind('/')]

        if u.startswith('http://'):
            u = u.replace('http://', '', 1)

        elif u.startswith('https://'):
            u = u.replace('https://', '', 1)

        return u


if __name__ == '__main__':
    app = Application()
    app.remove_duplicates()
