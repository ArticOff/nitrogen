"""
The MIT License (MIT)

Copyright (c) 2022-today Artic

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import random, string, os, aiohttp, asyncio, requests


class color:
    VIOLET = '\033[95m'
    CYAN = '\033[96m'
    DARK_CYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[37m'
    BLACK = '\033[30m'
    GRAY = '\033[38;2;88;88;88m'
    MAGENTA = '\033[35m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    NORMAL = '\033[22m'
    UNDERLINED = '\033[4m'
    STOP = '\033[0m'

def gen_code(lenght: int):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(lenght))

def scrape():
    scraped = 0
    f = open("proxies.txt", "a+")
    f.truncate(0)
    r = requests.get('https://api.proxyscrape.com/?request=displayproxies')
    proxies = []
    for proxy in r.text.split('\n'):
        proxy = proxy.strip()
        proxy = 'https://{}'.format(proxy)
        if proxy:
            proxies.append(proxy)
    for p in proxies:
        scraped = scraped + 1 
        f.write("{}\n".format(p))
    f.close()

def readproxies():
    try:
        p = open("proxies.txt", encoding="UTF-8")
    except FileNotFoundError:
        p = open("proxies.txt", "w+", encoding="UTF-8")
        raise SystemExit
    rproxy = p.read().split('\n')
    for i in rproxy:
        if i == "" or i == " ":
            index = rproxy.index(i)
            del rproxy[index]
    p.close()
    return rproxy

def ask(question: str):
    return input('[ {0.MAGENTA}?{0.STOP} ] {0.GRAY}{1}:{0.STOP} '.format(color, question))

rproxy = readproxies()

async def main():
    checker = False
    boost = False
    os.system('cls')
    print('[ {0.YELLOW}>{0.STOP} ] {0.GREEN}{0.BOLD}DISCORD NITRO GENERATOR{0.STOP}'.format(color))
    print('[ {0.YELLOW}>{0.STOP} ] {0.GRAY}Made by{0.STOP} Artic ({0.DARK_CYAN}{0.UNDERLINED}https://github.com/ArticOff{0.STOP})\n'.format(color))
    try:
        count = int(ask('How much codes will be generated'))
    except ValueError:
        print('\n[ {0.RED}>{0.STOP} ] Please enter an integer !\n'.format(color))
        return exit()
    if str(ask('Enable Checker (yes/no)')).lower() == 'yes':
        checker = True
    else:
        checker = False
    if str(ask('Boost codes or Classic codes (boost/classic)')).lower() == 'boost':
        boost = True
    else:
        boost = False
    print('')
    scrape()
    while count > 0:
        if boost:
            code = gen_code(24)
        else:
            code = gen_code(16)
        if checker:
            count -= 1
            badge = '#'
            async with aiohttp.ClientSession() as session:
                async with session.get('https://discord.com/api/v10/entitlements/gift-codes/{}'.format(code)) as response:
                    if response.status == 429:
                        try:
                            proxi = random.choice(rproxy)
                            index = rproxy.index(proxi)
                            del rproxy[index]
                        except IndexError:
                            print('\n[ {0.RED}>{0.STOP} ] There are no more proxies available !\n'.format(color))
                            return exit()
                        badge = '{}{}{}'.format(color.RED, '-', color.STOP)
                    elif response.status == 404:
                        badge = '{}{}{}'.format(color.RED, '-', color.STOP)
                    elif response.status == 200:
                        badge = '{}{}{}'.format(color.GREEN, '+', color.STOP)
                    print('[ {} ] {}{}https://discord.gift/{}{}'.format(badge, color.DARK_CYAN, color.UNDERLINED, code, color.STOP))
        else:
            count -= 1
            print('[ {0.BLUE}~{0.STOP} ] {0.DARK_CYAN}{0.UNDERLINED}https://discord.gift/{1}{0.STOP}'.format(color, code))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print('\n[ {0.MAGENTA}*{0.STOP} ] Thanks for using our nitro generator !\n'.format(color))
