from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.graphics import Color, Rectangle
import simpleaudio as sa
from course import Course


class SpellingWidget(BoxLayout):
    N = 60
    K = 50
    font_size = 40
    total_errors = NumericProperty(0)
    current_errors = NumericProperty(0)
    correct = NumericProperty(0)
    lesson_time = NumericProperty(0)
    index = NumericProperty(0)

    def __init__(self, **kwargs):
        super(SpellingWidget, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        for i in range(self.N):
            self.ids['input'].add_widget(Label(font_name='arial', font_size=self.font_size))
            self.ids['reference'].add_widget(Label(font_name='arial', font_size=self.font_size))
        self.input = self.ids['input'].children
        self.reference = self.ids['reference'].children

        self.sound_right = sa.WaveObject.from_wave_file('resources/pop1.wav')
        self.sound_wrong = sa.WaveObject.from_wave_file('resources/incorrect1.wav')
        self.sound_finished = sa.WaveObject.from_wave_file('resources/kolhakavod_noomi.wav')

        self.course = Course('hebrew')
        self.lesson_number = 0
        self.index = 1
        self.index = 0
        self.reference_length = 0

        self._reset_lesson()

    def _set_reference_text(self, text):
        text = text.replace(' ', '_')
        for i in range(self.N):
            self.reference[i].text = ''
            self.input[i].text = ''
        for i, letter in enumerate(text):
            self.reference[i].text = letter
        self.reference_length = len(text)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print(f'keycode = {keycode}')

        if len(keycode[1])>1:
            if keycode[1] not in ['backspace', 'spacebar']:
                return True

        if text==' ':
            text='_'

        if keycode[1] == 'backspace':
            if self.index > 0:
                self.index -= 1
                if self.input[self.index].text == self.reference[self.index].text:
                    self.correct -= 1
                else:
                    self.current_errors -= 1
                self.input[self.index].text = ''
        else:
            self.index +=1
            self.input[self.index-1].text = text
            if text == self.reference[self.index-1].text:
                self.correct += 1
                self.sound_right.play()
            else:
                self.total_errors += 1
                self.current_errors += 1
                self.sound_wrong.play()

        if self.index == self.reference_length:
            if self.current_errors==0:
                self.sound_finished.play()
            self.course.update(self.current_errors, self.total_errors, self.correct)
            self._reset_lesson()

        return True

    def _reset_lesson(self):
        self._set_reference_text(self.course.generate(self.K))
        self.current_errors = 0
        self.total_errors = 0
        self.correct = 0
        while self.index>0:
            self.index -= 1

    def on_index(self, *args):
        height = self.font_size
        width = self.font_size/2
        with self.canvas:
            if self.index>0:
                Color(0,0,0,1)
                p = self.input[self.index-1].center
                Rectangle(pos=[p[0]-width/2, p[1]-1.1*height], size=[width, height/2])
            Color(0,0,1,1)
            p = self.input[self.index].center
            Rectangle(pos=[p[0]-width/2, p[1]-1.1*height], size=[width, height/2])
            Color(0,0,0,1)
            p = self.input[self.index+1].center
            Rectangle(pos=[p[0]-width/2, p[1]-1.1*height], size=[width, height/2])


class PongApp(App):
    def build(self):
        return SpellingWidget()


if __name__ == "__main__":
    # Window.fullscreen = True
    PongApp().run()
