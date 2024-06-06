from scripts.settings import *
import pygame

# "Maybe make this class completly static, so you can call SoundManager.play(...) from everywhere." -hulah, 2024

class SoundManager:
    def __init__(self) -> None:
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        pygame.mixer.set_num_channels(64)

        self._sound_cache: dict[str, pygame.mixer.Sound]
        self._currently_playing: dict[int, pygame.mixer.Sound]

        self.__global_volume = 0.0

    @property
    def global_volume(self) -> float:
        return self.__global_volume

    @global_volume.setter
    def global_volume(self, val: float) -> None:
        self.__global_volume = max(.0, min(1., val))

    def stop_all(self) -> None:
        pygame.mixer.stop()

    def pause_all(self) -> None:
        pygame.mixer.pause()

    def resume_all(self) -> None:
        pygame.mixer.unpause()

    def play(self, sound_name: str, loop: int = 0, fade_in_time: int = 0, max_time: int = 0, volume: float | None = None) -> int:
        if sound_name not in self._sound_cache:
            s = pygame.mixer.Sound(sound_name)
            self._sound_cache[sound_name] = s
        else:
            s = self._sound_cache[sound_name]

        s.set_volume(self.__global_volume if not volume else volume)
        s.play(loops=loop, maxtime=max_time, fade_ms=fade_in_time)

        id = hash(s)
        self._currently_playing[id] = s

        return id

    def fade_sound(self, sound_id: int, fade_out_seconds: int) -> None:
        if sound_id in self._currently_playing:
            self._currently_playing[sound_id].fadeout(fade_out_seconds)

    def stop_sound(self, sound_id: int) -> None:
        if sound_id in self._currently_playing:
            self._currently_playing[sound_id].stop()
            del self._currently_playing[sound_id]
