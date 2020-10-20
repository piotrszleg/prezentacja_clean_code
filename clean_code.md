# Krótkie omówienie najciekawszych literatury 
# Clean code
## Trzymanie się nazewnictwa 
```python
# nie
depth=depthSensor.getDepth()
angle=sonar.readAngle()
# tak
depth=depthSensor.getDepth()
angle=sonar.getAngle()
```
## Używanie nazw i wyrażeń języka jako dokumentacji zamiast komentarzy
```python
# nie:
def area(a, b, c):
    # calculates area of triangle using its sides
    p=(a+b+c)/2
    return sqrt(p*(p−a)*(p−b)*(p−c))

# tak:
# source: https://www.matemaks.pl/wzory-na-pole-trojkata.html
def triangleArea(sideA, sideB, sideC):
    perimeter=sideA+sideB+sideC
    halfOfPerimeter=perimeter/2
    areaSquared=halfOfPerimeter
              *(halfOfPerimeter−sideA)
              *(halfOfPerimeter−sideB)
              *(halfOfPerimeter−sideC)
    return sqrt(areaSquared)
``` 
- zmienne lokalne są całkowicie optymalizowane przez interpreter więc nie ma różnicy w wydajności tych dwóch funkcji.
- nazwy są weryfikowane przez interpreter, komentarze nie, dlatego też komentarze często tracą aktualność

Przykład użycia wyrażeń języka:
```python
with builder=Builder(result)
    builder.add(a)
    builder.add(b)
result.init()
return result
``` 

## Używanie nazw i skrótów charakterystycznych dla dziedziny 
Na przykład piszemy `ip_address` a nie `internet_protocol_address`,
ponieważ każdy programista zna ten skrót. 

## Zasady czystego programowania
- Do Not Repeat Yourself
- Keep it Simple Stupid
- You aren't gonna need it
- SOLID
    - **Single-responsibility principle**
    A class should only have a single responsibility, that is, only changes to one part of the software's specification should be able to affect the specification of the class.
    - **Open–closed principle**
    "Software entities ... should be open for extension, but closed for modification."
    - **Liskov substitution principle**
    "Objects in a program should be replaceable with instances of their subtypes without altering the correctness of that program." 
    - **Interface segregation principle**
    "Many client-specific interfaces are better than one general-purpose interface."
    - **Dependency inversion principle**
    One should "depend upon abstractions, [not] concretions."

## Enkapsulacja (pojedyncza kropka w wyrażeniu)
```python
browser.currentPage.body.header.add(element)
```
Każdy element za kropką może być null'em. 
Ktoś może zmienić nazwę jednego z tych pól.
W tym momence jedna linijka mało istotnego kodu używa wiedzy o czterech warstwach struktury obiektowej programu. 
To utrudnia debugowanie i refactoring.

## Warstwy abstrakcji
Przykładowo kod routing'owy aplikacji webowej nie powinien już edytować treści strony.
Hierarchia takiej aplikacji webowej:
- Router - dopasowywanie adresów do obiektów typu Page
    - Page - logika stron
        - File - czytanie z pliku
        - TemplateBuilder - łączy dynamiczne i statyczne częsci strony
            - StringBuilder - optymalnie wykonuje operacje na zmiennych typu string

## Maksymalne rozbicie na metody i klasy 
- jedna funkcja robi *jedną rzecz*
- jedna klasa ma *jedną rolę*
- użycie warstwy abstrakcji do osiągnięcia tych celów 

## Bycie "młodym harcerzem" i 'gnicie kodu"
Młody harcerz - programista który pozostawia każdą jednostkę kodu czystszą niż ją zastał.

Gnicie kodu (ang. *code rot*) - wraz z rozwojem starsze częsci kodu ulegają degradacji.
```python
# oryginał
class BallLocationTask():
    def __init__(self, sensors, motors):
        ...

# rozwój i gnicie
class BallLocationTask():
    def __init__(self, sensors, motors, environment, vision):
        ...

# propozycja refactoringu
class Task():
    def __init__(self, components):
        self.components=components
        self.start()

    def start(self):
        raise NotImplementeException()

    def __getattr_(self, attr):
        self.components[attr]

class BallLocationTask(Task):
    def start():
        ...
```
*A co jak się popusje?*
- częste commit'y i szczegółowe branch'e
- pisanie wyczerpujących testów dla nowego kodu 
- dopisywanie testów przed refactoringiem po wcześniejszych konsultacjach z autorami  
- komunikacja na temat kompetencji poszczególnych członków projektu
- code review i wzajemna pomoc
- dyskusja z pozostałymi członkami projektu na temat stanu kodu i opłacalności refactoringu

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
- dopasowanie do problemu

## Komunikacja 
Książka zaleca częstą i otwartą komunikację między zespołami oraz między zespołami a klientem. Krytykuje niekompetentne pośrednictwo oraz ukrywanie problemów i detali implementacji ze względu na chęć pokazania się z lepszej strony. Zaleca tworzenie szczegółowych dokumentów opisujących oczekiwane działanie programu.

## Prototypowanie 
Dzielimy projekty na prototypy throw-away'e które służą tylko do eksploracji i **nie mogą** być rozwijane po jej zakończeniu oraz na prototypy które nadają się do rozwoju.
Obydwa mają swój czas i miejsce.

# Structure and Interpretation of Computer Programs
## Konsekwencje ręcznego zarządzania stanem programu
```C#
// w metodzie Chunk.Start:
Random.seed=chunk.position.GetHashCode();

// w metodzie Player.Start:
Random.seed=name.GetHashCode();
speed=Random.value

// w metodzie Chunk.Generate wywołanej w kolejnej klatce:
x=Random.value()

// Rezultat: wartość x została wygenerowana ze złego seed'a, świat jest nieścisły i nie wiadomo dlaczego. 
// Możliwe rozwiązanie: użycie instancji System.Random zamiast statycznej klasy UnityEngine.Random,
// czego konsekwencją będzie konieczność przetrzymywania tej instancji w polu klasy.
```
## Pisząc program tworzysz język 
Wraz z rozwojem programu dodajemy nowe typy, funkcje, makra i uzgodnienia.
Dlatego też proces tworzenia programu odpowiada procesowi tworzeniu języka programowania 
i powinniśmy się w nich kierować podobnymi regułami.

Przykładowe pytania:
- Czy typ który stworzyłeś byłby użyteczny i łatwy do zrozumienia gdyby istniał w bibliotece standardowej?
- Czy nazwy twoich funkcji i typów pozwalają czytać twój program jak gdyby był on instrukcją rozwiązania problemu w języku naturalnym?
- Czy twój kod użwający callback'ów wyraża kolejność działań?
- Czy twoje wybory rozwiązań są intuicyjne?
- Czy na użytkowników twoich klas oraz osób implemetujących stworzone przez ciebie interfejsy i klasy abstrakcyjne czekają pułapki?

# Practical Object-Oriented Design in Ruby
- zamiana polimorfii na kompozycję przy użyciu komponentów
- odpowiedzialność obiektów na przykładzie wypożyczalni rowerów 
- grafy powiązań i ich analizowanie 
- testowanie przynależności obiektu do typu 

# Popularne style guide'y
- [google](https://google.github.io/styleguide/pyguide.html)
- [pep8](https://pep8.org/)

# Metody organizacji 
- dependency injection (+ problemy z rozszerzaniem interfejsu) 
- finite state machine 
- komponenty 
- mix-iny  
- lambdy i funkcje jako wartości 

## Alternatywy dla wyjątków i wartości null 
**Option\<T\>** to klasa która może ale nie musi zawierać wartości. 

Jeśli jest dobrze napisana (oraz dobrze wspierana przez język i narzędzia) będzie wyrzucać łatwiejsze w interpretacji wyjątki oraz uławiać wykrywanie błędów w czasie pisania programu. 

Używając **Option** jak typ wartości zwracanej przez funkcje daje się też znać użytkownikowi że brak zwracanej wartości jest czymś, czego ma się spodziewać.

```python
# rotate only if sensor outputted a value
read_result=sensor.read()
if sensor.hasValue:
    rotateTowards(sensor.value)

# "prostsza" składnia
sensor.read().ifHasValue(lambda v: rotateTowars(v))

# value field getter will raise error if there is no value
rotateTowards(sensor.value)
```
**Result\<V, E\>** to klasa zawierająca wartość lub błąd. W przeciwieństwie do użycia raise użycie tego typu nie zaburza normalnego biegu proramu co może być bardzo korzystne przy analizie działania programu.

**Promise\<V, E\>** reprezentuje proces który po jakimś czasie może zakończyć się sukcesem lub porażką.
```javascript
// source: https://javascript.info/promise-basics

// funkcja ładująca skrypt, która zwraca obiekt typu Promise
function loadScript(src) {
  return new Promise(function(resolve, reject) {
    let script = document.createElement('script');
    script.src = src;

    script.onload = () => resolve(script);
    script.onerror = () => reject(new Error(`Script load error for ${src}`));

    document.head.append(script);
  });
}

// użycie tej funkcji
loadScript("https://example.com/lodash.js").then(
  script => alert(`${script.src} is loaded!`),
  error => alert(`Error: ${error.message}`)
);

// łączenie Promises
let promises=[
    loadScript("https://example.com/lodash.js"),
    loadScript("https://example.com/bootstrap.js")
];
Promise.all(promises)
    .then(values => console.log(values));
// Promise posiada też metody any i race
// możliwe jest też dodanie własnych metod
// do prototypu Promise
```

# Częste zadania 
- ekstrakcja metod 
- rozszerzanie kompetencji metody 
- zamiana ciągu ifów/switcha na polimorfię 
- specjalne pola 
- monkey patching i inne nietypowe dodatki do języka które upraszczają kod 

# Częste problemy 
- duża ilość argumentów 
  - weryfikowalna dict
  - łańcuch wywołań withSize(5).withName("test").invoke() 
- sekcje krytyczne 
- obchodzenie bugów i quirków w zewnętrznych bibliotekach 
- implementowanie wzorów matematycznych i fizycznych 
- modyfikacja obiektu czy utworzenie nowego (normalized a Normalize())
- callbacks 

# Efektywne testowanie 

Potrzebne pojęcia
- dziedzina funkcji 
- umowy nieformalne (komentarze, nazwy, typy)

Mocking 
- dobrze rozplątane obiekty powinny być łatwe do zastąpienia obiektami we wnętrzu których istnieją tylko asercje 
- przykład component unity z asercjami w funkcjach wydarzeń 
```python
# tworzymy mock komponentu i sprawdzamy czy metody-eventy zostały wywołane
class ComponentEventsTester(Component):
    def __init__():
        self.expect_start=AssertHappened
        self.expect_update=AssertHappenedMultipleTimes

    def start():
        self.expect_start.fulfill()

    def start():
        self.expect_update.fulfill()

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
system.run(collector)
assert(contains_name(collector.writes, "Piotr"))
```

Testowane dużą ilością danych 
- używanie własności, np: 2+5=5+2
- konstrukcja danych które mają być zdekonstruowane przez system `(name,domain)`=>`name@domain`
- weryfikacja zewnętrzna dużej ilości danych 
- testy polegające na badaniu jak system degeneruje się z czasem 
- trafianie na wyjątki występujące dla danych z dziedziny 

Szczegółowe testy
- edge cases
- załataniu bug'a powinno towarzyszyć utworzenie testu 
- testy dedykowane pod coverage (odwiedzanie wszystkich ścieżek)

# Moje propozycje dotyczące modułu sterującego robota 
## Abstrakcyjny model łodzi
Możliwość nakładania na siebie implementacji modelu na wzór warstw, np: konsolowy\*asercyjny\*unity
implementacje modelu
  - pełna wizualizacja w konsoli wartości czuników i silników
  - zapamiętująca przebieg do pliku
  - odgrywająca przebieg z pliku
  - eksplorująca reakcje tasków na możliwe wartości z czujników
  - unity
  - fizyczna

Różne czujniki z taką pseudo notacją węgierską
   - hasValue 
   - getAngle 
   - getEulerAngles 
   - getPosition 
   - getDistance 
   - getScreenPosition 

Funkcjonalność
   - grabber.close
   - grabber.open
   - marker.drop
 - motors
   - setValue 
   - keepValue (konflikty jako wyjątki)
- mockupy sensorów eksplorujące ich możliwe wartości
- typu result i promise oraz ściśle sprawdzanie poprawności ich użycia

## Task'i
 - taski jako parametryzowane stany w FSM że stosem 
 - zadania wkonywane w tle (wykrywanie obiektów, rozpoznawanie otoczenia)
- każdy Task składałby się z dowolnie parametryzowanego konstruktora, init i update. 
- forwardowan'ie obsługi FSM, czujników, akcji i silników do klasy Task przy użyciu `__getattr__` i podobnych funkcji

```python
def LocateAndDropMarker(target):
    return TasksSequence([
        RepeatUntilSuccess(TasksSequence([
            FindTarget(controller, target),
            CenterOnTargetVertically(controller, target),
            GoForwardUntilHoveringOver(controller, target),
        ])),
        FunctionToTask(lambda: controller.marker.drop())
    ])

class TasksSequence(Task):
    def __init__(controller, subtasks):
        super(controller)
        self.target=target
        self.subtasks=subtasks

    def start(self):
        for subtask in subtasks:
            # push_subtask makes it so if any subtask
            # fails the main task fails as well 
            self.push_subtask(subtask)

class GoForwardUntilHoveringOver(Task):
    def __init__(controller, target):
        super(controller)
        self.target=target
        self.camera_selector.select(Camera.BOTTOM)

    def start(self):
        self.movement=Vector3.FORWARD*MAX_SPEED

    def update(self):
        if self.collision_detector.has_value:
            return Task.FAILURE
        if self.vision.has_value:
            return Task.SUCCESS
```