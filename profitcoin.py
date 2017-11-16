#!/usr/bin/env python
import urllib2
import json
import argparse


SRC_META = {
    'whattomine': {
        'url': "https://whattomine.com/coins.json",
        'sort_key': 'profitability',
        'reverse': True
    },
    'coinchoose': {
        'url': '',
        'sort_key': 'profitability',
        'reverse': True
    }
}


class ProfitCoin(object):
    '''
    This class handles retrieving a list of most
    profitable coins to mine and returning the data
    '''
    def __init__(self, src='whattomine'):
        self.src = src
        self.url = SRC_META[src]['url']
        self.sort_key = SRC_META[src]['sort_key']
        self.set_json_obj()
        self.set_coin_list()

    def set_json_obj(self):
        self.json_obj = self.get_json()

    def get_json(self):
        url_opener = urllib2.build_opener()
        url_opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        try:
            response = url_opener.open(self.url)
            string = response.read().decode('utf-8')
            json_obj = json.loads(string)
        except:
            json_obj = {'coins': {}}
        return json_obj

    def print_json(self, json_obj):
        print json.dumps(json_obj, indent=4, sort_keys=True),

    def set_coin_list(self):
        self.coin_list = self.get_coin_list()

    def get_coin_list(self):
        coin_list = []
        if self.src=='whattomine':
            # coins_list = [v for k,v in json_obj['coins'].iteritems()]
            for coin_set in self.json_obj['coins'].items():
                # we want a dict so get the main data
                coin = coin_set[1]
                # we don't have the name so let's add the key as the coin
                coin['coin'] = coin_set[0]
                # add this coin to the list!
                coin_list.append(coin)
        elif self.src=='coinchoose':
            pass
        else:
            pass
        # sort the list of dicts by the key specified
        sorted_list = sorted(coin_list, key=lambda k:k[self.sort_key], reverse=True)
        return sorted_list

    def print_coin_list(self):
        print self.coin_list or None


def parse_args():
    parser = argparse.ArgumentParser(description='This script will return the most profitable coin(s) to mine')
    parser.add_argument('-s','--source',
        default='whattomine',
        help='Data Source - a url to a JSON datasource')
    parser.add_argument('num',
        default=1,
        help='Number of coins to display',
        nargs='?')
    args = parser.parse_args()
    # if not (opts.plot_file or opts.csv_file):
    #     parser.error("You have to specify either a --csv-file or --plot-file!")
    return args


def main():
    args = parse_args()
    profit_coin=ProfitCoin(args.source)
    display_count=int(args.num)
    if not profit_coin.coin_list is None:
        print ' '.join([k['coin'] for k in profit_coin.coin_list[:display_count]]),
    else:
        print '',


if __name__ == '__main__':
    main()