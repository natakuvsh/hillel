import requests
from bs4 import BeautifulSoup
from django_school.models import Rate

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
           "Accept-Encoding": "gzip, deflate",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
           "Connection": "close", "Upgrade-Insecure-Requests": "1"}


def mono_rate():
    UAH_CODE = 980
    USD_CODE = 840

    r = requests.get("https://api.monobank.ua/bank/currency", headers=HEADERS)
    if r.status_code == 200:
        data = r.json()
    for d in data:
        if d['currencyCodeA'] == USD_CODE and d['currencyCodeB'] == UAH_CODE:
            vendor = 'Monobank'
            rate_buy = d['rateBuy']
            rate_sell = d['rateSell']
            Rate.objects.update_or_create(vendor=vendor,
                                          defaults={'currency_1': 'USD',
                                                    'currency_2': 'UAH',
                                                    'rate_buy': rate_buy,
                                                    'rate_sell': rate_sell
                                                    })
    print('Added rate for Monobank')


def privat_rate():
    r = requests.get("https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11", headers=HEADERS)

    if r.status_code == 200:
        data = r.json()
    for d in data:
        if d['ccy'] == 'USD' and d['base_ccy'] == 'UAH':
            vendor = 'Privatbank'
            rate_buy = d['buy']
            rate_sell = d['sale']
            Rate.objects.update_or_create(vendor=vendor,
                                          defaults={'currency_1': 'USD',
                                                    'currency_2': 'UAH',
                                                    'rate_buy': rate_buy,
                                                    'rate_sell': rate_sell
                                                    })

    print('Added rate for Privatbank')


def ukrsib_rate():
    r = requests.get('https://ukrsibbank.com/ru/currency-cash/', headers=HEADERS)

    if r.status_code == 200:
        content = r.content
        soup = BeautifulSoup(content, 'html.parser')
        rates = soup.select('ul.exchange__wrap li')

        rate = rates[0].find_all('div', attrs={'class': "exchange__item-text"})
        if rate[0].text == 'USD':
            vendor = 'Ukrsibbank'
            rate_buy = float(rate[1].text.replace(',', '.'))
            rate_sell = float(rate[2].text.replace(',', '.'))
            Rate.objects.update_or_create(vendor=vendor,
                                          defaults={'currency_1': 'USD',
                                                    'currency_2': 'UAH',
                                                    'rate_buy': rate_buy,
                                                    'rate_sell': rate_sell
                                                    })

    print('Added rate for Ukrsibbank')


def pumb_rate():
    r = requests.get(
        'https://www.eximb.com/ua/business/pryvatnym-klientam/pryvatnym-klientam-inshi-poslugy/obmin-valyut/kursy-valyut.html',
        headers=HEADERS)

    if r.status_code == 200:
        content = r.content
        soup = BeautifulSoup(content, 'html.parser')

        rates = soup.select('tbody')
        rate = rates[2].find_all('td')
        if rate[0].text == 'USD':
            vendor = 'Pumb'
            rate_buy = rate[2].text.replace(',', '.')
            rate_sell = rate[5].text.replace(',', '.')
            Rate.objects.update_or_create(vendor=vendor,
                                          defaults={'currency_1': 'USD',
                                                    'currency_2': 'UAH',
                                                    'rate_buy': rate_buy,
                                                    'rate_sell': rate_sell
                                                    })

    print('Added rate for Pumb')


def add_rates():
    pumb_rate()
    ukrsib_rate()
    privat_rate()
    mono_rate()
