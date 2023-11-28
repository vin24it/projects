import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pygame
import os
import time

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title('Python Music Player')

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=False, fill='both')

        self.current_song_label = tk.Label(self.main_frame, text='No song playing')
        self.current_song_label.pack(side=tk.TOP, pady=10, fill='both')

        self.time_spam_label = tk.Label(self.main_frame, text='Total: 0:00 | Remaining: 0:00')
        self.time_spam_label.pack(side=tk.TOP, pady=5, fill='both')

        self.next_song_label = tk.Label(self.main_frame, text='Next: None')
        self.next_song_label.pack(side=tk.TOP, pady=5, fill='both')

        # Rearranged the placement of the progress bar below the next song label
        self.progress_bar = ttk.Progressbar(self.main_frame, orient='horizontal', length=300, mode='determinate')
        self.progress_bar.pack(side=tk.TOP, pady=5, fill='both', padx=10)

        button_params = {'padx': 10, 'pady': 5, 'height': 2}

        self.play_pause_button = tk.Button(self.main_frame, text='Play', command=self.play_pause_song, **button_params)
        self.play_pause_button.pack(side=tk.LEFT, expand=True, fill='both', padx=5)

        self.previous_button = tk.Button(self.main_frame, text='Previous', command=self.previous_song, **button_params)
        self.previous_button.pack(side=tk.LEFT, expand=True, fill='both', padx=5)

        self.next_button = tk.Button(self.main_frame, text='Next', command=self.next_song, **button_params)
        self.next_button.pack(side=tk.LEFT, expand=True, fill='both', padx=5)

        self.list_songs_button = tk.Button(self.main_frame, text='List Songs', command=self.list_songs, **button_params)
        self.list_songs_button.pack(side=tk.LEFT, expand=True, fill='both', padx=5)

        pygame.mixer.init()

        self.current_song_index = 0
        self.song_list = []
        self.start_time = 0
        self.paused_time = 0
        self.total_duration = 0
        self.update_elapsed_time()

    def play_pause_song(self):
        if pygame.mixer.music.get_busy():
            if self.paused_time == 0:
                self.paused_time = time.time() - self.start_time
            pygame.mixer.music.pause()
            self.play_pause_button.config(text='Play')
        else:
            if self.paused_time > 0:
                self.start_time = time.time() - self.paused_time
            pygame.mixer.music.unpause()
            self.play_pause_button.config(text='Pause')
            self.update_elapsed_time()

    def stop_song(self):
        pygame.mixer.music.stop()
        self.play_pause_button.config(text='Play')
        self.start_time = 0
        self.paused_time = 0
        self.update_elapsed_time()

    def next_song(self):
        if self.song_list:
            self.current_song_index = (self.current_song_index + 1) % len(self.song_list)
            self.load_and_play_song()
            self.update_next_song_label()

    def previous_song(self):
        if self.song_list:
            self.current_song_index = (self.current_song_index - 1) % len(self.song_list)
            self.load_and_play_song()
            self.update_next_song_label()

    def load_and_play_song(self):
        if self.song_list:
            song_path = self.song_list[self.current_song_index]
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            song_name = os.path.basename(song_path)
            self.current_song_label.config(text=f'Now playing: {song_name}')
            if self.paused_time == 0:
                self.start_time = time.time()
                self.total_duration = pygame.mixer.Sound(song_path).get_length()
                self.progress_bar['maximum'] = self.total_duration  # Set the maximum value of the progress bar
                self.update_elapsed_time()
            else:
                self.update_elapsed_time()

    def update_next_song_label(self):
        if self.song_list:
            next_song_index = (self.current_song_index + 1) % len(self.song_list)
            next_song_path = self.song_list[next_song_index]
            next_song_name = os.path.basename(next_song_path)
            self.next_song_label.config(text=f'Next: {next_song_name}')
            self.root.after(100, lambda: self.update_next_song_label_remaining_time(next_song_path))

    def update_next_song_label_remaining_time(self, next_song_path):
        next_song_duration = pygame.mixer.Sound(next_song_path).get_length()
        remaining_time = max(0, next_song_duration - self.paused_time)
        remaining_time_str = self.format_time(remaining_time)
        self.time_spam_label.config(text=f'Total: {self.format_time(self.total_duration)} | Remaining: {remaining_time_str}')

    def list_songs(self):
        file_paths = filedialog.askopenfilenames(
            title='Select MP3 Files',
            filetypes=[("MP3 files", "*.mp3")],
        )
        if file_paths:
            self.song_list = list(file_paths)
            if self.song_list:
                self.current_song_index = 0
                self.load_and_play_song()
                self.update_next_song_label()

    def update_elapsed_time(self):
        if pygame.mixer.music.get_busy():
            elapsed_time = pygame.mixer.music.get_pos() / 1000  # Get current position in seconds

            if self.paused_time > 0:
                elapsed_time += self.paused_time

            remaining_time = max(0, self.total_duration - elapsed_time)
            elapsed_time_str = self.format_time(elapsed_time)
            remaining_time_str = self.format_time(remaining_time)

            self.time_spam_label.config(text=f'Total: {self.format_time(self.total_duration)} | Remaining: {remaining_time_str}')

            self.progress_bar['value'] = elapsed_time  # Update the progress bar value

            if elapsed_time < self.total_duration:
                self.root.after(1000, self.update_elapsed_time)  # Update every 1 second

    def format_time(self, time_in_seconds):
        minutes, seconds = divmod(int(time_in_seconds), 60)
        return f'{minutes}:{seconds:01}'

if __name__ == '__main__':
    root = tk.Tk()
    music_player = MusicPlayer(root)
    root.mainloop()
