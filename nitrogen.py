import random, string, os, aiohttp, asyncio, requests

class color:
    VIOLET, CYAN, DARK_CYAN, BLUE, GREEN, YELLOW, RED, WHITE, BLACK, GRAY, MAGENTA, BOLD, DIM, NORMAL, UNDERLINED, STOP = '\033[95m', '\033[96m', '\033[36m', '\033[94m', '\033[92m', '\033[93m', '\033[91m', '\033[37m', '\033[30m','\033[38;2;88;88;88m', '\033[35m', '\033[1m', '\033[2m', '\033[22m', '\033[4m', '\033[0m'

def gen_code(lenght: int):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(lenght))

def scrape():
    f, scraped = open('proxies.txt', 'a+'), 0
    f.truncate(0)
    r, proxies = requests.get('https://api.proxyscrape.com/?request=displayproxies'), []
    for proxy in r.text.split('\n'):
        proxy = proxy.strip()
        proxy = 'https://{}'.format(proxy)
        if proxy:
            proxies.append(proxy)
    for p in proxies:
        scraped += 1 
        f.write('{}\n'.format(p))
    f.close()
    return scraped

def readproxies():
    try:
        p = open('proxies.txt', encoding='UTF-8')
    except FileNotFoundError:
        p = open('proxies.txt', 'w+', encoding='UTF-8')
        raise SystemExit
    rproxy = p.read().split('\n')
    for i in rproxy:
        if i == '' or i == ' ':
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
        print('\n[ {0.RED}>{0.STOP} ] {0.GRAY}Please enter an integer{0.STOP} !\n'.format(color))
        return exit()
    if str(ask('Boost codes or Classic codes (boost/classic)')).lower() == 'boost':
        boost = True
    else:
        boost = False
    if str(ask('Enable Checker (yes/no)')).lower() == 'yes':
        checker = True
        valid = invalid = 0
        print('\n[ {0.BLUE}i{0.STOP} ] {1} {0.GRAY}scraped proxys.{0.STOP}'.format(color, scrape()))
    else:
        checker = False
        valid =  invalid = 'CHECKER NOT ENABLED'
    print('')
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
    os.system('pause')
