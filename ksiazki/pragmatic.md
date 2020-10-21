# Pragmatic programmer 
## Pojedyncze źródło prawdy
```python
# nie:
if speedFromConsoleArgument: 
    move(speedFromConsoleArgument)
elif jsonConfig:
    move(jsonConfig.speed)
else:
    move(10)
# tak:
# config przechodzi przez wszystkie źródła prawdy 
# według wybranej kolejności i ustala wartość speed
move(config.speed)
```
## Domain Specifc Languages
Powiedzmy że mamy:
- schemat danych przekazywanych przez sieć
- schemat bazy danych
- zbiór działań należących do danego zadania
- dużą ilość stałych używanych w różnych częściach projektu i ulegającyh częstym zmianom

Rozwiązanie - DSL transpilowany do wybranych języków lub interpretowany w czasie działania programu.

Zalety:
- pojedyncze źródło prawdy
- lepsza czytelność
- mniej pisania
- możliwość napisania dodatkowych narzędzi ze względu na prostotę języka
- możliwość korzystania z pomocy nieprogramistów
- dopasowanie do problemu

## Prototypowanie 
Dzielimy projekty na prototypy throw-away'e które służą tylko do eksploracji i **nie mogą** być rozwijane po jej zakończeniu oraz na prototypy które nadają się do rozwoju.
Obydwa mają swój czas i miejsce.

## Komunikacja 
Książka zaleca częstą i otwartą komunikację między zespołami oraz między zespołami a klientem. Krytykuje niekompetentne pośrednictwo oraz ukrywanie problemów i detali implementacji ze względu na chęć pokazania się z lepszej strony. Zaleca tworzenie szczegółowych dokumentów opisujących oczekiwane działanie programu oraz dzielenie się wczesnymi prototypami. 

Autorzy zalecają tworzenie dokumentacji kiedy program jest już stabilny, jednak implementacja programu na bazie już napisanej dokumentacji jest ich zdaniem bezsensowna i przede wszystkim męcząca.