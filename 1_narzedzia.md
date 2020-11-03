# Narzędzia

## Programy
- generatory dokumentacji
- formatery
- programy sprawdzające typy
- lintery

## Biblioteki
- pytest / inne biblioteki do testowania
- fastcore - uproszczone mokey patching i type dispatch
- dataclass - dodaje operatory i funkcje dla klas które służą jedynie przetrzymywaniu danych
- abc - definiowanie abstrakcyjnych klas 


## Funkcje jako wartości i anonimowe funkcje 

Wielu nowych programistów nie zdaje sobie sprawy z tego że funkcje mogą być traktowane jako wartości (przynajmniej w większości nowoczesnych języków programowania). To pozwala na znaczące zwiększenie możliwości parametryzowania działania funkcji i w konsekwencji lepszy *code reuse*. Możemy ich także używać do tworzenia własnych *control flow statements*, np. własnych pętli czy mechanizmów wyboru.

Praktyczny przykład:
```C#
// in Utils.cs

// calls action until it returns true or it is called tries times
// returns true if action succeded
public static bool Try(int tries, System.Func<bool> action)
    {
        while (tries > 0)
        {
            if (action()) return true;
            else tries--;
        }
        return false;
}

// in Placer.cs

using Restriction = System.Func<Placeable, bool>;

public bool Place(Placeable toPlace, Restriction restriction = null, int? maxTries = null)
{
    placed.Remove(toPlace);
    toPlace.RotateRandomly();
    return Utils.Try(maxTries.GetValueOrDefault(this.maxTries), () =>
    {
        placingArea.Place(toPlace);
        if (RestrictionSatisfied(restriction, toPlace) && !OverlapsWithAnother(toPlace))
        {
            FinalizePlacing(toPlace);
            return true;
        }
        else return false;
    });
}
```

Prosta implementacja wyrażenia switch jako funkcja w Python'ie.
```python
from enum import Enum, auto

def switch(value, options):
    return options[value]()

class UserType(Enum):
    ADMIN=auto() 
    NORMAL=auto()
    BANNED=auto()

value=UserType.ADMIN
switch(value, {
    UserType.ADMIN  : lambda: admin_console.open(),
    UserType.NORMAL : lambda: user_page.open(),
    UserType.BANNED : lambda: None
})
```

## Event'y

**Event'y** w programowaniu obiektowym najczęsciej rozumiemy jako listę funkcji do której możemy swobodnie dodawać i usuwać elementy. Następnie możemy je wszystkie naraz wywołać co powoduje kolejne wywołanie tych funkcji z danymi argumentami. Mają one ogromne zastosowanie w UI (*OnClick*, *OnHover*, etc.).

## Mix-in'y

**Mix-in'y** to innymi słowy fragmenty klas które mogą być *domieszane* do klas w trakcie ich deklaracji aby nadać im pewną funkcjonalność. Są one kwestią sporną ze względu na konflikty nazw i trudności w analizowaniu hierarchi klas które wprowadzają. W Pythonie istnieje wielokrotne dziedziczenie więc mix-in'y nie są w nim niczym niezwykłym. C# nie pozwala na mix-in'y całkowicie (można za to używać interaface'ów, kompozycji i klas statycznych). 

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

calculator.register("+", new Addition());
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

Bardzo przydatny do rozkładania skomplikowanej funkcjonalności na kawałki, rozproszenia stanu programu na moduły i ułatwienia debuggowania.

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

## Proste optymalizacje
Poniżej przedstawiam dwie optymalizacje które nie modyfikują interface'u ale pozwalają znacząco zwiększyć wydajność implementacji. 
Jest to na tyle istotne, że pozwala nam na stworzenie interface'ów które w normalnych warunkach okrutnie marnowałyby zasoby.

### Cache
Cache'ing polega on na zapamiętywaniu wyników kosztownych operacji do przyszłego użycia, co przyspiesza program kosztem zużycia pamięci.

```python
# użycie zmiennej globalnej jest tutaj dla uproszczenia
# w bibliotece powinna się też znaleźć możliwość usunięcia cache'u 
# lub jego automatyczne usuwanie

saved={
    0 : 0,
    1 : 1
}
# klucze w dict mogą być dowolnego typu
# możemy też zapisywać kilka argumentów jako krotki
def fibonacci(n):
    global saved
    if n in saved:
        return saved[n]
    else:
        result=fibonacci(n-1)+fibonacci(n-2)
        saved[n]=result
        return result

# po wywołaniu fibonacci(n) w saved
# znajdą się wszystkie wartości użyte do obliczenia n
# oraz wartość funkcji dla n
# ich obliczenie jest teraz operacją O(1)
# w przypadku typów innych niż int
# w grę wchodzi też czas ich hash'owania
```

Bardzo często możemy uprościć dodawanie optymalizacji poprzez użycie dekoratorów lub klas generycznych. 
Przykładowo biblioteka `functools` zawiera dekorator `cache` który robi dokładnie to co pokazałem na przykładzie funkcji `fibonacci`.

### Omijanie kosztownych operacji
Możemy też przyspieszać program poprzez sprawdzanie czy dana operacja jest potrzebna.

```python
class Engine:
    def set_value(value):
        if self.last_value!=value:
            # zakładamy że self.connection.send jest bardzo kosztowną operacją
            self.connection.send(f"set {self.name} {value}")
            self.last_value=value
```

Musimy tutaj ważyć trzy rzeczy:
- koszt operacji
- koszt przypisania zmiennej
- koszt pamięciowy zmiennej przetrzymującej ostatni stan
- zwiększenie się złożoności kodu źródłowego

## Strumienie

Z zewnątrz operacje na strumieniach wyglądają jak tworzenie nowych tablic z tablic źródłowych. Jednak ich właściwa implementacja polega na nakładaniu na siebie operacji a następnie (gdy nadejdzie potrzeba) iteracji po źródłowym iteratorze i przeprawodzania tych operacji na zwróconych przez niego elementach. Możliwe jest też tworzenie nieskończonych strumieni, jednak jest to raczej używane w językach funkcyjnych.

Mają one jednak kilka wad:
- mogą zmniejszać czytelność
- są trudniejsze do debuggowania
- mogą odstraszać nowych użytkowników
- wbudowane funkcje czasami zawierają pułapki

Funkcje z biblioteki standardowej:
```python
from functools import partial
from operator import mul

# jedyna alokacja tablicy w tym przykładzie
array=[1, 2, 3]

doubled=map(partial(mul, 2), array)
as_floats=map(float, doubled)

for index, element in enumerate(as_floats):
    print(f"{index}=>{element}")

```
Bardzo popularne funkcje zwracające iterable w Python'ie to również:
- `range` - zwraca kolejne liczby z zakresu
- `zip` - zszywa dwie listy w iterable z parami
- `itertools.starmap` - `map` połączone z operatorem odpakowania argumentów `*`

Z bibliotek warto sprawdzić:
- functools
- itertools
- operator

C# Linq:

```C#
using System;
using UnityEngine;
using System.Linq;

// umownie w kodzie używającym Linq używa się var
var array=new int[]{1, 2, 3};
var doubled=array.Select(x=>x*2);
var as_floats=doubled.Select(x=>(float)x);
var numbered=as_floats.Select((x, i)=>new Tuple<int, float>(i, x));

foreach(var pair in numbered) {
    Debug.Log($"{pair.Item1}=>{pair.Item2}");
}
```

Wyrażenia generatory (tylko python):
```python
array=[1, 2, 3]

doubled=(x*2 for x in array)
as_floats=(float(x) for x in doubled)

for index, element in enumerate(as_floats):
    print(f"{index}=>{element}")
```

yield w języku Python
```python
array=[1, 2, 3]

# yield pozwala na wielokrotne
# zwracanie wartości przez funkcje
# poprzez mechanizm iteracji
def transform(source):
    for x in source:
        yield float(x*2)

for index, element in enumerate(transform(array)):
    print(f"{index}=>{element}")
```

yield w języku C#
```C#
using System.Collections.Generic;

var array=new int[]{1, 2, 3};

// ważne: staramy się używać możliwie
// najbardziej ogólnych typów
IEnumerable<Tuple<int, float>> Transform(IEnumerable<int> source){
    int i=0;
    foreach(var n in source) {
        yield return new Tuple<int, float>(
            i, (float)(n*2)
        );
        i++;
    }
}

// jeżeli używamy pętli foreach 
// to nie ma potrzeby tworzyć 
// zmiennej tymczasowej na iterable
foreach(var pair in Transform(array)) {
    Debug.Log($"{pair.Item1}=>{pair.Item2}");
}
```