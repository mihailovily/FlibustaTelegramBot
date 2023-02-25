import os
import sys
import pathlib
import zipfile
import click
import requests
import humanize
from pyquery import PyQuery as Pq
from tqdm import tqdm

_t = humanize.i18n.activate('ru_RU')

RATING = {
    'файл не оценен': 0,
    'файл на 1': 1,
    'файл на 2': 2,
    'файл на 3': 3,
    'файл на 4': 4,
    'файл на 5': 5
}


def get_search_result(book_name, sort):
    payload = {'ab': 'ab1', 't': book_name, 'sort': sort}
    try:
        r = requests.get('http://flibusta.is/makebooklist', params=payload)
    except requests.exceptions.ConnectionError:
        click.echo('не удалось подключиться к серверу flibusta.is')
        sys.exit(1)

    if r.text == 'Не нашлось ни единой книги, удовлетворяющей вашим требованиям.':
        os.system('echo "bad" > log.txt')
        tqdm.write(f'Не нашлось ни единой книги по запросу {book_name}')
        return 'No result'
    else:
        os.system('echo "ok" > log.txt')
        return r.text
        


def fetch_book_id(search_result, sort):
    doc = Pq(search_result)
    if sort == 'litres':
        book = [Pq(i)('div > a').attr.href for i in doc.find('div') if '[litres]' in Pq(i).text().lower()][0]
    elif sort == 'rating':
        books = [(Pq(i)('div > a').attr.href, Pq(i)('img').attr.title) for i in doc.find('div')]
        # print(books)
        # pass
        book = sorted(books, key=lambda book: RATING[book[1]], reverse=True)[0][0]
        # book = sorted(books, key=lambda book: RATING[book[1], reverse=True)[0][0]
    else:
        book = doc('div > a').attr.href
    return book


def get_all_links(books, sort='rating', file_format='fb2'):
    books_link = dict()
    for book_name in books:
        search_result = get_search_result(book_name, sort)
        if search_result == 'No result':
            continue
        else:
            book = fetch_book_id(search_result, sort)
            link = f'http://flibusta.is{book}/{file_format}'
            books_link[book_name] = link
    return books_link


def save_file(book_file, output_folder, file_format):
    filename = 'book.fb2'
    file_path = os.path.join(output_folder, filename)

    with open(file_path, 'wb') as f:
        f.write(book_file.content)

    if file_format == 'fb2':
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(output_folder)
        os.remove(file_path)


def download_sync(books_link, sfn, output_folder, file_format):
    downloaded_sizes, downloaded_book = [], []
    for book_name, book_link in tqdm(books_link.items(), miniters=1, disable=True):
        book_file = requests.get(book_link)
        save_file(book_file, output_folder, file_format)

        content_length = int(book_file.headers['content-length'])
        downloaded_sizes.append(content_length)
        downloaded_book.append(book_name)
        size = humanize.naturalsize(content_length)

    total_size = humanize.naturalsize(sum(downloaded_sizes))
    return downloaded_book, total_size

def statuscheck():
    a = open('log.txt').readlines()
    return a


def cli(filename, output_folder='', sort='rating', file_format='fb2', sfn=True):
    books = [filename]
    pathlib.Path(output_folder).mkdir(parents=True, exist_ok=True)
    books_link = get_all_links(books, sort, file_format)
    if statuscheck() == ['ok\n']:
        book, size = download_sync(books_link, sfn, output_folder, file_format)
        os.system("ls | grep fb2 >> name_of_book.txt")
        with open('name_of_book.txt') as f:
            filename = f.readline().rstrip('\n')
        os.rename(filename, 'book.fb2')
        os.system('rm name_of_book.txt')
    return book[0]
