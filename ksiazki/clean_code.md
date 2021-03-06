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
def find(array, predicate):
    ...
    return None

# tak:
def find(array, predicate):
    ...
    raise ElementNotFound()
```

Różnica jest taka że wyjątek `ElementNotFound` w konsoli więcej mówi nam o tym co się stało niż `AttributeError: 'NoneType' object has no attribute <attribute>`.

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
    ```python
    def debug_print(self):
        # make sure that the object is correct before printing ^^
        self.name=self.name or names_generator.new_name()
        # pretty print the object
        print(f"(name=\"{name}\", size={self.size})")

    # co się teraz dzieje: obiekt zapisujemy do bazy - wychodzi bład, pole name jest nullem
    # próbujemy debugować - wszystko wydaje się być w porządku
    # w końcu ktoś przekopuje się przez kilkaset linijek kodu, żeby odnaleźć ten oto kwiatek
    
    ```
    - **Open–closed principle**
    "Software entities ... should be open for extension, but closed for modification."
    ```python
    class FileReader:
        def read():
            ...

    class BufferedFileReader(FileReader):
        def read():
            if len(self.buffer)==0:
                for i in range(self.buffer.max_size):
                    self.buffer.add(super().read())
            return self.buffer.read()
    ```
    - **Liskov substitution principle**
    "Objects in a program should be replaceable with instances of their subtypes without altering the correctness of that program." 
    ```C#
    // w dobrze napisanym kodzie obiektowym to po prostu działa,
    // więc pokażę jak to w prosty sposób zepsuć

    void Render(IPageController controller) {
        (controller as FormController).AddStringInput("email");
    }

    // ktoś przekazuje do tej metody BasicPageController 
    // (bo nigdzie nie miał napisane że nie może) i wychodzi mu błąd castowania; 
    // najprostrze rozwiązanie - typ controllera jako argument generyczny klasy

    // (w pythonie wystarczyłoby tylko wywołać tę metodę bez castowania)
    ```
    - **Interface segregation principle**
    "Many client-specific interfaces are better than one general-purpose interface."
    ```C#
    class Player : IDamagable, IItemPicker, IPushable {
    
    }

    class Box : IPushable {
    
    }

    class Worm : IDamagable, IPushable {
    
    }

    class Pickup {
        void OnEnter(IItemPicker picker){
            picker.PickItem(item);
        }
    }
    ```
    - **Dependency inversion principle**
    One should "depend upon abstractions, \[not\] concretions."
    ```C++
    // wyobraźmy sobie grę typu bullet-hell gdzie w przeciągu kilku sekund
    // pojawia się i znika kilkadziesiąt pocisków
    // klasa vector w C++ pozwala to znacząco zoptymalizować za pomocą argumentu
    // generycznego allocator - obiektu alokującego i dealokującego pamięć
    // dzięki temu można bardzo szczegółowo dobrać algorytm zarządzania pamięcią do sytuacji

    // bez tego argumentu do każdej sytuacji trzeba by było pisać całą klasę vector od nowa

    vector<Bullet, FastLinearAllocator<Bullet>> bullets;
    bullets.push_back(Bullet(x, y));
    ```
## Kapsułkowanie (Encapsulation) 
- Tworzenie publicznego interfejsu klasy i ukrywanie prywatnych pól.
- Komponenty powinny być widoczne tylko poprzez publiczny interfejs.

## Zawieranie się obiektów
```javascript
browser.currentPage.body.header.add(element)
```
Każdy element za kropką może być null'em. 
Ktoś może zmienić nazwę jednego z tych pól.
W tym momence jedna linijka mało istotnego kodu używa wiedzy o czterech warstwach struktury obiektowej programu. 
To utrudnia debugowanie i refactoring.

## Maksymalne rozbicie na metody i klasy 
- jedna funkcja robi *jedną rzecz* 
    - częstym błędem jest wykonanie jakiejś funkcjonalności klasy w jej konstruktorze, powinien on tylko ustawić ją w poprawnym stanie początkowym
    - całej funkcjonalności funkcji powinno się dać domyślić z jej nazwy
- jedna klasa ma *jedną rolę*
- warto powiedzieć sobie w myślach co robi funkcja lub klasa, zdanie które sformułujemy nie powinno być złożone. Przykłady rozbicia w zależności od użytych łączników zdań:
    - i - kompozycja
    - lub / jeżeli to - polimorfizm
    - poprzez - dziedziczenie/kompozycja/klasa pomocnicza
- użycie warstwy abstrakcji do osiągnięcia tych celów 

## Warstwy abstrakcji
Przykładowo kod routing'owy aplikacji webowej nie powinien już edytować treści strony.
Hierarchia takiej aplikacji webowej mogłaby wyglądać tak:
- Router - dopasowywanie adresów do obiektów typu Page
    - Page - logika stron
        - File - czytanie z pliku
        - TemplateBuilder - łączy dynamiczne i statyczne częsci strony
            - StringBuilder - optymalnie wykonuje operacje na zmiennych typu string
                - string - reprezentuje tekst

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
        raise NotImplementedException()

    def __getattr__(self, attr):
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
