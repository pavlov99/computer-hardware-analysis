import csv
import logging
import re
import ssl
from bs4 import BeautifulSoup
from os import path
from urllib.request import urlopen

CPU_LIST_URL = 'https://www.cpubenchmark.net/cpu_list.php'
GPU_LIST_URL = 'https://www.videocardbenchmark.net/gpu_list.php'
DATA_FOLDER = path.join(
    path.dirname(path.dirname(path.abspath(__file__))), 'data')

ssl_context = ssl.SSLContext()
ssl_context.verify_mode = ssl.CERT_NONE

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def crawl_cpus():
    output_filename = path.join(DATA_FOLDER, 'cpus.csv')
    header = ['name', 'passmark', 'rank', 'value', 'price']
    logger.debug('Request CPU html page')

    cpu_data = urlopen(CPU_LIST_URL, context=ssl_context).read()
    logger.debug('Parse CPU html page')
    soup = BeautifulSoup(cpu_data, 'html.parser')

    num_rows = 0
    with open(output_filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(
            csvfile,
            dialect=csv.unix_dialect,
            quoting=csv.QUOTE_MINIMAL
        )
        csvwriter.writerow(header)

        for cpu_html in soup.find_all('tr', id=re.compile('cpu')):
            row = [t.get_text() for t in cpu_html.find_all('td')]
            assert len(row) == len(header)

            price_index = header.index('price')
            price = row[price_index]
            row[price_index] = None if price == 'NA' \
                else float(price.lstrip('$').rstrip('*').replace(',', ''))
            csvwriter.writerow(row)
            num_rows += 1

    logger.info('Successfully crawled {:,} CPU records'.format(num_rows))


def crawl_gpus():
    output_filename = path.join(DATA_FOLDER, 'gpus.csv')
    header = ['name', 'passmark', 'rank', 'value', 'price']
    logger.debug('Request GPU html page')

    gpu_data = urlopen(GPU_LIST_URL, context=ssl_context).read()
    logger.debug('Parse GPU html page')
    soup = BeautifulSoup(gpu_data, 'html.parser')

    num_rows = 0
    with open(output_filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(
            csvfile,
            dialect=csv.unix_dialect,
            quoting=csv.QUOTE_MINIMAL
        )
        csvwriter.writerow(header)

        for cpu_html in soup.find_all('tr', id=re.compile('gpu')):
            row = [t.get_text() for t in cpu_html.find_all('td')]
            assert len(row) == len(header)

            price_index = header.index('price')
            price = row[price_index]
            row[price_index] = None if price == 'NA' \
                else float(price.lstrip('$').rstrip('*').replace(',', ''))
            csvwriter.writerow(row)
            num_rows += 1

    logger.info('Successfully crawled {:,} GPU records'.format(num_rows))


if __name__ == '__main__':
    crawl_cpus()
    crawl_gpus()
