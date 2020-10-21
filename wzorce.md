# Metody organizacji i wzorce projektowe

## Funkcje jako wartości i anonimowe funkcje 

Wielu nowych programistów nie zdaje sobie sprawy z tego że funkcje mogą być traktowane jako wartości (w większości nowoczesnych języków programowania). To pozwala na znaczące zwiększenie możliwości parametryzowania działania funkcji i w konsekwencji lepszy *code reuse*. Możemy ich także używać do tworzenia własnych *control flow statements*, np. własnych pętli czy mechanizmów wyboru.

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
public bool Place(Placeable toPlace, System.Func<Placeable, bool> restriction=null)
{
    placed.Remove(toPlace);
    toPlace.RotateRandomly();
    return Utils.Try(maxTries, () =>
    {
        placingArea.Place(toPlace);
        bool restrictionSatisifed = restriction == null || !restriction(toPlace);
        if (restrictionSatisifed && !OverlapsWithAnother(toPlace))
        {
            placed.Add(toPlace);
            toPlace.placer = this;
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

**Event'y** najczęsciej rozumiemy jako listę funkcji do której możemy swobodnie dodawać i usuwać elementy. Następnie możemy je wszystkie naraz wywołać co powoduje kolejne wywołanie tych funkcji z danymi arguemntami. Mają one ogromne zastosowanie w UI (*OnClick*, *OnHover*, etc.).

## Mix-in'y

**Mix-in'y** to innymi słowy fragmenty klas które mogą być *domieszane* do klas w trakcie ich deklaracji aby nadać im pewną funkcjonalność. Są one kwestią sporną ze względu na konflikty nazw i trudności w analizowaniu hierarchi klas które wprowadzają. W Pythonie istnieje wielokrotne dziedziczenie więc mix-in'y nie są w nim niczym niezwykłym. C# nie pozwala na mix-in'y całkowicie (można za to używać kompozycji i klas statycznych). 

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