from requests_html import HTMLSession

session = HTMLSession()


def text_grabber(session, url):
    '''
    Собирает текст с сайта по ссылке
    :param session: HTMLSession
    :param url: Сайт, с которого дергается текст
    :return: строковую перменную text
    '''
    resp = session.get(url)
    status = resp.status_code
    print(status)

    if status != '200':
        for i in range(1,3):
            text = resp.html.xpath(f'//div//div[h{i}]//text()')
            text = ''.join(text)
        print(text)
        text = text.replace('\n\n', '')
        text = text.replace('\u21d2', ' ')
    else:
        print('Недоступен сайт')
    return text


def text_saver(intext):
    '''
    Сохраняет полученный текст в файл text.txt
    :param intext: Входящий текст в виде строковой переменной str
    :return: ничего
    '''
    with open('text.txt', 'a') as t:
        intext = intext.encode('utf-32')
        intext = intext.decode('utf-32')
        t.write(intext)


def top10_yandex(keyword):
    '''
    Функция возвращает первую страницу поисковой выдачи Яндекса, без очистки от директа, колдунщиков и агрегаторов
    результатов получается больше 10, для очистки нужно использовать методы yandex_filter() или url_filter()
    :param session: HTMLSesson
    :param keyword: фраза, по которой будет собираться поисковая выдача
    :return: список ссылок на сайты по выдаче
    '''
    session = HTMLSession()
    srch_url = f'https://yandex.ru/yandsearch?text={keyword}&lr=1'
    resp = session.get(srch_url)  # lr - номер региона
    status = resp.status_code
    print('Yandex status code: ' + str(status))
    url_list = resp.html.xpath('//div//h2/a//@href')
    url_list_2 = ['']
    for url in url_list:
        if yandex_filter(url):
            url_list_2.append(url)
        else:
            continue
    return url_list_2


def yandex_filter(url):
    '''
    Проверяет, относится ли ссылка из списка к сервисам яндекса или нет
    :param url: проверяемая ссылка
    :return: если ссылка не относится к домену yandex.ru, то True, иначе False
    '''
    if url.find('yandex.ru') == -1:
        return True
    else:
        return False


def url_filter(url, url_list):
    '''
    Проверяет, относится ли ссылка к доменам, которые содержатся в списке. Нужна, чтобы отминусовать агрегаторы и
    ненужные сайты
    :param url: проверяемая ссылка
    :param url_list: список нежелательных доменов
    :return: если ссылка не относится к списку, то True, если ссылка не относится к списку, то False
    '''
    for i in url_list:
        if url.find(i) == -1:
            continue
        else:
            return False
    return True


def top10_google(session, keyword):
    '''
    Собирает выдачу Гугла - первые 10 результатов
    :param session: HTMLSession
    :param keyword: фраза, по которой собирается ТОП
    :return: список ссылок из ТОП10
    '''
    resp = session.get(f'https://www.google.ru/search?q={keyword}&num=10&hl=en')
    status = resp.status_code
    print(f'Google status code: {status}')
    url_list = resp.html.xpath('//div[@class="r"]/a[1]/@href')
    return url_list


def top10_bing(session, keyword):
    '''
    Собирает выдачу Гугла - первые 10 результатов
    :param session: HTMLSession
    :param keyword: фраза, по которой собирается ТОП
    :return: список ссылок из ТОП10
    '''
    resp = session.get(f'http://www.bing.com/search?q={keyword}&count=10')
    status = resp.status_code
    print(f'bing status code: {status}')
    url_list = resp.html.xpath('//div//ol//li/h2/a/@href')
    return url_list


def resper(url):
    resp = session.get(url)
    status = resp.status_code
    print(f'{url} status code: {status}')
    if status == 200:
        return resp
    else:
        return False


def get_title(resp):
    '''
    Возвращает тег <Title> сайта
    :param resp: открытая страница
    :return: текст значения тега <Title> сайта
    '''
    return resp.html.xpath('//title/text()')[0]


def get_description(resp):
    '''
    Возвращает тег <meta description> сайта
    :param resp: открытая страница
    :return: текст значения тега <meta description> сайта
    '''
    return resp.html.xpath('//meta[@name="description"]/@content')[0]


def get_keywords(resp):
    '''
    Возвращает тег <meta keywords> сайта
    :type resp: открытая страница
    :return: текст значения тега <meta description> сайта
    '''
    try:
        return resp.html.xpath('//meta[@name="keywords"]/@content')[0]
    except IndexError:
        return ['No keywords']


def text_cleaner(intext):
    return 0


def clusterizer(url_list1, url_list2, i=0):
    for url1 in url_list1:
        for url2 in url_list2:
            i += 1 if url1 == url2 else 0
    if i > 3:
        print(f'Списки близки друг к другу, степень близости {i}')
        return True, i
    else:
        print(f'Не близки друг к другу, степень близости {i}')
        return False, i
