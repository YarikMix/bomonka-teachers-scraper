import logging
from tqdm import tqdm


import requests
from bs4 import BeautifulSoup
from pytils import numeral

from functions import write_json, write_excel


HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
}

logging.basicConfig(
    format='%(asctime)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    level=logging.INFO
)


class Scraper:
    def get_data(self):
        url = "https://studizba.com/hs/151-mgtu-im-baumana/teachers/"
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, "html.parser")
        raw_data = soup.find("div", class_="cat-list").findChildren("div", recursive=False)

        logging.info("Будет собрана информация о {}".format(
            numeral.get_plural(len(raw_data), "кафедре, кафедрах, кафедр"),
        ))

        data = []

        for department in tqdm(raw_data):
            department_title = department.get("data-sort-name")[7:]
            department_url = department.find("a").get("href")
            teachers = self.get_teachers(department_url)

            if teachers == "Error":
                continue

            for teacher in teachers:
                data.append({
                    "Ф.И.О": teacher["Ф.И.О"],
                    "Кафедра": department_title,
                    "Должность": teacher["Должность"]
                })

        # TODO: Доделать
        # Сортируем преподователей
        # data.sort(key=lambda name: name.split(" ")[-1].lower())

        logging.info(f"Всего преподователей в бомонке - {len(data)}")

        return data

    def get_teachers(self, url):
        response = requests.get("https://studizba.com/hs/151-mgtu-im-baumana/teachers/" + url, headers=HEADERS)
        soup = BeautifulSoup(response.content, "html.parser")

        teachers = []

        try:
            raw_data = soup.find("div", class_="cat-list").findChildren("div", recursive=False)
            for teacher in raw_data:
                teachers.append({
                    "Ф.И.О": teacher.get("data-sort-name"),
                    "Должность": teacher.select(".link-teacher > .link-teacher-a > .link-teacher-name > .disnone800 > .one-teacher-descr")[0].getText()
                })

        except:
            return "Error"

        return teachers

    def main(self):
        teachers = self.get_data()
        write_json(teachers, "Преподователи")
        write_excel(teachers, "Преподователи")




if __name__ == "__main__":
    bomonka_scraper = Scraper()
    bomonka_scraper.main()