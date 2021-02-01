import requests
import bs4
import openpyxl
from urllib.parse import urlparse, urljoin
import os


def save_to_xlsx(city, dict_data, zhk_name_manual=""):

    if zhk_name_manual != "":
        zhk_name_manual = "_" + zhk_name_manual
    filename = city + zhk_name_manual + ".xlsx"
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)
    if os.path.isfile(path):
        os.remove(path)
    wb = openpyxl.Workbook()
    ws = wb.active
    start_row = 1
    start_column = 1

    ws.cell(row=start_row, column=start_column + 0).value = "ЖК"
    ws.cell(row=start_row, column=start_column + 1).value = "Номер дома"
    ws.cell(row=start_row, column=start_column + 2).value = "Кол-во комнат"
    ws.cell(row=start_row, column=start_column + 3).value = "Площадь обшая"
    ws.cell(row=start_row, column=start_column + 4).value = "Цена м2"
    ws.cell(row=start_row, column=start_column + 5).value = "Цена за квартиру"
    ws.cell(row=start_row, column=start_column + 6).value = "Этаж"

    row_ = start_row + 1
    for zhk_name, buildings in dict_data.items():
        for building_name, apartments in buildings.items():
            for apartment in apartments:
                ws.cell(row=row_, column=start_column + 0).value = zhk_name
                ws.cell(row=row_, column=start_column + 1).value = building_name
                ws.cell(row=row_, column=start_column + 2).value = apartments[apartment]["Кол-во комнат"]
                ws.cell(row=row_, column=start_column + 3).value = apartments[apartment]["Общая площадь"]
                ws.cell(row=row_, column=start_column + 4).value = apartments[apartment]["Цена м2"]
                ws.cell(row=row_, column=start_column + 5).value = apartments[apartment]["Стоимость"]
                ws.cell(row=row_, column=start_column + 6).value = apartments[apartment]["Этаж"]
                row_ += 1

    return


def get_zhks_urls(city_url, url_zhks={}, params={}):

    up = urlparse(city_url)
    domain = up[0] + "://" + up[1]
    resp = requests.get(city_url, params=params)
    if resp.status_code == requests.codes.ok:
        page = params.get("page", 1)
        soup = bs4.BeautifulSoup(resp.text, "html.parser")
        zhks = soup.find_all(class_="district-card__full-name")
        for zhk in zhks:
            name_zhk = zhk.text
            url_zhk = urljoin(domain, zhk.attrs['href'])
            url_zhks[name_zhk] = url_zhk
        pages = soup.find(class_="page-item active")
        if pages is not None:
            temp_page = pages.next_element.next_element.next_element.next_element.get("class")
            if len(temp_page) > 1 and temp_page[1] == "disabled":
                return url_zhks
            else:
                params["page"] = page + 1
                get_zhks_urls(city_url, url_zhks, params)

    else:
        print("Сайт при считывании ЖК не отвечает!")
        quit()

    return url_zhks

    # if pages is not None:
    #     flag = True
    #     page = 2
    #     while flag:
    #         resp = requests.get(city_url, params={"page": page})
    #         if resp.status_code == requests.codes.ok:
    #             soup = bs4.BeautifulSoup(resp.text, "html.parser")
    #             pages = soup.find(class_="page-item active")
    #             zhks = soup.find_all(class_="district-card__full-name")
    #             for zhk in zhks:
    #                 name_zhk = zhk.text
    #                 url_zhk = domain + zhk.attrs['href']
    #                 url_zhks[name_zhk] = url_zhk
    #         else:
    #             print("Сайт при считывании ЖК не отвечает!")
    #             quit()
    #
    #         temp_page = pages.next_element.next_element.next_element.next_element.get("class")
    #         if len(temp_page) > 1 and temp_page[1] == "disabled":
    #             flag = False
    #         else:
    #             page += 1

    return url_zhks


def get_buildings_urls(zhk_url):

    url_buildings = {}
    up = urlparse(zhk_url)
    domain = up[0] + "://" + up[1]
    resp = requests.get(zhk_url)
    if resp.status_code == requests.codes.ok:
        soup = bs4.BeautifulSoup(resp.text, "html.parser")
        buildings = soup.find_all(class_="filter-table__column house-selling-item__number")
        for building in buildings:
            nd = building.text
            url_building = building.next.attrs['href']
            url_buildings[nd] = urljoin(domain, url_building)
    else:
        print("Сайт при считывании зданий не отвечает!")
        quit()

    return url_buildings


def get_building_data(url):

    resp = requests.get(url)
    if resp.status_code == requests.codes.ok:
        soup = bs4.BeautifulSoup(resp.text, "html.parser")
        pages = soup.find(class_="pagination")
        apartments = soup.find_all(class_="flat-card")
        dict_apartments = {}
        r = 1
        for apartment in apartments:
            qty_rooms = apartment.find(class_="flat-card__title-link").text[0]
            total_square = float(
                apartment.find(class_="flat-card__common-area").find(class_="key-value-table__value").text)
            temp_m2 = apartment.find(class_="flat-card__price-per-meter").find(class_="key-value-table__value")
            if temp_m2 is not None:
                price_m2 = int("".join(temp_m2.text.split()))
            else:
                price_m2 = int("".join(apartment.find(class_="flat-card__price-per-meter").contents[0].split()))

            temp_cost = apartment.find(class_="flat-card__price").find(class_="key-value-table__value")
            if temp_cost is not None:
                cost = int("".join(temp_cost.text.split()))
            else:
                cost = int("".join(apartment.find(class_="flat-card__price").text.split()))

            if apartment.find(class_="flat-card__floor") is not None:
                floors = apartment.find(class_="flat-card__floor").find(class_="key-value-table__value").text
            else:
                floors = ""

            for floor in floors.split(","):
                iFloor = floor.strip()
                if "-" not in floor:
                    dict_apartments[r] = {"Кол-во комнат": qty_rooms,
                                          "Общая площадь": total_square,
                                          "Цена м2": price_m2,
                                          "Стоимость": cost,
                                          "Этаж": iFloor}
                else:
                    temp_floors = floor.split("-")
                    start_floor = int(temp_floors[0].strip())
                    end_floor = int(temp_floors[1].strip())
                    for iFloor in range(start_floor, end_floor+1):
                        dict_apartments[r] = {"Кол-во комнат": qty_rooms,
                                              "Общая площадь": total_square,
                                              "Цена м2": price_m2,
                                              "Стоимость": cost,
                                              "Этаж": iFloor}
                        r += 1
                r += 1
    else:
        print("Сайт при считывании здания не отвечает!")
        quit()

    if pages is not None:
        flag = True
        page = 2
        while flag:
            resp = requests.get(url, params={"page": page})
            if resp.status_code == requests.codes.ok:
                soup = bs4.BeautifulSoup(resp.text, "html.parser")
                pages = soup.find(class_="page-item active")
                apartments = soup.find_all(class_="flat-card")
                for apartment in apartments:
                    qty_rooms = apartment.find(class_="flat-card__title-link").text[0]
                    total_square = float(
                        apartment.find(class_="flat-card__common-area").find(class_="key-value-table__value").text)

                    temp_m2 = apartment.find(class_="flat-card__price-per-meter").find(class_="key-value-table__value")
                    if temp_m2 is not None:
                        price_m2 = int("".join(temp_m2.text.split()))
                    else:
                        price_m2 = int("".join(apartment.find(class_="flat-card__price-per-meter").contents[0].split()))

                    temp_cost = apartment.find(class_="flat-card__price").find(class_="key-value-table__value")
                    if temp_cost is not None:
                        cost = int("".join(temp_cost.text.split()))
                    else:
                        cost = int("".join(apartment.find(class_="flat-card__price").text.split()))

                    if apartment.find(class_="flat-card__floor") is not None:
                        floors = apartment.find(class_="flat-card__floor").find(class_="key-value-table__value").text
                    else:
                        floors = ""

                    for floor in floors.split(","):
                        iFloor = floor.strip()
                        if "-" not in floor:
                            dict_apartments[r] = {"Кол-во комнат": qty_rooms,
                                                  "Общая площадь": total_square,
                                                  "Цена м2": price_m2,
                                                  "Стоимость": cost,
                                                  "Этаж": iFloor}
                        else:
                            temp_floors = floor.split("-")
                            start_floor = int(temp_floors[0].strip())
                            end_floor = int(temp_floors[1].strip())
                            for iFloor in range(start_floor, end_floor + 1):
                                dict_apartments[r] = {"Кол-во комнат": qty_rooms,
                                                      "Общая площадь": total_square,
                                                      "Цена м2": price_m2,
                                                      "Стоимость": cost,
                                                      "Этаж": iFloor}
                                r += 1
                        r += 1
            else:
                print("Сайт при считывании здания не отвечает!")
                quit()

            temp_page = pages.next_element.next_element.next_element.next_element.get("class")
            if len(temp_page) > 1 and temp_page[1] == "disabled":
                flag = False
            else:
                page += 1

    return dict_apartments


def get_site_urls():
    cities = {1: ("Ростов", "https://www.domostroydon.ru"),
              2: ("Воронеж", "https://domostroyrf.ru/voronezh"),
              3: ("Нижний Новгород", "https://www.domostroynn.ru"),
              }

    return cities


def print_cities_table(dict_cities):
    for key_city, data in dict_cities.items():
        print(key_city, "-", data[0])


def get_city_main_url(city_url):
    resp = requests.get(city_url)
    if resp.status_code == requests.codes.ok:
        soup = bs4.BeautifulSoup(resp.text, "html.parser")
        city_main_url = soup.find('span', text='Новостройки').parent.attrs['href']
    else:
        print("Сайт не отвечает!")
        quit()

    return city_main_url


def get_cities_names_urls(city_name, city_main_url):
    cities_urls = {city_name: {"url_city": city_main_url}}
    resp = requests.get(city_main_url)
    if resp.status_code == requests.codes.ok:
        soup = bs4.BeautifulSoup(resp.text, "html.parser")
        for item in soup.find(id="tab-district").find_all(type="checkbox"):
            city_id = item.attrs["value"]
            city_name = item.next.next.text
            pos = city_name.find(" (")
            city_name = city_name[:pos]
            city_url = get_city_url(city_main_url, city_id)
            cities_urls[city_name] = {"url_city": city_url}
    else:
        print("Сайт при считывании списка городов не отвечает!")
        quit()

    return cities_urls


def get_city_url(city_main_url, city_id):
    url_ = urljoin(city_main_url, "?DistrictSearch%5Blocality%5D="+city_id)
    city_url = requests.get(url_).url

    return city_url
