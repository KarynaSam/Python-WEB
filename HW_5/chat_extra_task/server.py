import asyncio
import aiohttp
import logging
import websockets
import names
import datetime
import aiofile
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
from aiohttp import ClientConnectionError

logging.basicConfig(level=logging.INFO)


async def request(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            result = await res.json()
            return result


async def exchange_for_days(currency: str, days: int):
    list_results = []
    if days >= 10:
        return 'Unfortunately, more than 10 days cant`n be processed.'

    async with aiofile.AIOFile('log_exchange.txt', 'a') as f:
        log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await f.write(f"{log_time}:exchange executed\n")

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
            if exchange_rate['currency'] == currency.upper():
                try:
                    res_list.append([el['date'], exchange_rate['purchaseRate'], exchange_rate['saleRate']])
                except KeyError:
                    pass
    if len(res_list) == 0:
        return f'{currency.upper()} not found.'
    else:
        a = f"{' || '.join(f'{i[0]} Sell {currency.upper()} {i[1]} Buy {currency.upper()} {i[2]}' for i in res_list)}"
        return a


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distribute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distribute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            if message.startswith('exchange'):
                list_message = message.split(' ')
                exc = await exchange_for_days(str('EUR'), int(list_message[1]))
                await self.send_to_clients(str(exc))
            else:
                await self.send_to_clients(f"{ws.name}: {message}")


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, 'localhost', 8080):
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())