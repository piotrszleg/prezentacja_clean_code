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

    Make().with_size(5).with_name("test").invoke()
    ``` 
- zamiana ciągu ifów/switcha na polimorfię
    ```python
    if element.type=="button":
        element.press()
    elif element.type=="radio_button":
        element.parent.select(element.index)
    elif "click" in element:
        element.click()

    # zamieniamy na:
    element.on_click()
    # gdzie różne elementy mają różne implementacje on_click
    ```
- sekcje krytyczne z punktu widzenia wydajności
    - zrozumiałe nazwy
    - komentarze a w nich:
        - ASCII art
        - linki do źródeł
        - objaśnienia
- obchodzenie bugów i quirk'ów w zewnętrznych bibliotekach 
    - komentarze
    - owijanie w przyjazne abstrakcje
- monkey patching typów bazowych, specjalne pola i inne nietypowe dodatki do języka które upraszczają kod 
  - staraj się separować tę część kodu od reszty (osobne pliki, sekcje)
  - możesz napisać czego używasz (tak aby dało się to "wygooglować") ale nie rób znowu całego wykładu (replikacja wiedzy)
- implementowanie wzorów matematycznych i fizycznych 
    - używamy własnych nazw, nie literek ze wzoru
    - przyjazne abstrakcje jak Vector3 lub Line
- modyfikacja obiektu czy utworzenie nowego (`normalized` a `Normalize()`)
- callback hell
    - typy wspierające różne operacje (np. Promise) zamiast czystych wskaźników na funkcję
    - funkcje asynchroniczne (w Pythonie i C# generatory)
    - zupełna zmiana sposobu komunikacji między obiektami (Elm)

## Wyjątki

### Programowanie defensywne

**Programowanie defensywne** doprowadzone do ekstremum prowadzi najczęsciej do programów które i tak nie działają, ale są bardzo trudne do zdebuggowania. W którymś momencie program może się w końcu wysypać, czy będzie to przepełnienie stosu, pamięci dynamicznej, błąd arytmetyczny czy w końcu nieprawidłowe działanie w świecie zewnętrznym.

Dlatego ja preferuję inne, bardziej zrównoważone podejście: programowanie tylko dla przewidzianych i mieszczących się w założeniach stanów programu i tworzenie zewnętrznego mechanizmu defensywnego, na przykład w postaci tak zwanego watchdog'a. 

### Wyjątki standardowe
Zazwyczaj istnieje grupa wyjątków które przewijają się cały czas przez dany program, często jednak wynikają one z typem rozwiązywanego problemu i użytych technik i dlatego nie są zdefiniowane przez bibliotekę standardową języka programowania. Dlatego też warto stworzyć listę takich wyjątków i konsekwentnie z nich korzystać.

Przykładem takiej listy mogą być wyjątki w kodzie źródłowym symulatora:
- UnreachablePathException
- IncorrectEnumValueException
- NoSingletonInstanceException

### Kiedy rzucać wyjątkami
Odwołałbym się teraz do SiCP: wyobraź sobie że zamiast modułu modelujesz język programowania, zastanów się które programy odrzuciłbyś z góry jako niepoprawnie sformułowane (lub wyrzucał na nich runtime exception) i jakie miało by to konsekwencje dla użytkownika. 

Przykład, znak równości w Javascript'cie z [wtfjs](https://github.com/denysdovhan/wtfjs):
```javascript
[] == ''   // -> true
[] == 0    // -> true
[''] == '' // -> true
[0] == 0   // -> true
[0] == ''  // -> false
[''] == 0  // -> true

[null] == ''      // true
[null] == 0       // true
[undefined] == '' // true
[undefined] == 0  // true

[[]] == 0  // true
[[]] == '' // true

[[[[[[]]]]]] == '' // true
[[[[[[]]]]]] == 0  // true

[[[[[[ null ]]]]]] == 0  // true
[[[[[[ null ]]]]]] == '' // true

[[[[[[ undefined ]]]]]] == 0  // true
[[[[[[ undefined ]]]]]] == '' // true
```

Ja osobiście rozwiązałbym problem powyżej wyrzuceniem wyjątku w momencie porównywania obiektów różnego typu, a w miejscach gdzie te obiekty są traktowane jako klucze łapałbym ten wyjątek i traktował jako fałsz. 

Ogólnie rzecz biorąc jasny i konkretny wyjątek wyrzucony na górze funkcji jest 100x lepszy niż jakiś `IndexOutOfBoundsException` w środku lub nawet gorzej: niepoprawnie działający program który nie zgłasza żadnych błedów.