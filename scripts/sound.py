from scripts.globals import VOLUME, IS_PYGBAG
import pygame
import pathlib

if not pygame.mixer.get_init():
    pygame.mixer.pre_init(frequency=44100, size=16, channels=2, buffer=512)
    pygame.mixer.init()
    pygame.mixer.set_num_channels(64)

if IS_PYGBAG:
    pygame.mixer.SoundPatch()  # type: ignore -> for web


class BGMManager:
    """
    for background music only, since it uses less resources
    """

    def __init__(self) -> None:
        self._bgm_cache: dict[str, pathlib.Path] = {}
        self._currently_playing: str | None = None
        self.volume: float = 0
        self.set_volume(VOLUME)

        print("Initialized BGM manager")

    def set_volume(self, val: float) -> None:
        self.volume = max(0, min(1, val))
        pygame.mixer.music.set_volume(val)

    def add_music(self, name: str, path: pathlib.Path | None = None) -> None:
        if name in self._bgm_cache and path == None:
            path = self._bgm_cache[name]
            print(f"BGM {name} already exists")
        else:
            if path != None:
                self._bgm_cache[name] = path
                print(f"Added BGM {name} at {path}")
            else:
                raise FileNotFoundError(path)

        pygame.mixer.music.load(path)

    def play(
        self,
        name: str,
        loop: int = 0,
        start: int = 0,
        fade: int = 0
    ) -> None:
        self.add_music(name)
        pygame.mixer.music.play(loop, start, fade)
        self._currently_playing = name
        print(f"Playing BGM {name}, looping? {loop}, started at {start} ms, will fade at {start} ms")

    def get_music(self) -> str | None:
        return self._currently_playing

    def stop(self) -> None:
        pygame.mixer.music.stop()
        self._currently_playing = None
        print("Stopped BGM")

    def unload(self) -> None:
        pygame.mixer.music.unload()
        print("Unloaded BGM")

    def pause(self) -> None:
        pygame.mixer.music.pause()
        print("Paused BGM")


class SFXManager:
    """
    for sfx only, since its realtime
    """

    def __init__(self) -> None:
        self._sfx_cache: dict[str, pygame.mixer.Sound] = {}
        self._currently_playing: dict[int, tuple[pygame.mixer.Channel, pygame.mixer.Sound]] = {}

        self.volume: float = 0
        self.set_volume(VOLUME)

        print("Initialized SFX manager")

    def set_volume(self, val: float) -> None:
        self.volume = max(0, min(1, val))

    def stop_all(self) -> None:
        pygame.mixer.stop()
        print("Stopped all SFX")

    def pause_all(self) -> None:
        pygame.mixer.pause()
        print("Paused all SFX")

    def resume_all(self) -> None:
        pygame.mixer.unpause()
        print("Unpaused all SFX")

    def add_sfx(self, name: str, path: pathlib.Path | None = None) -> None:
        if name in self._sfx_cache and path == None:
            print(f"SFX {name} already exists")
        else:
            if path != None:
                self._sfx_cache[name] = pygame.mixer.Sound(path)
                print(f"Added SFX {name} at {path}")
            else:
                raise FileNotFoundError(path)

    def play(
        self,
        name: str,
        loop: int = 0,
        fade_in_time: int = 0,
        max_time: int = 0,
        volume: float | None = None,
        pan: tuple[float, float] = (1, 1)
    ) -> int:
        self.add_sfx(name)

        s = self._sfx_cache[name]

        c = pygame.mixer.find_channel()
        c.set_volume(volume if volume else self.volume)
        c.set_volume(c.get_volume()*pan[0], c.get_volume()*pan[1])
        s.play(loop, max_time, fade_in_time)
        id = hash(s)
        self._currently_playing[id] = (c, s)

        print(f"Playing SFX {name} at {c.id}, busy? {c.get_busy()}")
        return id

    def fade_sfx(self, sfx_id: int, fade_out_seconds: int) -> None:
        if sfx_id in self._currently_playing:
            self._currently_playing[sfx_id][1].fadeout(fade_out_seconds)

    def stop_sfx(self, sfx_id: int) -> None:
        if sfx_id in self._currently_playing:
            self._currently_playing[sfx_id][1].stop()
            del self._currently_playing[sfx_id]
        print(f"Stopped SFX {sfx_id}")

    def update(self) -> None:
        to_delete = []

        for sfx_id, (channel, sfx) in self._currently_playing.items():
            if not channel.get_busy():
                to_delete.append(sfx_id)

        for id in to_delete:
            del self._currently_playing[id]


class SoundManager:
    def __init__(self) -> None:
        self.bgm = BGMManager()
        self.sfx = SFXManager()
