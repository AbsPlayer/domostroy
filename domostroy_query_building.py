import domostroy

city_name = "Ростов" # город
zhk_name = "ЖК Звёздный-2" # название ЖК
building_name = "дом №3" # номер дома
building_url = "https://www.domostroydon.ru/novostroyki/zhk-zhk-zvezdnyy-2/dom-3" # ссылка на ЖК
# все введенные данные будут использованы в xls-отчёте

cities = {}
zhks = {}
buildings = {}
apartments = domostroy.parse_building(building_url)
buildings[building_name] = apartments
zhks[zhk_name] = buildings
cities[city_name] = zhks

for city, city_data in cities.items():
    domostroy.save_to_xlsx(city, city_data)
print("All done!")
