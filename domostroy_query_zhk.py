import domostroy

city_name = input("Введите название города: ") # город
zhk_name = input("Введите название ЖК: ") # название ЖК
url_zhk = input("Введите ссылку на ЖК: ") # ссылка на ЖК
# все введенные данные будут использованы в xls-отчёте

cities = {}
zhks = {}
buildings = {}

buildings = domostroy.parse_buildings(url_zhk)
for building, url_building in buildings.items():
    apartments = domostroy.parse_building(url_building)
    buildings[building] = apartments
zhks[zhk_name] = buildings
cities[city_name] = zhks

for city, city_data in cities.items():
    domostroy.save_to_xlsx(city, city_data)

print("All done!")
