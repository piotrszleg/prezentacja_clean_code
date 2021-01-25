# Wyjątki

## Programowanie defensywne

**Programowanie defensywne** doprowadzone do ekstremum prowadzi najczęsciej do programów które i tak nie działają, ale są bardzo trudne do zdebuggowania. W którymś momencie program może się w końcu wysypać, czy będzie to przepełnienie stosu, pamięci dynamicznej, błąd arytmetyczny czy w końcu nieprawidłowe działanie w świecie zewnętrznym.

Dlatego ja preferuję inne, bardziej zrównoważone podejście: programowanie tylko dla przewidzianych i mieszczących się w założeniach stanów programu i tworzenie zewnętrznego mechanizmu defensywnego, na przykład w postaci tak zwanego watchdog'a. 

## Wyjątki standardowe
Zazwyczaj istnieje grupa wyjątków które przewijają się cały czas przez dany program, często jednak wynikają one z typu rozwiązywanego problemu i użytych technik i dlatego nie są zdefiniowane przez bibliotekę standardową języka programowania. Dlatego też warto stworzyć listę takich wyjątków i konsekwentnie z nich korzystać.

Przykładem takiej listy mogą być wyjątki w kodzie źródłowym symulatora:
- UnreachablePathException
- IncorrectEnumValueException
- NoSingletonInstanceException

### Kiedy rzucać wyjątkami
Odwołałbym się teraz do SiCP: wyobraź sobie że zamiast modułu modelujesz język programowania, zastanów się które programy odrzuciłbyś z góry jako niepoprawnie sformułowane (lub wyrzucał na nich runtime exception) i jakie miało by to konsekwencje dla użytkownika. 

Przykład, znęcanie się nad znakiem równości w Javascript'cie z [wtfjs](https://github.com/denysdovhan/wtfjs):
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

# Tworzenie obiektów wyjątków
Typy wyjątków w dużych projektach powinny je dzielić na kategorie. W małych projektach jest sens używać `ValueError`, jednak im są one większe tym bardziej istotny jest ich sensowny podział.

Jeżeli takich wyjątków jest dużo to można się zdecydować na stworzenie bardzo specyficznych wyjątków np. na stworzenie `EmptyDictionaryError` czy `ListSizeNotPowerOfTwo`.

Oczywiście kluczowe są błędy typowe dla domeny, np.: `EngineLocked`.

Wiadmość przekazywana w argumencie do konstruktora do wyjątku powinna umożliwić zrozumienie błędu bez czytania kodu źródłówego. Można też w niej przekazać dodatkowe wskazówki na temat możliwego powodu błędu.

Jedyną cechą kategoryzującą wyjątki jest to, że mogą być rzucane i łapane. Jeżeli jest taka potrzeba to możemy w ich środku równie dobrze umieścić ilustracje czy stan systemu w momencie wystąpienia. Mechanizmu `raise-except` można także używać w niestandardowy sposób, na przykład do szybkiego wychodzenia z sekcji programu czy sygnalizowania że do wykonania zadania powinno się użyć innego modułu. Oczywiście im więcej *namieszamy* tym gorzej dla osób zaznajamiających się z projektem.