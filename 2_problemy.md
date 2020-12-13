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
    # jeżeli funkcjonalność "nie pasuje" do obiektu można użyć
    # techniki type dispatch (functools.singledispatch)
    ```

- callback hell
    - modularyzacja
    - ekstrakcja funkcji używanych jako callbacki
    - typy wspierające różne operacje (np. Promise) zamiast czystych wskaźników na funkcję
    - funkcje asynchroniczne (w Pythonie i C# generatory)
    - zupełna zmiana sposobu komunikacji między obiektami (Elm)
    - przykład:
    ```js
    // src: http://callbackhell.com/
    fs.readdir(source, function (err, files) {
        if (err) {
            console.log('Error finding files: ' + err)
        } else {
            files.forEach(function (filename, fileIndex) {
            console.log(filename)
            gm(source + filename).size(function (err, values) {
                if (err) {
                console.log('Error identifying file size: ' + err)
                } else {
                console.log(filename + ' : ' + values)
                aspect = (values.width / values.height)
                widths.forEach(function (width, widthIndex) {
                    height = Math.round(width / aspect)
                    console.log('resizing ' + filename + 'to ' + height + 'x' + height)
                    this.resize(width, height).write(dest + 'w' + width + '_' + filename, function(err) {
                    if (err) console.log('Error writing file: ' + err)
                    })
                }.bind(this))
                }
            })
            })
        }
    })
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
  - możesz napisać czego używasz (tak aby dało się to "wygooglować") ale nie rób znowu całego wykładu (bo jest to swego rodzaju replikacja wiedzy)
- implementowanie wzorów matematycznych i fizycznych 
    - używamy własnych nazw, nie literek ze wzoru
    - przyjazne abstrakcje jak Vector3 lub Line
- modyfikacja obiektu czy utworzenie nowego (`normalized` a `Normalize()`)
- aplikacje czasu rzeczywistego 
    - event'y
    - funkcje asynchroniczne
    - rozbicie na parametryzowalne i niezależne moduły
    - interfejsy dyktowane logiką programu a nie detalami implementacji
    ```python
    # nie
    def set_target(self, target):
        self.target=target

    def approach(self, engine):
        ...
        return finished

    # wywołanie funkcji
    self.set_target("gate")
    while self.approach(engine):
        sleep(10)
        self.update_camera()
        pass
    
    # tak
    async def approach_target(self, target):
        ...
        return success

    self.approach_target(target)

    # Możliwość stworzenia przejrzystych interfejsów mocno zależy
    # od możliwości języka oraz pozostałych klas i funkcji w projekcie.
    ```