import asyncio

import aiohttp
import datetime
from aiohttp import ClientConnectionError
from pretty_view import ExchangeView

pretty = ExchangeView()


async def request(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            result = await res.json()
            return result


async def exchange_for_days(curr: str, days: int):
    list_results = []
    for i in range(days):
        check_day = datetime.date.today() - datetime.timedelta(days=i)
        formatted_date = check_day.strftime("%d.%m.%Y")
        try:
            result = await request(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={formatted_date}')
            if result:
                list_results.append(result)
        except ClientConnectionError as err:
            print(f'Connection error {err}')
    res_list = []
    for el in list_results:
        for exchange_rate in el['exchangeRate']:
            if exchange_rate['currency'] == curr.upper():
                try:
                    res_list.append([el['date'], exchange_rate['purchaseRate'], exchange_rate['saleRate']])
                except KeyError:
                    pass
    if len(res_list) == 0:
        print(f'{curr.upper()} not found.')
    else:
        return print(pretty.create_row(res_list, curr))


if __name__ == '__main__':
    curr = input('Enter currency (ex. USD, EUR, PLN): ')
    days = int(input(f'For how many days you want to receive an information (less than 10)?: '))
    if days <= 10:
        asyncio.run(exchange_for_days(curr, days))
    else:
        print('Unfortunately, more than 10 days cant`n be processed.')
