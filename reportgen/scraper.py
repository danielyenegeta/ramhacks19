import random
import requests
import time


def openfile(filename=None):
    global USER_AGENTS
    with open("/Users/zabih/Documents/ramhacks19/data/" + filename, 'r+') as f:
        lines = f.read().strip().split(",")
        return lines


USER_AGENTS = openfile(filename="browser_data.txt")
proxy_pass = openfile(filename='proxies.txt')
ACCEPT = openfile(filename='accept.txt')
ACCEPT_LANGUAGE = openfile(filename='accept_language.txt')
ACCEPT_ENCODING = openfile(filename='accept_encoding.txt')


def get_random(array):
    return array[random.randrange(0, len(array))]


def open_url(url):
    global header

    USE_PROXY = True

    header = {'User-Agent': get_random(USER_AGENTS),
              'Connection': 'Keep-Alive',
              'Accept-Language': get_random(ACCEPT_LANGUAGE),
              'Accept-Encoding': get_random(ACCEPT_ENCODING),
              'Accept': get_random(ACCEPT)
              }
    header = {'User-Agent': get_random(USER_AGENTS),
              'Accept-Language': get_random(ACCEPT_LANGUAGE),
              'Accept': get_random(ACCEPT),
              'Connection': 'Keep-Alive', }

    proxy = proxy_pass
    page = None
    for _ in range(5):
        try:
            s = requests.session()
            s.store_cookies = False
            s.keep_alive = False
            if (USE_PROXY):
                page = s.get(url, proxies={"https": get_random(proxy)}, headers=header, timeout=20)
            else:
                page = s.get(url, headers=header)
            page.connection.close()
            s.close()
            break  # success
        except Exception as e:
            if hasattr(e, 'code'):
                if e.code == 400:
                    print("Malformed URL --> ", url)
                    print("Skipping and processing next request")
                    return ""
                print("Error code ", e.code)
            print(f"Exception {e}")
            time.sleep(10)
    else:  # all ntries failed
        print("\n\nURL OPEN FAILED ALL RETRIES... SLEEPING FOR 2 MINS \n\n")
        time.sleep(120)

    return page.content
