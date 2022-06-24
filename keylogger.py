#!/usr/bin/env python3

from pynput import keyboard
from time import perf_counter
from threading import Thread, enumerate
from queue import Queue
        
class KeyEvent():
    def __init__(self, key, time):
            self.key = key
            self.time = time

class KeyLogger:
    def __init__(self, max_repetitions, target_string):
        self.max_repetitions = max_repetitions
        self.repetition = 0
        self.down_key_events = [[] for _ in range(max_repetitions)]
        self.up_key_events   = [[] for _ in range(max_repetitions)]
        self.user_input = ''
        self.target_string = target_string
        self.running = False
        self.on_down_events = Queue()
        self.on_up_events = Queue()
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release, suppress=True)
        self.worker = Thread(target=self.process_keys)

    def process_keys(self):

        while self.thread_running:
            while self.running is True:
                key_event = self.on_down_events.get()
                if key_event == False:
                    self.thread_running = False
                    self.on_down_events.task_done()
                    break
                self.on_press_do(key_event)
                self.on_down_events.task_done()
                key_event = self.on_up_events.get()
                self.on_release_do(key_event)
                self.on_up_events.task_done()
        print('[!] Stopping worker thread...')
            

    def on_press(self, key):
        
        if key == keyboard.Key.esc:
            print('[!] Stopping listener thread...')
            #signals worker thread to stop
            self.on_down_events.put(False)
            # Stop listener
            return False
        
        if not self.running and key == keyboard.Key.space:
            print("\nTest starting....")
            print(f"Please type: {self.target_string}")
        else:
            self.on_down_events.put(KeyEvent(key, perf_counter()))

    def on_release(self, key):
        if not self.running and key == keyboard.Key.space:
            self.running = True
        else:
            self.on_up_events.put(KeyEvent(key, perf_counter()))

    def on_press_do(self, event):
        if self.running:   
            if hasattr(event.key, 'char'):
                print(event.key.char.strip(), end='', flush=True)
                self.user_input += event.key.char
                self.down_key_events[self.repetition].append(event.time)
            if self.user_input == self.target_string and event.key == keyboard.Key.enter:
                self.down_key_events[self.repetition].append(event.time)
            

    def on_release_do(self, event):
        if self.running:
            if hasattr(event.key, 'char'):
                if self.target_string.startswith(self.user_input):
                    self.up_key_events[self.repetition].append(event.time)
                else:
                    print(f'\nBad input {self.user_input}, please enter {self.target_string}\n')
                    self.down_key_events[self.repetition] = []
                    self.up_key_events[self.repetition] = []
                    self.user_input = ''

            elif event.key == keyboard.Key.enter:
                if self.user_input == self.target_string:
                    self.up_key_events[self.repetition].append(event.time)
                    self.repetition += 1
                    
                    if self.repetition < self.max_repetitions:
                        print(f'\n{self.repetition}/{self.max_repetitions}')
                        print(f'Please type {self.target_string}')
                    else:
                        print(f'\n{self.repetition}/{self.max_repetitions}')
                        print('\n[!] Cleaning up...')
                        self.running = False
                        self.listener.stop()
                        print('[!] Press any button to finish test...')
                else:
                    print(f'\nBad input {self.user_input}, please enter {self.target_string}\n')
                    self.down_key_events[self.repetition] = []
                    self.up_key_events[self.repetition] = []
                
                self.user_input = ''

                        


    def start(self):
        
        self.thread_running = True
        self.worker.setDaemon(True)
        self.worker.start()
        
        self.listener.start()
        self.listener.join()




