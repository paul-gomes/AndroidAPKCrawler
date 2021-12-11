import requests
import bs4
import csv


class AppDetail:
    def __init__(self, category, title, link, number_of_installs ):
        self.category = category
        self.title = title
        self.link = link
        self.number_of_installs = number_of_installs


class GooglePlay:
    def __init__(self, baseUrl):
        self.baseUrl = baseUrl

    def get_app_list(self, categories):
        apps = []
        for category in categories:
            r = requests.get(self.baseUrl + "/category/" + category + "/top-free/")
            soup = bs4.BeautifulSoup(r.text, "html.parser")
            a_tags = soup.findAll("a", {'class': "l_item"})
            for x in range(len(a_tags)):
                if len([c for c in apps if c.category == category]) == 25:
                    break
                ir = requests.get(self.baseUrl + a_tags[x].attrs['href'])
                soup_ir = bs4.BeautifulSoup(ir.text, "html.parser")
                installs = soup_ir.find("td", text="Installs").find_next_sibling("td").text
                nr = requests.get(self.baseUrl + a_tags[x].attrs['href'] + "download/apk")
                soup = bs4.BeautifulSoup(nr.text, "html.parser")
                dl = soup.findAll("a", {'class': "variant"})
                if len(dl) > 0:
                    apps.append(AppDetail(category, a_tags[x].attrs['title'], dl[0].attrs['href'], installs))

        return apps

    def save_apps_list(self, apps):
        with open('data/app_data.csv', 'wb', ) as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Title', 'Category', 'Number_of_installs'])
            for a in apps:
                writer.writerow([a.title.encode('utf-8'), a.category.encode('utf-8'), a.number_of_installs])


    def download_apps_apk(self, apps):
        num = 1
        for a in apps:
            r = requests.get(a.link, stream=True, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5 (KHTML, like Gecko) '
                              'Version/9.1.2 Safari/601.7.5 '
            })
            print num, "Downloading......", a.title
            with open('data/apps/' + a.title.split()[0] + '.apk', 'wb') as file:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            num += 1
