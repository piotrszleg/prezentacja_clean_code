# Efektywne testowanie 

Potrzebne pojęcia
- dziedzina funkcji - wartości dla których została zaprojektowana funkcja
- umowy (ang.: *contracts*) - komentarze, nazwy, typy i wiedza wspólna dla członków projektu na temat utworzonych klas i funkcji

## Mocking

Dobrze rozplątane obiekty powinny być łatwe do zastąpienia obiektami we wnętrzu których istnieją tylko asercje lub kod zapamiętujący operacje na nich wykonane. 

Częste jest też zamienianie baz danych obiektami używającymi słowników, co znacząco przyspiesza test. Idąc tym tokiem myślenia dowolną powolną lub niewygodną funkcję lub obiekt można zastąpić mock'iem.
```python
# tworzymy mock komponentu i sprawdzamy czy metody-eventy zostały wywołane
class ComponentEventsTester(Component):
    def __init__():
        self.expect_start=AssertHappened()
        self.expect_update=AssertHappenedMultipleTimes()

    def start():
        self.expect_start.fulfill()

    def update():
        self.expect_update.fulfill()

    def finalize():
        # jeżeli metody-eventy nie zostały wywołane to tutaj wyskoczy wyjątek
        self.expect_start.finalize()
        self.expect_update.finalize()

test_component=ComponentEventsTester()
system.add(test_component)
system.run()
test_component.finalize()
```

```python
# ten obiekt zbiera dane o użyciu bazy danych które później możemy sprawdzić asercjami
class DatabaseUsageCollector(Database):
    def __init__():
        self.writes=[]
        self.reads=[]
    
    def write(*args):
        self.writes.append(args)

    def read(*args):
        self.reads.append(args)
        return None

collector=DatabaseUsageCollector()
run_test_commands(system, collector)
assert(contains_name(collector.writes, "Piotr"))
...
```

## Testowane dużą ilością danych 
- używanie własności, np: 2+5=5+2
- konstrukcja danych które mają być później zdekonstruowane przez system `(name, domain)`=>`name@domain`
- weryfikacja zewnętrzna dużej ilości danych 
- testy polegające na badaniu jak system degeneruje się z czasem 
- trafianie na wyjątki występujące dla danych z dziedziny 

## Szczegółowe testy
- podstawowe założenia funkcji lub obiektu
- wyjątki - nie piszemy na zasadzie *może być, może nie być*, jeżeli w dokumentacji pisze że wyjątek jest to musi być a jego brak jest bug'iem
- edge cases (0, 1, -1, pusta lista, ujemny indeks itp.)
- załataniu bug'a powinno towarzyszyć utworzenie testu 
- testy dedykowane pod coverage (odwiedzanie wszystkich ścieżek)
- testy manualne - zbiór zadań wykonywanych przez człowieka-testera spisany w jakimś dokumencie
