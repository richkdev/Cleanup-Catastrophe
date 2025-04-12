# /// script
# dependencies = [
#   'numpy',
#   'opencv-python',
#   'pygame-ce'
# ]
# ///

# WIP!!!!! doesnt work on web yet

import os
import sys
import cv2
import pygame
import asyncio
import platform
import io
import tempfile

# run this command for pygbag
#   pygbag --git "tests/opencv_web_test/main.py"

# desktop - requires ffmpeg
# pygbag - has opencv-python and ffmpeg wheel from pyodide (if `--git` param) AND it supports websocket connections, so it works now. huh.
# pyodide - SCRAPPED since it needs pyfetch since it doesn't support websocket connections AND you gotta use pyodide's file system AND it returns "Error: Unsupported data type" which i have no idea how to fix

emscripten = sys.platform in ('emscripten', 'wasi')
pyodideAvailable = "pyodide" in sys.modules
print("pyodide?", pyodideAvailable)

print(cv2.getBuildInformation())

if pyodideAvailable:
    import pyodide # type: ignore
    baseURL: str
    blobData: str

def newPath(relPath: str):
    relPath = relPath.replace(("/" if len(relPath.split("/"))>1 else "\\"), os.sep)
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        basePath = sys._MEIPASS # type: ignore -> pyinstaller temp folder
    elif pyodideAvailable:
        basePath = baseURL # type: ignore -> baseURL is set by pyodide
    else:
        basePath = os.path.abspath('.')
    return os.path.join(basePath, relPath)

input_video_path = newPath("assets\\video.mp4") if emscripten else newPath("tests/opencv_web_test/assets/video.mp4")
print("FILE PATH HERE!!!", input_video_path)

async def main():
    if pyodideAvailable:
        from pyodide.http import pyfetch # type: ignore
        res = await pyfetch(input_video_path) # type: ignore
        print(res.status)
        url = "NOT SUPPOSED TO BE USED"
    else:
        url = input_video_path

    print("url to the vid", url)

    video = cv2.VideoCapture()
    
    if pyodideAvailable:
        video.open(blobData) # BROKEN, DON'T USE
    elif emscripten:
        async with platform.fopen(url, "rb") as data: # type: ignore
            if isinstance(data, io.BufferedReader):
                video.set(cv2.CAP_PROP_VIDEO_STREAM, -1)

                with tempfile.NamedTemporaryFile(mode="rb", delete=False) as temp_file:
                    temp_file.write(data.read())
                    temp_file_path = temp_file.name

                video.open(temp_file_path)
    else:
        video.open(url)

    print("VIDEO OPENED", video.isOpened())

    if video.isOpened():
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        FPS = int(video.get(cv2.CAP_PROP_FPS))
        print("SUCCESS", width, height, FPS)
    else:
        print("FAILED")

    screen = pygame.display.set_mode((width, height))
    clock = pygame.Clock()

    running = True
    print("VIDEO START")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        status, video_frame = video.read()
        if status:
            cv2.waitKey(1)
        else:
            break

        image = pygame.image.frombuffer(video_frame.tobytes(), video_frame.shape[1::-1], "BGR")
        screen.blit(image, (0, 0))

        pygame.display.flip()
        clock.tick(FPS)

        if pyodideAvailable:
            await asyncio.sleep(1/FPS)
        else:
            await asyncio.sleep(0)

    print("VIDEO END")
    video.release()
    pygame.quit()

if __name__ ==  '__main__':
    if pyodideAvailable: # required if you want to not get `RuntimeError` on pyodide
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    else:
        asyncio.run(main())
