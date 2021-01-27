import domostroy

city_name = input("Введите название города: ") # город
zhk_name = input("Введите название ЖК: ") # название ЖК
building_name = input("Введите номер дома: ") # номер дома
building_url = input("Введите ссылку на дом: ") # ссылка на ЖК
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
