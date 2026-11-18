import unittest
from app_workings import add_song
from app_workings import show_songs_in_playlist
from app_workings import remove_song_from_playlist
from app_workings import music_library
from app_workings import add_playlist
from app_workings import show_playlists
import io
from contextlib import redirect_stdout


class Testmusiclibrary(unittest.TestCase):
    def setUp(self):
        music_library.clear()
        music_library["workout"] = [
            ["believer", "imagine dragons", 204],
            ["radioactive", "imagine dragons", 186],
        ]

    def test_add_song(self):
        expected_length = len(music_library["workout"])
        add_song("workout", "as", "sa", 213)
        expected_length += 1
        add_song("workout", "as", "sa", 213)
        self.assertEqual(len(music_library["workout"]), expected_length)

    def test_remove_song(self):
        expected_length = len(music_library["workout"])
        remove_song_from_playlist("workout", "believer", "imagine dragons")
        expected_length -= 1
        self.assertEqual(len(music_library["workout"]), expected_length)
        self.assertEqual(music_library["workout"][0][0], "radioactive")

    def test_remove_nonexistent_song(self):
        expected_length = len(music_library["workout"])
        remove_song_from_playlist("workout", "faded", "alan walker")
        self.assertEqual(len(music_library["workout"]), expected_length)
        self.assertEqual(music_library["workout"][0][0], "believer")
        self.assertEqual(music_library["workout"][1][0], "radioactive")

    def test_add_playlist(self):
        expected_len = len(music_library.keys())
        add_playlist("chill")
        expected_len += 1
        result = music_library["chill"]
        self.assertEqual(len(music_library.keys()), expected_len)
        self.assertEqual(result, [])

    def test_duplicate_playlist(self):
        expected_len = len(music_library.keys())
        expected_playlist = [
            ["brittle", "chango", 234],
            ["life", "chance", 234],
            ["love me more", "change", 234],
        ]
        add_playlist("chill")
        expected_len += 1
        add_song("chill", "brittle", "chango", 234)
        add_song("chill", "life", "chance", 234)
        add_song("chill", "love me more", "change", 234)
        add_playlist("chill")
        self.assertEqual(len(music_library.keys()), expected_len)
        self.assertEqual(music_library["chill"], expected_playlist)

    def test_show_songs_in_existing_playlist(self):
        expected_output = "\nSongs in workout playlist:\n1. believer by imagine dragons, duration: 204 seconds\n2. radioactive by imagine dragons, duration: 186 seconds\n"
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            show_songs_in_playlist("workout")
        result = captured_output.getvalue()
        self.assertEqual(result, expected_output)

    def test_show_songs_in_empty_playlist(self):
        add_playlist("study")
        captured_output2 = io.StringIO()
        with redirect_stdout(captured_output2):
            show_songs_in_playlist("study")
        result2 = captured_output2.getvalue()
        self.assertEqual(result2, "study playlist is empty.\n")

    def test_show_songs_in_non_existing_playlist(self):
        captured_output3 = io.StringIO()
        with redirect_stdout(captured_output3):
            show_songs_in_playlist("go")
        result3 = captured_output3.getvalue()
        self.assertEqual(result3, "Playlist not found\n")

    def test_show_existing_playlists(self):
        expected_output = "1. workout\n"
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            show_playlists()
        result = captured_output.getvalue()
        self.assertEqual(result, expected_output)

    def test_show_nonexisting_playlists(self):
        expected_output = "No playlists available.\n"
        music_library.clear()
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            show_playlists()
        result = captured_output.getvalue()
        self.assertEqual(result, expected_output)

    def test_show_multiple_playlists(self):
        expected_output = "1. workout\n2. chill\n"
        add_playlist("chill")
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            show_playlists()
        result = captured_output.getvalue()
        self.assertEqual(result, expected_output)
