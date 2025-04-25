# /// script
# dependencies = [
#   'numpy',
#   'opencv-python',
#   'pygame-ce'
# ]
# ///

import os
import sys
import pygame
import cv2
from pathlib import Path

IS_WEB = sys.platform in ('emscripten', 'wasi')

if not pygame.mixer.get_init():
    pygame.mixer.pre_init(frequency=44100, size=16, channels=2, buffer=512)
    pygame.mixer.init()
    pygame.mixer.set_num_channels(64)

if IS_WEB:
    pygame.mixer.SoundPatch()  # type: ignore
    import platform
else:
    from moviepy import VideoFileClip
    import requests


class VideoPlayer(object):
    def __init__(self) -> None:
        self.video = cv2.VideoCapture()
        self.channel = pygame.mixer.find_channel(True)
        self.audio: pygame.Sound
        self.width: int
        self.height: int
        self.FPS: int
        self.currentFrame: int
        self.totalFrames: int

        self.path: Path
        self.tmp_dir: Path
        self.has_audio: bool
        self.override_audio_source: Path | None
        self.remove_dir: bool

    def __repr__(self) -> str:
        return f"{__name__}.{type(self).__name__}(path=\"{self.path}\", has_audio={self.has_audio}, override_audio_source={self.override_audio_source is not None})"

    async def open(
            self,
            path: Path | str,
            tmp_dir: Path | str,
            has_audio: bool,
            override_audio_source: Path | str | None,
            remove_dir: bool = True
        ) -> None:
        self.path = Path(path)
        self.tmp_dir = Path(tmp_dir)
        self.has_audio = has_audio
        self.override_audio_source = Path(override_audio_source) if override_audio_source is not None else None
        self.remove_dir = remove_dir

        if not IS_WEB and not self.tmp_dir.exists():
            os.makedirs(self.tmp_dir, exist_ok=True)

        if self._isURL(self.path):
            tmp_video = await self._fetch(self.path, self.tmp_dir)
            self.video.open(tmp_video)
        else:
            self.video.open(str(self.path))

        self.width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.FPS = int(self.video.get(cv2.CAP_PROP_FPS))
        self.totalFrames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))

        if self.has_audio:
            if self.override_audio_source is None:
                # use the original video's audio
                if not IS_WEB:
                    # file is local
                    tmp_audio = self.tmp_dir.joinpath(f"{self.path.stem}.mp3")

                    with VideoFileClip(tmp_video if self._isURL(self.path) else self.path) as clip:
                        if clip.audio is not None:
                            clip.audio.write_audiofile(tmp_audio)
                        else:
                            tmp_audio = await self._fetch("https://github.com/pygame-web/pygbag/raw/refs/heads/main/static/empty.ogg", self.tmp_dir) # use pygbag's empty ogg file for now, since other empty files just causes errors
                        clip.close()
                else:
                    raise NotImplementedError(
                        "Haven't figured out how to extract audio from video on pygbag, sorry. To play audio, you must manually set the path to the video\'s audio as the desired path."
                    )
            elif isinstance(self.override_audio_source, Path):
                if self._isURL(self.override_audio_source):
                    # check if audio is a URL
                    self.audio = pygame.Sound(
                        await self._fetch(self.override_audio_source, self.tmp_dir)
                    )
                else:
                    # if not a URL and is local file
                    self.audio = pygame.Sound(self.override_audio_source)
            else:
                raise TypeError

        if self.remove_dir:
            os.removedirs(self.tmp_dir)

    async def _fetch(
            self,
            url: Path | str,
            tmp_dir: Path,
        ) -> str:
        url = self._urlify(url)
        tmp_path = tmp_dir.joinpath(Path(url).name)

        if self._isURL(url):
            if not IS_WEB:
                # copied from https://stackoverflow.com/questions/76628078/downloading-video-with-python-requests-content-receiving-status

                response = requests.request(method="GET", url=url, stream=True)
                # file_size = int(response.headers['Content-Length'])
                # downloaded = 0
                with open(tmp_path, "wb") as data:
                    for chunk in response.iter_content(chunk_size=1024):
                        # downloaded += len(chunk)
                        # print(f"Downloaded {downloaded}/{file_size} bytes")
                        data.write(chunk)
            else:
                async with platform.fopen(url, "rb") as data:  # type: ignore
                    data.rename_to(tmp_path)
            return str(tmp_path)
        else:
            raise FileNotFoundError("File is not a URL.")

    def _isURL(self, path: Path | str) -> bool:
        return "http" in str(path)

    def _urlify(self, url: Path | str) -> str:
        return Path(url).as_posix().replace("https", "http").replace(":/", "://")

    def set_frame(self, frameNumber: int) -> None:
        self.currentFrame = int(self.video.set(cv2.CAP_PROP_POS_FRAMES, frameNumber))

    def get_frame(self) -> pygame.Surface:
        self.currentFrame = int(self.video.get(cv2.CAP_PROP_POS_FRAMES))
        self.totalFrames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        status, video_frame = self.video.read()

        if not IS_WEB and not status:
            blank =  pygame.Surface((self.width, self.height))
            blank.fill((0, 0, 0))
            return blank
        else:
            return pygame.image.frombuffer(
                video_frame.tobytes(),
                video_frame.shape[1::-1],
                "BGR"
            )

    def play_audio(self, loops: int = 0, maxtime: int = 0, fade_ms: int = 0) -> None:
        self.channel.play(self.audio, loops, maxtime, fade_ms)

    def busy_audio(self) -> bool:
        return self.channel.get_busy()

    def close(self) -> None:
        self.video.release()

        if self.has_audio:
            self.audio.stop()
