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

Czujniki z taką pseudo-węgierską notacją mówiącą o zwracanej wartości jak na przykład:
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

silnki
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
            self.push_task(subtask)

    def control_returned(self):
        for subtask in subtasks:
            if not subtask_succeded:
                self.fail()
        self.succeed()

class GoForwardUntilHoveringOver(Task):
    def __init__(controller, target):
        super().__init__(controller)
        self.target=target

    def start(self):
        self.vision.set_target(self.target)
        self.saved_camera=self.camera_selector.selected
        self.camera_selector.select(Camera.BOTTOM)
        self.movement=Vector3.FORWARD*MAX_SPEED

    def update(self):
        if self.collision_detector.has_value:
            self.fail()
        if self.vision.has_value:
            self.succeed()

    def cleanup(self):
        self.camera_selector.select(self.saved_camera)
        self.movement=Vector3.ZERO
```

## Konfiguracja
Myślę że Python jest wystarczająco ekspresyjnym i prostym językiem aby można w nim było zapisywać całą konfigurację.

Co chciałbym jednak zmienić to rozbicie na podpliki. Unikałbym tworzenia sztucznych przestrzeni nazw przy użyciu klas ponieważ utrudniają one czytelność i importowanie. Dzięki temu będziemy mogli importować stałe w ten sposób `from config.model.movement import SPEED` ze wszystkimi zaletami statystycznej weryfikacji kodu.