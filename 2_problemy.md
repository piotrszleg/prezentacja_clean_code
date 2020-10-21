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
    - komentarze a w nich ASCII art, linki, objaśnienia
    - zrozumiałe nazwy
- obchodzenie bugów i quirk'ów w zewnętrznych bibliotekach 
    - komentarze
    - owijanie w przyjazne abstrakcje
- monkey patching typów bazowych, specjalne pola i inne nietypowe dodatki do języka które upraszczają kod 
  - staraj się separować tę część kodu od reszty (osobne pliki, sekcje)
  - możesz napisać czego używasz (tak aby dało się to "wygooglować") ale nie rób znowu całego wykładu bo to replikacja wiedzy
- implementowanie wzorów matematycznych i fizycznych 
    - używamy własnych nazw, nie literek ze wzoru
    - przyjazne abstrakcje jak Vector3 lub Line
- modyfikacja obiektu czy utworzenie nowego (`normalized` a `Normalize()`)
- callback hell
    - typy wspierające różne operacje (np. Promise) zamiast czystych wskaźników na funkcję
    - funkcje asynchroniczne (w pythonie generatory)
    - zupełna zmiana sposoby komunikacji między obiektami (Elm)
