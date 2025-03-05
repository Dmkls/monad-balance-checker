from web3 import AsyncWeb3, AsyncHTTPProvider
from datetime import datetime
from loguru import logger
import asyncio

logger.add('log.log', format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}', level='DEBUG')

RPC = "https://testnet-rpc.monad.xyz/"
w3 = AsyncWeb3(provider=AsyncHTTPProvider(endpoint_uri=RPC))

WALLETS = open("wallets.txt")
WALLETS_TO_GET_BALANCE = []

now = datetime.now()
formatted_date = now.strftime("%d-%m-%Y %H:%M:%S")


for line in WALLETS.readlines():
    if line.strip():
        line = line.strip()

        if line[:2] != '0x':
            line = '0x' + line

        if len(line) > 50:
            recipient_address = w3.eth.account.from_key(line).address
            WALLETS_TO_GET_BALANCE.append(recipient_address)
        else:
            WALLETS_TO_GET_BALANCE.append(line)

def write_failed_wallet(address: str):
    with open('failed.txt', 'a', encoding="utf-8") as f:
        f.write(f'{address}\n')

def write_success_wallet(address: str):
    with open('success.txt', 'a', encoding="utf-8") as f:
        f.write(f'{address}\n')

async def get_balance():

    for wallet in WALLETS_TO_GET_BALANCE:
        try:
            wallet_address = AsyncWeb3.to_checksum_address(AsyncWeb3.to_checksum_address(wallet))
            balance_in_wei = await w3.eth.get_balance(wallet_address)
            balance_in_mon = w3.from_wei(balance_in_wei, 'ether')
            balance_in_mon = round(balance_in_mon, 4)
            logger.success(f"{wallet} | Balance: {balance_in_mon} MON")
            write_success_wallet(f"{wallet} | Balance: {balance_in_mon} MON")
        except:
            logger.error(f"{wallet} | Error while receiving the balance")
            write_failed_wallet(wallet)

write_success_wallet(f'---------------------{formatted_date}------------------------')
write_failed_wallet(f'-----------{formatted_date}------------')
asyncio.run(get_balance())