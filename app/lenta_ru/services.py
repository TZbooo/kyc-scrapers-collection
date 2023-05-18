import time

from bsslib import get_driver


driver = get_driver()
driver.get('https://lenta.ru/parts/news/')
print('wait for page load')
time.sleep(5)

response = driver.execute_script('''
return await (await fetch("https://lenta.ru/parts/news/2/?full", {
    "headers": {
      "accept": "*/*",
      "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
      "sec-fetch-dest": "empty",
      "sec-fetch-mode": "cors",
      "sec-fetch-site": "same-origin",
      "x-requested-with": "XMLHttpRequest"
    },
    "referrer": "https://lenta.ru/parts/news/",
    "referrerPolicy": "strict-origin-when-cross-origin",
    "body": null,
    "method": "GET",
    "mode": "cors",
    "credentials": "include"
})).json();
''')
print(response)