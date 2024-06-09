from scripts.settings import *
import pygame

# "Maybe make this class completly static, so you can call SoundManager.play(...) from everywhere." -hulah, 2024
# 2024-06-06 hulahhh: Maybe there is no point in doing so since every object has a link towards the main game class, where the soundmanager instance could be
# 2024-06-06 richy: thank you hulah :heart:

if not pygame.mixer.get_init():
    pygame.mixer.pre_init(frequency=44100, size=16, channels=2, buffer=512)
    pygame.mixer.init()

if emscripten:
    pygame.mixer.SoundPatch()  # type: ignore

class SoundManager:
    def __init__(self) -> None:
        pygame.mixer.set_num_channels(64)

        self._sound_cache: dict[str, pygame.mixer.Sound] = {}
        self._currently_playing: dict[int, tuple[pygame.mixer.Channel, pygame.mixer.Sound]] = {}

        self.__global_volume = volume

        self._next_channel_id = 0

    @property
    def global_volume(self) -> float:
        return self.__global_volume

    @global_volume.setter
    def global_volume(self, val: float) -> None:
        self.__global_volume = max(.0, min(1., val))

    def stop_all(self) -> None:
        pygame.mixer.stop()
        print("Stopped all sounds")

    def pause_all(self) -> None:
        pygame.mixer.pause()
        print("Paused all sounds")

    def resume_all(self) -> None:
        pygame.mixer.unpause()
        print("Unpaused all sounds")

    def add_sound(self, sound_name: str, path: str) -> None:
        self._sound_cache[sound_name] = pygame.mixer.Sound(path)
        print(f"Loaded sound {sound_name} at {path}")

    def play(self, sound_name: str, loop: int = 0, fade_in_time: int = 0, max_time: int = 0, volume: float | None = None) -> int:
        if sound_name not in self._sound_cache:
            s = pygame.mixer.Sound(sound_name)
            self._sound_cache[sound_name] = s
        else:
            s = self._sound_cache[sound_name]

        c = pygame.mixer.Channel(self._next_channel_id)
        s.set_volume(self.__global_volume if not volume else volume)
        s.play(loop, max_time, fade_in_time)
        id = hash(s)
        self._currently_playing[id] = (c, s)

        self._next_channel_id += 1

        print(f"Playing {s}, {c}, busy? {c.get_busy()}")
        return id

    def fade_sound(self, sound_id: int, fade_out_seconds: int) -> None:
        if sound_id in self._currently_playing:
            self._currently_playing[sound_id][1].fadeout(fade_out_seconds)

    def stop_sound(self, sound_id: int) -> None:
        if sound_id in self._currently_playing:
            self._currently_playing[sound_id][1].stop()
            del self._currently_playing[sound_id]

    def update(self) -> None:
        to_delete = []

        for sound_id, (channel, sound) in self._currently_playing.items():
            if not channel.get_busy():
                self._next_channel_id -= 1
                to_delete.append(sound_id)

        for id in to_delete:
            del self._currently_playing[id]
