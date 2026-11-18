import os
import random
import tkinter as tk

from tkinter import filedialog, simpledialog, messagebox

from app_workings import (
    music_library,
    load_library,
    add_song,
    remove_song,
    play_song,
    play_next_song,
    play_previous_song,
    pause_song,
    resume_song,
    stop_song,
    check_song_finished,
    set_shuffle,
)

import pygame


class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Offline Music Player")
        self.root.geometry("650x520")
        self.root.configure(bg="#171717")

        self.shuffle = False

        load_library()

        title = tk.Label(
            root,
            text="OFFLINE MUSIC PLAYER",
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#171717",
        )
        title.pack(pady=15)

        self.song_list = tk.Listbox(
            root,
            width=65,
            height=15,
            font=("Arial", 11),
            bg="#252525",
            fg="white",
            selectbackground="#e67e22",
            activestyle="none",
        )
        self.song_list.pack(padx=20, pady=10)

        controls = tk.Frame(root, bg="#171717")
        controls.pack(pady=12)

        buttons = [
            ("Add", self.add),
            ("Remove", self.remove),
            ("Previous", self.previous),
            ("Play", self.play),
            ("Pause", self.pause),
            ("Resume", self.resume),
            ("Stop", self.stop),
            ("Next", self.next),
            ("Shuffle", self.toggle_shuffle),
        ]

        for text, command in buttons:
            tk.Button(
                controls,
                text=text,
                command=command,
                bg="#333333",
                fg="white",
                activebackground="#e67e22",
                activeforeground="white",
                relief="flat",
                padx=8,
                pady=7,
            ).pack(side="left", padx=3, pady=3)

        self.status = tk.Label(
            root, text="Ready", font=("Arial", 11), fg="#f39c12", bg="#171717"
        )
        self.status.pack(pady=10)

        self.refresh()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.check_events()

    def refresh(self):
        self.song_list.delete(0, tk.END)

        for song in music_library:
            self.song_list.insert(tk.END, f"{song[0]} - {song[1]} ({song[2]} sec)")

    def selected_index(self):
        selection = self.song_list.curselection()

        if not selection:
            messagebox.showwarning("Select Song", "Please select a song first.")
            return None

        return selection[0]

    def add(self):
        path = filedialog.askopenfilename(
            title="Choose MP3", filetypes=[("MP3 Files", "*.mp3")]
        )

        if not path:
            return

        name = simpledialog.askstring("Song Name", "Enter song name:")

        if not name:
            return

        artist = simpledialog.askstring("Artist", "Enter artist name:")

        if not artist:
            return

        try:
            duration = round(pygame.mixer.Sound(path).get_length())
        except pygame.error:
            messagebox.showerror("Audio Error", "Could not read this audio file.")
            return

        if add_song(name.strip(), artist.strip(), duration, path):
            self.refresh()
            self.status.config(text=f"Added: {name}")
        else:
            messagebox.showinfo(
                "Already Added", "This song is already in your library."
            )

    def remove(self):
        index = self.selected_index()

        if index is None:
            return

        if messagebox.askyesno("Remove Song", "Remove this song from your library?"):
            remove_song(index)
            self.refresh()
            self.status.config(text="Song removed")

    def play(self):
        index = self.selected_index()

        if index is None:
            return

        if play_song(index):
            self.status.config(text=f"Playing: {music_library[index][0]}")
        else:
            messagebox.showerror(
                "Playback Error", "Could not play this song. Check its file path."
            )

    def next(self):
        if play_next_song():
            self.update_status()
        else:
            self.status.config(text="No songs available")

    def previous(self):
        if play_previous_song():
            self.update_status()

    def pause(self):
        pause_song()
        self.status.config(text="Paused")

    def resume(self):
        resume_song()
        self.update_status()

    def stop(self):
        stop_song()
        self.status.config(text="Stopped")

    def toggle_shuffle(self):
        self.shuffle = not self.shuffle
        set_shuffle(self.shuffle)

        self.status.config(text="Shuffle ON" if self.shuffle else "Shuffle OFF")

    def update_status(self):
        from app_workings import current_song_index

        if current_song_index is not None:
            song = music_library[current_song_index]
            self.status.config(text=f"Playing: {song[0]}")

    def check_events(self):
        if check_song_finished():
            if play_next_song():
                self.update_status()
            else:
                self.status.config(text="Playback finished")

        self.root.after(100, self.check_events)

    def close(self):
        stop_song()
        pygame.mixer.quit()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
