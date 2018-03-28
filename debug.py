import requests
import re


def main(url, string):
    # для остановки в этой точке и работы с консольным отладчиком
    # import pdb
    # pdb.set_trace()
    # также под отладкой можно запускать так:
    # > python -m pdb file.py

    site_code = get_site_code(url)
    matching = get_matching_str(site_code, string)
    print(f'"{string}" found {len(matching)} times in {url}')


def get_site_code(url):
    if not url.startswith('http'):
        url = 'https://' + url

    return requests.get(url).text


def get_matching_str(source, string):
    return re.findall(string, source)


main('www.mail.ru', 'script')