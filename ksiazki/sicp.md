# Structure and Interpretation of Computer Programs
## Konsekwencje ręcznego zarządzania stanem programu
Powiedzmy że mamy grę w stylu Minecraft'a z nieskończonym światem, w którym gdy raz odwieziliśmy miejsce pozostaje ono takie samo.

Tworzymy więc obiekty chunk'i które używają swojej pozycji w świecie jako seed do generatora liczb losowych na czas tworzenia swoich elementów.
```C#
// w metodzie Chunk.Start:
Random.seed=gridPosition.GetHashCode();

// metoda Player.Start również ustawia seed:
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
- Czy nazwy twoich funkcji i typów pozwalają czytać twój program jak gdyby był on instrukcją rozwiązania problemu w języku naturalnym?
- Czy typ który stworzyłeś byłby użyteczny i łatwy do zrozumienia gdyby istniał w bibliotece standardowej?
- Czy twój kod użwający callback'ów wyraża kolejność działań?
- Czy twoje wybory rozwiązań są intuicyjne?
- Czy na użytkowników twoich klas oraz osób implemetujących stworzone przez ciebie interfejsy i klasy abstrakcyjne czekają pułapki?
