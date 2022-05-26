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
    checker =  boost = False
    os.system('cls')
    print('[ {0.YELLOW}>{0.STOP} ] {0.GREEN}{0.BOLD}DISCORD NITRO GENERATOR{0.STOP}'.format(color))
    print('[ {0.YELLOW}>{0.STOP} ] {0.GRAY}Made with {0.RED}<3{0.STOP} {0.GRAY}by{0.STOP} Artic ({0.DARK_CYAN}{0.UNDERLINED}https://github.com/ArticOff{0.STOP})\n'.format(color))
    try:
        count = int(ask('How much codes will be generated'))
    except ValueError:
        print('\n[ {0.RED}>{0.STOP} ] Please enter an integer !\n'.format(color))
        return exit()
    if str(ask('Enable Checker (yes/no)')).lower() == 'yes':
        checker = True
        valid = invalid = 0
    else:
        checker = False
        valid =  invalid = 'CHECKER NOT ENABLED'
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
                async with session.get('https://discordapp.com/api/v9/entitlements/gift-codes/{}?with_application=false&with_subscription_plan=true'.format(code)) as response:
                    if response.status == 429:
                        try:
                            proxi = random.choice(rproxy)
                            index = rproxy.index(proxi)
                            del rproxy[index]
                        except IndexError:
                            print('\n[ {0.RED}>{0.STOP} ] There are no more proxies available !\n'.format(color))
                            return exit()
                        invalid += 1
                        badge = '{0.RED}-{0.STOP}'.format(color)
                    elif response.status == 404:
                        invalid += 1
                        badge = '{0.RED}-{0.STOP}'.format(color)
                    elif response.status == 200:
                        valid += 1
                        badge = '{0.GREEN}+{0.STOP}'.format(color)
                    print('[ {1} ] {0.DARK_CYAN}{0.UNDERLINED}https://discord.gift/{2}{0.STOP}'.format(color, badge, code))
        else:
            count -= 1
            print('[ {0.BLUE}~{0.STOP} ] {0.DARK_CYAN}{0.UNDERLINED}https://discord.gift/{1}{0.STOP}'.format(color, code))
    return [invalid, valid]

if __name__ == '__main__':
    gen = asyncio.get_event_loop().run_until_complete(main())
    print('\n[ {0.YELLOW}>{0.STOP} ] Result:\n{0.RED}Invalid{0.STOP}: {1[0]}\n{0.GREEN}Valid{0.STOP}: {1[1]}'.format(color, gen))
    print('\n[ {0.MAGENTA}*{0.STOP} ] {0.GRAY}Thanks for using our nitro generator !{0.STOP}\n'.format(color))
