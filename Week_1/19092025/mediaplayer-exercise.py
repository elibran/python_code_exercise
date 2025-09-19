# 1. Base MediaFile Class
class MediaFile:
    def __init__(self, title, duration):
        self.title = title
        self.duration = duration

    def play(self):
        print("Playing generic media...")

    # Operator Overloading for str() and print()
    def __str__(self):
        return f"Title: {self.title}, Duration: {self.duration}s"

# 2. Child Classes with Method Overriding
class AudioFile(MediaFile):
    def play(self):
        """Overrides the parent's play method."""
        print(f"🎵 Playing audio: {self.title}")

class VideoFile(MediaFile):
    def play(self):
        """Overrides the parent's play method."""
        print(f"🎬 Playing video: {self.title} with resolution 1080p")

# 3. Playlist Class
class Playlist:
    def __init__(self, name):
        self.name = name
        self.files = []

    def add_file(self, file):
        if isinstance(file, MediaFile):
            self.files.append(file)
        else:
            print("Error: Can only add MediaFile objects to a playlist.")

    # Operator Overloading for the '+' operator
    def __add__(self, other):
        if isinstance(other, Playlist):
            new_name = f"{self.name} & {other.name} Mix"
            new_playlist = Playlist(new_name)
            # Combine the file lists
            new_playlist.files = self.files + other.files
            return new_playlist
        else:
            # Return NotImplemented to indicate the operation is not supported
            return NotImplemented

    # 4. Method to Demonstrate Duck Typing
    def play_all(self):
        print(f"--- Starting Playlist: {self.name} ---")
        for file in self.files:
            # This is Duck Typing in action.
            # We don't check if file is AudioFile or VideoFile.
            # We just trust that it has a .play() method.
            file.play()

# --- Testing ---
song1 = AudioFile("Bohemian Rhapsody", 355)
song2 = AudioFile("Stairway to Heaven", 482)
video1 = VideoFile("The Matrix Trailer", 150)

playlist1 = Playlist("Rock Classics")
playlist1.add_file(song1)
playlist1.add_file(song2)

playlist2 = Playlist("Movie Clips")
playlist2.add_file(video1)

# Test __str__
print(song1)
print(video1)
print("-" * 20)

# Test Operator Overloading (+)
combined_playlist = playlist1 + playlist2
print(f"Created new playlist: {combined_playlist.name}")

# Test Duck Typing by playing all files
print("-" * 20)
combined_playlist.play_all()