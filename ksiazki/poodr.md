# Practical Object-Oriented Design in Ruby

Książka przechodzi przez stworzenie i refaktoryzację oprogramowania wypożyczalni rowerów napisanej w Ruby'm pokazując różne techniki projektowania i naprawy kodu. Duża część książki jest poświęcona na efektywnym i bezpiecznym korzystaniu z języków dynamicznych (do których należy Python).

Inne tematy o któe poszerza materiał z Clean Code:

- stopniowy refactoring i ważene kosztu refactoringu z zyskami
- zamiana polimorfii na kompozycję przy użyciu komponentów (_Composition over inheritance_)
- testowanie przynależności obiektu do interfejsu

## Grafy powiązań i ich analizowanie

Wydaje mi się że w tej książce były znacznie częściej używane niż w Clean Code.

[UML Reference](https://creately.com/blog/diagrams/class-diagram-relationships/)

Przykład dwóch popularnych struktur rozrysowanych na takie grafy:

```java
// Oznaczenie: A->B - klasa A jest zależne od klasy B.

// Calkulator używa klas TextInput i Button
// i bez nich nie może istnieć.
// Ale juz TextInput i Button są zupełnie niezależnymi od niego klasami
// i mogą być używane i testowane oddzielnie.
// Taki związek osiąga się zazwyczaj używając tzw. event'ów (OnClick, OnChange).
   
   Calculator
      / \
     /   \
    /     \
   ↓       ↓
  Text   Button
 Input


// Pandoc to aplikacja która bierze za argumenty nazwę pliku wejściowego i wyjściowego 
// i zamienia dokument z jednego typu inny, np. html na pdf.
// Zawiera ona różne obiekty przekształcające pliki, każdy jest w stanie stwierdzić czy
// obsługuje daną konwersję i ją przeprowadzić.
// W języku obeiktowym Transformer byłby interfejsem 
// a Pandoc to klasą zawierającą listę obiektów przynależących do tego interfejsu. 

// Konieczny byłby też jakiś mechanizm ładowania tych obiektów, 
// np.: przez iterację plików w folderze, xml lub metodę register.

     Pandoc
       ↓
   Transformer


  Transformer
       ↑
      / \
     /   \
    /     \
   /       \
MD_HTML  HTML_PDF

```
