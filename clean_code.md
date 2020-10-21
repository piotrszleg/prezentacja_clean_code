# Krótkie omówienie najciekawszej literatury 
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

## Używanie jednego stylu
Popularne style guide'y do Python'a:
- [google](https://google.github.io/styleguide/pyguide.html)
- [pep8](https://pep8.org/)

Często strona dużej korporacji która intensywnie używa danego języka będzie miała taki style guide. 

## Używanie nazw jako dokumentacji zamiast komentarzy
```python
# nie:
def area(a, b, c):
    # calculates area of a triangle using its sides
    p=(a+b+c)/2
    return sqrt(p*(p−a)*(p−b)*(p−c))

# tak:
# source: https://www.matemaks.pl/wzory-na-pole-trojkata.html
def triangle_area(side1, side2, side3):
    perimeter=side1+side2+side3
    half_of_perimeter=perimeter/2
    area_squared=half_of_perimeter
              *(half_of_perimeter−side1)
              *(half_of_perimeter−side2)
              *(half_of_perimeter−side3)
    return sqrt(area_squared)
```
- pasowało by i tak dodać docstring z typami argumentów i typem zwracanej wartości
- zmienne lokalne są całkowicie optymalizowane przez interpreter więc nie ma różnicy w wydajności tych dwóch funkcji.
- nazwy są weryfikowane przez interpreter, komentarze nie, dlatego też komentarze często tracą aktualność
- matematycy i fizycy dużo razy transformują swoje wzory, my nasze programy najczęściej czytamy

## Używanie elementów języka jako dokumentacji zamiast komentarzy

Przykład: dzięki `with` wiemy która część kodu używa obiektu builder'a:
```python
a.normalize()

with builder=Builder(result):
    builder.add(a)
    builder.add(b)

result.preprocess()
return result
``` 
Oraz oczywiście wyjątki.
```python
# nie:
# Will return None if there is no value
def find(array, element):
    ...

# tak:
def find(array, element):
    ...
    raise ElementNotFound()
```

Powinniśmy i tak w docstring'u zapisać że funkcja wyrzuca wyjątek. Różnica jest jednak taka że wyjątek `ElementNotFound` w konsoli więcej mówi nam o tym co się stało niż `AttributeError: 'NoneType' object has no attribute <attribute>`.

Niektóre języki wymagają też wpisywania wyjątków wyrzucanych przez funkcję w jej sygnaturze (Java) lub zwracania parametryzowanych enum'ów zamiast używania wyjątków (Rust).

## Używanie nazw i skrótów charakterystycznych dla dziedziny 
Przykład: piszemy `ip_address` a nie `internet_protocol_address`,
ponieważ każdy programista wie co oznacza ten skrót. 

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

## Kapsułkowanie (Encapsulation) 
- Tworzenie publicznego interfejsu klasy i ukrywanie prywatnych pól.
- Komponenty powinny być widoczne tylko poprzez interfejs.
TODO: roszerzyć

## Zawieranie się obiektów
```javascript
browser.currentPage.body.header.add(element)
```
Każdy element za kropką może być null'em. 
Ktoś może zmienić nazwę jednego z tych pól.
W tym momence jedna linijka mało istotnego kodu używa wiedzy o czterech warstwach struktury obiektowej programu. 
To utrudnia debugowanie i refactoring.

## Warstwy abstrakcji
Przykładowo kod routing'owy aplikacji webowej nie powinien już edytować treści strony.
Hierarchia takiej aplikacji webowej mogłaby wyglądać tak:
- Router - dopasowywanie adresów do obiektów typu Page
    - Page - logika stron
        - File - czytanie z pliku
        - TemplateBuilder - łączy dynamiczne i statyczne częsci strony
            - StringBuilder - optymalnie wykonuje operacje na zmiennych typu string
                - string - reprezentuje tekst

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
        return self.components[attr]

class BallLocationTask(Task):
    def start():
        ...
```
### *A co jak "się popsuje"?*
- częste commit'y i szczegółowe branch'e
- pisanie wyczerpujących testów dla nowego kodu 
- dopisywanie testów przed refactoringiem po wcześniejszych konsultacjach z autorami
- dotwarzanie dokumentacji w postaci komentarzy i doc-string'ów
- komunikacja na temat kompetencji poszczególnych członków projektu
- code review i wzajemna pomoc
- dyskusja z pozostałymi członkami projektu na temat stanu kodu i opłacalności refactoringu

## Częste błedy po przeczytaniu *Clean Code*
- gigantyczne nazwy jak np:
[AbstractBeanFactoryAwareAdvisingPostProcessor](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/aop/framework/autoproxy/AbstractBeanFactoryAwareAdvisingPostProcessor.html) w Spring Framework.
- usuwamy wszystko, globalny refactoring, zamieniamy wszystko na fabryki i abtrakcyjne klasy
- tworzenie niepotrzebnych abstrakcji; generalny plan działania ma wyglądać tak:
    - minimalistyczna abstrakcja która wydaje nam się słuszna
    - kod który chodzi poprawnie z tą abstrakcją
    - konieczność doimplementowania funkcjonalności
    - byle jakie doimplementowanie
    - refactoring i rozszerzenie abstrakcji

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
Wraz z rozwojem programu dodajemy nowe typy, funkcje, makra, uzgodnienia i konwencje.
Dlatego też proces tworzenia programu odpowiada procesowi tworzeniu języka programowania 
i powinniśmy się w nich kierować podobnymi regułami.

Przykładowe pytania:
- Czy typ który stworzyłeś byłby użyteczny i łatwy do zrozumienia gdyby istniał w bibliotece standardowej?
- Czy nazwy twoich funkcji i typów pozwalają czytać twój program jak gdyby był on instrukcją rozwiązania problemu w języku naturalnym?
- Czy twój kod użwający callback'ów wyraża kolejność działań?
- Czy twoje wybory rozwiązań są intuicyjne?
- Czy na użytkowników twoich klas oraz osób implemetujących stworzone przez ciebie interfejsy i klasy abstrakcyjne czekają pułapki?

# Practical Object-Oriented Design in Ruby
- stopniowy refactoring i ważene kosztu refactoringu z zyskami
- zamiana polimorfii na kompozycję przy użyciu komponentów
- odpowiedzialność obiektów na przykładzie wypożyczalni rowerów 
- grafy powiązań i ich analizowanie 
- testowanie przynależności obiektu do interfejsu 

# Metody organizacji
- lambdy i funkcje jako wartości 


**Mix-in'y** - w Pythonie istnieje wielokrotne dziedziczenie więc mix-in'y nie są niczym niezwykłym, C# nie pozwala na mix-in'y całkowicie. 

## Dependency injection 
Tworzymy interface lub klasę bazową dla pewnych obiektów i używamy ją w systemie. Użytkownik naszego systemu może później stworzyć własne klasy używając tego wzorca które będą miały wymyśloną przez niego funkcjonalność a następnie zarejestrować je w systemie.

```C#
interface Operation<T> {
    T perform(T a, T b);
    T neutralValue {get;};
}

class Addition : Operation<int> {
    public int perform(int a, int b){
        return a+b;
    }
    int neutralValue => 0;
}

calculator.register("+", Addition);
```

Popularnymi przykładami użycia *dependency injection* są aktorzy w grach, komponenty i stany w *finite state machine*.

## Finite state machine
FSM to model maszyny która ma swój stan oraz może przechodzić z jednego stanu na drugi. Stany najczęściej modeluje się za pomocą klas zawierających konstruktor, metodę start i update. Tak wymodelowane stany mogą wchodzić w interakcję z otoczeniem oraz rządać przejścia do innego stanu lub własnej terminacji. Częste jest też użycie stosu do przetrzymywania kolejno aktywowanych stanów, wtedy wykonywany jest stan na jego górze, a po terminacji stanu zostaje on z zdjęty ze stosu.

Przykład na postaci w grze:
- walk 
    - pozwala na chodzenie na boki 
    - po naciśnięciu na spację wrzuca na stos stany fall i jump
    - po naciśnięciu shift wrzuca na stos stan attack
    - po straceniu kontaktu z gruntem wrzuca na stos stan fall
- jump 
    - w swojej metodzie start przykłada do postaci siłę skierowaną w górę
    - kiedy przyspieszenie pionowe postaci przestaje mieć wartość dodatnią (ze względu na grawitację) ulega terminacji
- fall
    - po dotknięciu ziemi ulega terminacji
- attack
    - pokazuje animację
    - po zakończeniu się animacji ulega terminacji

Bardzo przydatny do rozkładania skomplikowanej funkcjonalności na kawałki, rozroszenia stanu programu na moduły i ułatwienia debuggowania.

## Alternatywy dla wartości null, wyjątków i callback'ów 
**Option\<T\>** to klasa która może ale nie musi zawierać wartości. 

Jeśli jest dobrze napisana (oraz dobrze wspierana przez język i narzędzia) będzie wyrzucać łatwiejsze w interpretacji wyjątki oraz uławiać wykrywanie błędów w czasie pisania programu. 

Używając **Option** jak typ wartości zwracanej przez funkcje daje się też znać użytkownikowi że brak zwracanej wartości jest czymś, czego ma się spodziewać.

```python
# rotate only if sensor outputted a value
read_result=sensor.read()
if sensor.hasValue:
    rotateTowards(sensor.value)

# "prostsza" składnia
sensor.read().ifHasValue(lambda v: rotateTowards(v))

# value field getter will raise error if there is no value
rotateTowards(sensor.value)
```

W module `typing` istnieje typ `Optional[X]`, mówi on jednak jedynie o tym, że zwracana wartość może mieć wartość typu X lub None co może być wykorzystane przez type checker ale nie ma wpływu na zachowanie programu.

**Result\<V, E\>** to klasa zawierająca wartość lub błąd. W przeciwieństwie do użycia raise użycie tego typu nie zaburza normalnego biegu programu co może być bardzo korzystne przy analizie jego działania.

W module `typing` istnieje typ `Union[X, Y]`, mówi on jednak jedynie o tym, że zwracana wartość może mieć wartość typu X lub Y co może być wykorzystane przez type checker ale nie ma wpływu na zachowanie programu.

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
- duża ilość argumentów (funkcja powinna mieć maksymalnie 3 zwyczajne argumenty nie licząc self) 
  - przekazywanie dict lub nazwanych argumentów 
    ```python
    schema=ArgumentsSchema(
        name=str,
        size=int,
        ...
    )
    def make(**args):
        schema.verify(args)
        ...
    ```
  - łańcuch wywołań
    ```python
    class Make():
        def with_size(self, size):
            assert_type(size, int)
            self.size=size
            return self

        ...

    Make.with_size(5).with_name("test").invoke()
    ``` 
- sekcje krytyczne z punktu widzenia wydajności
    - komentarze a w nich ASCII art, linki, objaśnienia
    - zrozumiałe nazwy
- obchodzenie bugów i quirków w zewnętrznych bibliotekach 
    - komentarze
    - owijanie w przyjazne abstrakcje
- implementowanie wzorów matematycznych i fizycznych 
    - używamy własnych nazw, nie literek ze wzoru
    - przyjazne abstrakcje jak Vector3 lub Line
- modyfikacja obiektu czy utworzenie nowego (`normalized` a `Normalize()`)
- callback hell
    - typy wspierające różne operacje (np. Promise) zamiast czystych wskaźników na funkcję
    - funkcje asynchroniczne (w pythonie generatory)
    - zupełna zmiana sposoby komunikacji między obeiktami (elm)

# Efektywne testowanie 

Potrzebne pojęcia
- dziedzina funkcji 
- umowy nieformalne (komentarze, nazwy, typy)

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

# Moje propozycje dotyczące modułu sterującego robota 
## Abstrakcyjny model łodzi
Implementacje modelu
  - wizualizująca w konsoli wartości czuników i silników
  - zapamiętująca przebieg do pliku
  - eksplorująca reakcje tasków na możliwe wartości z czujników
  - sprawdzający poprawność danych wpływających i wypływających z modelu
  - unity
  - fizyczna

Rezygnacja z wypisywania rzeczy do konsoli na rzecz modelu zapamiętującego (będzie on tworzył pliki *human readable* i pozwalał na wizualizację).

Task odgrywający przebieg z pliku.

Możliwość nakładania na siebie implementacji modelu na wzór warstw, np: konsolowy\*sprawdzjący\*zapamiętujący\*unity

Rezygnacja z pliku ze stałymi konfigurującymi przebieg programu na rzecz interaktywnej pracy w konsoli.

Model pełni jedynie rolę kontenera dla modułów (sensory, akcje, silniki), nie wprowadza własnej funkcjonalności.

Czujniki z taką pseudo notacją węgierską (mówiącą o zwracanej wartości)
- has_value 
- get_angle 
- get_euler_angles 
- get_position 
- get_distance 
- get_screen_position 

Każdy czujnik może zwrócić wartość `Fallback` która spowoduje przejście do czujnika z kolejnego modelu lub błąd krytyczny gdy takiego brak.

funkcjonalność
- grabber.close
- grabber.open
- grabber.is_open
- marker.drop
slinki
- set_value 
- get_value
- keep_value (konflikty jako wyjątki)

Model złożony przechodzi przez implemenetacje funkcjonalności i silników we wszystkich modelach i wszystkim zleca wykonanie zadania.

Mockupy sensorów eksplorujące ich możliwe wartości
```python
self.echo_locator=SensorTester(
    has_value=BooleansTester(),
    get_angle=NumbersTester(
                range=Range(0, 360), 
                edge_cases=[None, 0, 90, 180, 360]
              )
    )
```

## Controller
Klasa zajmująca się zarządzaniem stosem tasków oraz łączeniem tasków z modelem.

## Task'i
- taski jako parametryzowane stany w FSM ze stosem 
- zadania wkonywane między cyklami (wykrywanie obiektów, rozpoznawanie otoczenia, diagnostyka)
- każdy Task składałby się z dowolnie parametryzowanego konstruktora, start, update i cleanup.
- możliwość konfigurowania update-rate 
- forwardowan'ie obsługi FSM, czujników, akcji i silników do klasy Task przy użyciu `__getattr__` i podobnych funkcji
- mały rozmiar i kompozycja

```python
def LocateAndDropMarker(controller, target):
    return TasksSequence([
        LocateOnTheGround(target),
        FunctionTask(lambda: controller.marker.drop())
    ])

def LocateOnTheGround(controller, target):
    return RepeatUntilSuccess(TasksSequence([
        FindTarget(controller, target),
        CenterOnTargetHorizontally(controller, target),
        GoForwardUntilHoveringOver(controller, target),
    ]))

class TasksSequence(Task):
    def __init__(controller, subtasks):
        super().__init__(controller)
        self.target=target
        self.subtasks=subtasks

    def start(self):
        for subtask in subtasks:
            # push_subtask makes it so if any subtask
            # fails the main task fails as well 
            self.push_task(subtask)

    def control_returned(self):
        for subtask in subtasks:
            if not subtask_succeded:
                return Task.FAILURE
        return Task.SUCCESS

class GoForwardUntilHoveringOver(Task):
    def __init__(controller, target):
        super().__init__(controller)
        self.saved_camera=self.camera_selector.selected
        self.vision.set_target(target)
        self.camera_selector.select(Camera.BOTTOM)

    def start(self):
        self.movement=Vector3.FORWARD*MAX_SPEED

    def update(self):
        if self.collision_detector.has_value:
            return Task.FAILURE
        if self.vision.has_value:
            return Task.SUCCESS

    def cleanup(self):
        self.camera_selector.select(self.saved_camera)
```