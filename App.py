from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import cv2
from bluetooth import *
import struct


class MouseApp(App):
    def build(self):
        self.capture = cv2.VideoCapture(0)
        _, self.prev_frame = self.capture.read()
        self.prev_gray = cv2.cvtColor(self.prev_frame, cv2.COLOR_BGR2GRAY)

        self.sock = BluetoothSocket(RFCOMM)
        self.sock.connect(('your_computer_bt_address', 1))

        layout = BoxLayout(orientation='vertical')
        start_button = Button(text='Start', on_press=self.start_mouse)
        stop_button = Button(text='Stop', on_press=self.stop_mouse)
        layout.add_widget(start_button)
        layout.add_widget(stop_button)

        return layout

    def start_mouse(self, instance):
        Clock.schedule_interval(self.send_movement, 1 / 30)

    def stop_mouse(self, instance):
        Clock.unschedule(self.send_movement)

    def send_movement(self, dt):
        _, frame = self.capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        flow = cv2.calcOpticalFlowFarneback(
            self.prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        flow_x, flow_y = flow[..., 0], flow[..., 1]

        dx, dy = int(flow_x.mean()), int(flow_y.mean())
        data = struct.pack('2i', dx, dy)
        self.sock.sendall(data)

        self.prev_gray = gray.copy()

    def on_stop(self):
        self.capture.release()
        self.sock.close()


if __name__ == '__main__':
    MouseApp().run()
