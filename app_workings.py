import json
import random
import os
import pygame

from tkinter import filedialog

pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_endevent(pygame.USEREVENT)

LIBRARY_FILE = "music_library.json"

music_library = []
current_song_index = None
shuffle_enabled = False


def select_song_file():
    return filedialog.askopenfilename(
        title="Select a Song", filetypes=[("MP3 Files", "*.mp3")]
    )


def show_songs():
    for index, song in enumerate(music_library, start=1):
        print(f"{index}. {song[0]} by {song[1]}")


def add_song(song_name, artist_name, duration, song_path):
    for song in music_library:
        if song[3] == song_path:
            return False

    music_library.append([song_name, artist_name, duration, song_path])

    save_library()
    return True


def remove_song(index):
    global current_song_index

    if not 0 <= index < len(music_library):
        return False

    if current_song_index == index:
        stop_song()
        current_song_index = None
    elif current_song_index is not None and current_song_index > index:
        current_song_index -= 1

    music_library.pop(index)
    save_library()
    return True


def save_library():
    with open(LIBRARY_FILE, "w", encoding="utf-8") as file:
        json.dump(music_library, file, indent=4)


def load_library():
    try:
        with open(LIBRARY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            music_library.clear()
            music_library.extend(
                song
                for song in data
                if isinstance(song, list)
                and len(song) == 4
                and isinstance(song[3], str)
            )

    except FileNotFoundError, json.JSONDecodeError:
        music_library.clear()


def play_song(song_index):
    global current_song_index

    if not 0 <= song_index < len(music_library):
        return False

    song_path = music_library[song_index][3]

    if not os.path.isfile(song_path):
        return False

    try:
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        current_song_index = song_index
        return True
    except pygame.error:
        return False


def pause_song():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()


def resume_song():
    pygame.mixer.music.unpause()


def stop_song():
    pygame.mixer.music.stop()


def play_next_song():
    if not music_library:
        return False

    if shuffle_enabled and len(music_library) > 1:
        choices = [i for i in range(len(music_library)) if i != current_song_index]
        next_index = random.choice(choices)
    else:
        next_index = (
            (current_song_index + 1) % len(music_library)
            if current_song_index is not None
            else 0
        )

    return play_song(next_index)


def play_previous_song():
    if not music_library:
        return False

    previous_index = (
        (current_song_index - 1) % len(music_library)
        if current_song_index is not None
        else 0
    )

    return play_song(previous_index)


def set_shuffle(enabled):
    global shuffle_enabled
    shuffle_enabled = enabled


def check_song_finished():
    finished = False

    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            finished = True

    return finished


if __name__ == "__main__":
    print("Run project_spotify.py to start the music player.")
