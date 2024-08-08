try:
    import requests, re, random, string, base64, urllib.parse, json, time, os, sys
    from requests_toolbelt import MultipartEncoder
    from rich import print as printf
    from PIL import Image
    import pytesseract
    from rich.panel import Panel
    from rich.console import Console
    from requests.exceptions import RequestException
except (ModuleNotFoundError) as e:
    __import__('sys').exit(f"Error: {str(e).capitalize()}!")

COOKIES, SUKSES, LOGOUT, GAGAL = {
    "Cookie": None
    }, [], [], []

class DIPERLUKAN:

    def __init__(self) -> None:
        pass

    def LOGIN(self):
        with requests.Session() as r:
            r.headers.update(
                {
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Host': 'zefoy.com',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
                    'Sec-Fetch-User': '?1',
                    'Sec-Fetch-Dest': 'document'
                }
            )
            response = r.get('https://zefoy.com/').text
            if 'Sorry, you have been blocked' in str(response) or 'Just a moment...' in str(response):
                printf(Panel(f"[italic red]Zefoy server is currently affected by cloudflare, you can try again until cloudflare\nis gone, please visit[italic green] zefoy.com[italic red] to check it!", width=56, style="bold bright_white", title="[ Cloudflare ]"))
                sys.exit()
            else:
                self.captcha_image = re.search('src="(.*?)" onerror="imgOnError\\(\\)"', str(response)).group(1).replace('amp;', '')
                self.form = re.search('type="text" name="(.*?)"', str(response)).group(1)
                r.headers.update(
                    {
                        'Cookie': "; ".join([str(x) + "=" + str(y) for x, y in r.cookies.get_dict().items()]),
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
                    }
                )
                response2 = r.get('https://zefoy.com{}'.format(self.captcha_image))

                with open('Penyimpanan/Gambar.png', 'wb') as w:
                    w.write(response2.content)
                w.close()
                r.headers.update(
                    {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Connection': 'keep-alive',
                        'Origin': 'null',
                        'Cache-Control': 'max-age=0',
                        'Cookie': "; ".join([str(x) + "=" + str(y) for x, y in r.cookies.get_dict().items()])
                    }
                )
                data = {
                    self.form: self.BYPASS_CAPTCHA(),
                }
                response3 = r.post('https://zefoy.com/', data = data).text

                if 'placeholder="Enter Video URL"' in str(response3):
                    COOKIES.update(
                        {
                            "Cookie": "; ".join([str(x)+"="+str(y) for x,y in r.cookies.get_dict().items()])
                        }
                    )
                    printf(f"[bold bright_white]   ───>[bold green] LOGIN SUCCESSFUL!                ", end='\r')
                    time.sleep(2.5)
                    return (COOKIES['Cookie'])
                else:
                    printf(f"[bold bright_white]   ───>[bold red] LOGIN FAILED!                     ", end='\r')
                    time.sleep(2.5)
                    return (False)

    def BYPASS_CAPTCHA(self):
        self.file_gambar = ('Penyimpanan/Gambar.png')
        self.image = Image.open(self.file_gambar)
        self.image_string = pytesseract.image_to_string(self.image)
        return (self.image_string.replace('\n', ''))
    
    def MENDAPATKAN_FORMULIR(self, video_url):
        with requests.Session() as r:
            r.headers.update(
                {
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'Host': 'zefoy.com',
                    'Cookie': f'{COOKIES["Cookie"]}; window_size=1280x601; user_agent=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F127.0.0.0%20Safari%2F537.36;',
                    'Sec-Fetch-Site': 'none',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-User': '?1',
                    'Sec-Fetch-Dest': 'document',
                }
            )
            response = r.get('https://zefoy.com/').text

            if 'placeholder="Enter Video URL"' in str(response):
                self.video_form = re.search('name="(.*?)" placeholder="Enter Video URL"', str(response)).group(1)
                self.post_action = re.findall('action="(.*?)">', str(response))[3]
                printf(f"[bold bright_white]   ───>[bold green] SUCCESSFULLY FOUND VIDEO FORM!   ", end='\r')
                time.sleep(1.5)
                self.MENGIRIMKAN_TAMPILAN(self.video_form, self.post_action, video_url)
            else:
                printf(f"[bold bright_white]   ───>[bold red] VIDEO FORM NOT FOUND!        ", end='\r')
                time.sleep(3.5)
                COOKIES.update(
                    {
                        "Cookie": None
                    }
                )
                return (False)
    
    def MENGIRIMKAN_TAMPILAN(self, video_form, post_action, video_url):
        global SUKSES, GAGAL
        with requests.Session() as r:
            boundary = '----WebKitFormBoundary' \
                + ''.join(random.sample(string.ascii_letters + string.digits, 16))
            r.headers.update(
                {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
                    'Cookie': f'{COOKIES["Cookie"]}; {self.BYPASS_IKLAN_GOOGLE()}; window_size=1280x601; user_agent=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F127.0.0.0%20Safari%2F537.36;',
                    'Sec-Fetch-Mode': 'cors',
                    'Sec-Fetch-Site': 'same-origin',
                    'Connection': 'keep-alive',
                    'Origin': 'https://zefoy.com',
                    'Sec-Fetch-Dest': 'empty',
                    'Content-Type': 'multipart/form-data; boundary={}'.format(boundary),
                    'Accept': '*/*'
                }
            )

            data = MultipartEncoder(
                {
                    video_form: (None, video_url)
                }, boundary=boundary
            )

            response = r.post('https://zefoy.com/{}'.format(post_action), data = data).text
            self.base64_string = self.DECRYPTION_BASE64(response)

            if 'type="submit"' in str(self.base64_string):
                boundary = '----WebKitFormBoundary' \
                    + ''.join(random.sample(string.ascii_letters + string.digits, 16))
                r.headers.update(
                    {
                        'Content-Type': 'multipart/form-data; boundary={}'.format(boundary),
                    }
                )
                self.find_form_videoid = re.search('type="hidden" name="(.*?)" value="(\d+)"', str(self.base64_string))
                self.form_videoid, self.videoid = self.find_form_videoid.group(1), self.find_form_videoid.group(2)
                self.next_post_action = re.search('action="(.*?)"', str(self.base64_string)).group(1)
                data = MultipartEncoder(
                    {
                        self.form_videoid: (None, self.videoid)
                    }, boundary=boundary
                )

                response2 = r.post('https://zefoy.com/{}'.format(self.next_post_action), data = data).text
                self.base64_string2 = self.DECRYPTION_BASE64(response2)

                if 'Successfully 1000 views sent.' in str(self.base64_string2):
                    SUKSES.append(f"{self.base64_string2}")
                    printf(Panel(f"""[bold white]Status :[bold green] Successfully...
[bold white]Link :[bold red] {video_url}
[bold white]Views :[bold yellow] +1000""", width=56, style="bold bright_white", title="[ Sukses ]"))
                    printf(f"[bold bright_white]   ───>[bold green] TRY SENDING VIEWS AGAIN!           ", end='\r')
                    time.sleep(2.5)
                    self.MENGIRIMKAN_TAMPILAN(video_form, post_action, video_url)
                elif 'Successfully ' in str(self.base64_string2) and ' views sent.' in str(self.base64_string2):
                    self.views_sent = re.search('Successfully (.*?) views sent.', str(self.base64_string2)).group(1)
                    SUKSES.append(f"{self.base64_string2}")
                    printf(Panel(f"""[bold white]Status :[bold yellow] Successfully...
[bold white]Link :[bold red] {video_url}
[bold white]Views :[bold green] +{self.views_sent}""", width=56, style="bold bright_white", title="[ Sukses ]"))
                    printf(f"[bold bright_white]   ───>[bold green] TRY SENDING VIEWS AGAIN!           ", end='\r')
                    time.sleep(2.5)
                    self.MENGIRIMKAN_TAMPILAN(video_form, post_action, video_url)
                else:
                    GAGAL.append(f"{self.base64_string2}")
                    printf(f"[bold bright_white]   ───>[bold red] FAILED TO SEND VIEWS!           ", end='\r')
                    time.sleep(3.5)
                    COOKIES.update(
                        {
                            "Cookie": None
                        }
                    )
                    return (False)
            elif 'Checking Timer...' in str(self.base64_string):
                printf(f"[bold bright_white]   ───>[bold green] WAIT FOR 4 MINUTES!          ", end='\r')
                time.sleep(2.5)

                list(map(lambda _: (self.DELAY(0, 30), self.ANTI_LOGOUT()), range(8)))

                printf(f"[bold bright_white]   ───>[bold green] TRY SENDING VIEWS AGAIN!           ", end='\r')
                time.sleep(2.5)
                self.MENGIRIMKAN_TAMPILAN(video_form, post_action, video_url)
            elif 'Please try again later or' in str(self.base64_string):
                printf(f"[bold bright_white]   ───>[bold red] PLEASE TRY AGAIN IN A FEW MOMENTS!     ", end='\r')
                time.sleep(2.5)
                self.DELAY(0, 300)
                return (False)
            elif 'Please try again later. Server too busy.' in str(self.base64_string):
                printf(Panel(f"[italic red]Zefoy server is busy, you can try again in a few days, please check regularly on zefoy.com!", width=56, style="bold bright_white", title="[ Server Sibuk ]"))
                sys.exit()
            elif 'An error occurred. Please try again.' in str(self.base64_string):
                printf(f"[bold bright_white]   ───>[bold red] AN ERROR OCCURRED, PLEASE TRY AGAIN IN A FEW MOMENTS!", end='\r')
                time.sleep(2.5)
                self.DELAY(0, 120)
                return (False)
            elif 'Too many requests. Please slow down.' in str(self.base64_string):
                printf(f"[bold bright_white]   ───>[bold red] SUBJECT TO SPAM OR LIMIT!           ", end='\r')
                time.sleep(2.5)
                self.DELAY(0, 500)
                return (False)
            else: # YOU CAN DEBUGGING IF THIS ERROR HAPPENS!
                printf(f"[bold bright_white]   ───>[bold red] FAILED TO GET VIEWS FORM!     ", end='\r')
                time.sleep(3.5)
                COOKIES.update(
                    {
                        "Cookie": None
                    }
                )
                return (False)

    def ANTI_LOGOUT(self):
        with requests.Session() as r:
            r.headers.update(
                {
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Cookie': COOKIES["Cookie"],
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'Host': 'zefoy.com',
                    'Sec-Fetch-Site': 'none',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-User': '?1',
                    'Sec-Fetch-Dest': 'document',
                }
            )
            response = r.get('https://zefoy.com/').text
        return (True)

    def DECRYPTION_BASE64(self, base64_code):
        return base64.b64decode(urllib.parse.unquote(base64_code[::-1])).decode()
    
    def DELAY(self, menit, detik):
        self.total = (menit * 60 + detik)
        while (self.total):
            menit, detik = divmod(self.total, 60)
            printf(f"[bold bright_white]   ───>[bold white] TUNGGU[bold green] {menit:02d}:{detik:02d}[bold white] SUKSES:-[bold green]{len(SUKSES)}[bold white] GAGAL:-[bold red]{len(GAGAL)}          ", end='\r')
            time.sleep(1)
            self.total -= 1
        return ("0_0")

    def BYPASS_IKLAN_GOOGLE(self):
        with requests.Session() as r:
            r.headers.update(
                {
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Cookie': COOKIES["Cookie"],
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'Host': 'zefoy.com',
                    'Sec-Fetch-Site': 'none',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-User': '?1',
                    'Sec-Fetch-Dest': 'document',
                }
            )
            params = {
                'domain': 'zefoy.com',
                'callback': '_gfp_s_',
                'client': 'ca-pub-3192305768699763',
            }
            response = r.get('https://partner.googleadservices.com/gampad/cookie.js', params=params).text
            if '_gfp_s_' in str(response):
                self.json_cookies = json.loads(re.search('_gfp_s_\\((.*?)\\);', str(response)).group(1))
                return (f"_gads={self.json_cookies['_cookies_'][0]['_value_']}; __gpi={self.json_cookies['_cookies_'][1]['_value_']}")
            else:
                return ('_gads=; __gpi=;')

class MAIN:

    def __init__(self):
        try:
            self.TAMPILKAN_LOGO()
            printf(Panel(f"[italic white]Please fill in your tiktok video link, make sure the account is not private and the\nlink is correct. Take the video link via browser!", width=56, style="bold bright_white", title="[ Link Video ]", subtitle="╭─────", subtitle_align="left"))
            video_url = Console().input("[bold bright_white]   ╰─> ")
            if 'tiktok.com' in str(video_url) or '/video/' in str(video_url):
                printf(Panel(f"[italic white]You can use[italic green] CTRL + C[italic white] if stuck and use[italic red] CTRL + Z[italic white] if you want to stop. If views do not come\nin try running manually and run this program again!", width=56, style="bold bright_white", title="[ Catatan ]"))
                while True:
                    try:
                        if COOKIES['Cookie'] == None or len(COOKIES['Cookie']) == 0:
                            DIPERLUKAN().LOGIN()
                        else:
                            printf(f"[bold bright_white]   ───>[bold green] SENDING VIEWS!     ", end='\r')
                            time.sleep(2.5)
                            DIPERLUKAN().MENDAPATKAN_FORMULIR(video_url)
                    except (AttributeError, IndexError):
                        printf(f"[bold bright_white]   ───>[bold red] UNABLE TO FIND LOGIN FORM!     ", end='\r')
                        time.sleep(7.5)
                        continue
                    except (RequestException):
                        printf(f"[bold bright_white]   ───>[bold red] YOUR CONNECTION IS HAVING A PROBLEM!     ", end='\r')
                        time.sleep(7.5)
                        continue
                    except (KeyboardInterrupt):
                        printf(f"\r                                 ", end='\r')
                        time.sleep(2.5)
            else:
                printf(Panel(f"[italic red]Please fill in the TikTok video link correctly, make sure you take the video link in the browser!", width=56, style="bold bright_white", title="[ Link Salah ]"))
                sys.exit()
        except (Exception) as e:
            printf(Panel(f"[italic red]{str(e).capitalize()}!", width=56, style="bold bright_white", title="[ Error ]"))
            sys.exit()

    def TAMPILKAN_LOGO(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        printf(
            Panel("""[bold red]● [bold yellow]● [bold green]●[bold white]
[bold red] ______     ______     ______   ______     __  __    
[bold red]/\___  \   /\  ___\   /\  ___\ /\  __ \   /\ \_\ \   
[bold red]\/_/  /__  \ \  __\   \ \  __\ \ \ \/\ \  \ \____ \  
[bold white]  /\_____\  \ \_____\  \ \_\    \ \_____\  \/\_____\ 
[bold white]  \/_____/   \/_____/   \/_/     \/_____/   \/_____/
\t[underline green]Free Tiktok Views - Coded by Rozhak""", width=56, style="bold bright_white")
        )
        return (True)

if __name__ == '__main__':
    try:
        os.system('git pull')
        if os.path.exists("Penyimpanan/Subscribe.json") == False:
            youtube_url = json.loads(requests.get('https://raw.githubusercontent.com/RozhakXD/Zefoy/main/Penyimpanan/Youtube.json').text)['Link']
            os.system(f'xdg-open {youtube_url}')
            with open('Penyimpanan/Subscribe.json', 'w') as w:
                w.write(json.dumps({
                    "Status": True
                }))
            w.close()
            time.sleep(3.5)
        MAIN()
    except (Exception) as e:
        printf(Panel(f"[italic red]{str(e).capitalize()}!", width=56, style="bold bright_white", title="[ Error ]"))
        sys.exit()
    except (KeyboardInterrupt):
        sys.exit()