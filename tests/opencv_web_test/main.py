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

# run this command for pygbag
#   pygbag --git "tests/opencv_web_test/main.py"

# desktop - requires ffmpeg
# pygbag - needs an ffmpeg wasi for it to run on web, discussion: https://discord.com/channels/772505616680878080/971360806287577098/1354442361459183889
# pyodide - crashes cuz ffmpeg's video processing stuff doesn't exist?? but ffmpeg itself exists according to cv2.getBuildInformation??? so it throws a ton of errors

pyodideAvailable = "pyodide" in sys.modules
print("pyodide?", pyodideAvailable)

print(cv2.getBuildInformation())

if pyodideAvailable:
    import js # type: ignore
    import base64, io
    currentURL: str

def newPath(relPath: str):
    relPath = relPath.replace(("/" if len(relPath.split("/"))>1 else "\\"), os.sep)
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        basePath = sys._MEIPASS # type: ignore -> pyinstaller temp folder
    elif sys.platform == "emscripten" and pyodideAvailable:
        basePath = currentURL # type: ignore -> currentURL is set by pyodide
    else:
        basePath = os.path.abspath('.')
    return os.path.join(basePath, relPath)

input_video_path = newPath("tests/opencv_web_test/video.mp4")
print("FILE PATH HERE!!!", input_video_path)

video = cv2.VideoCapture()
print("VIDEO OPENED?", video.open(filename=input_video_path))

if video.isOpened():
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    FPS = int(video.get(cv2.CAP_PROP_FPS))
    print("SUCCESS", width, height, FPS)
else:
    print("FAILED")

screen = pygame.display.set_mode((width, height))

clock = pygame.Clock()


async def main():
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

        if pyodideAvailable:
            imageValue = "data:image/png;base64, " + str(base64.b64encode(io.BytesIO(pygame.image.tobytes(image, "RGBA")).read()))
            print(imageValue)
            print(js.window.pyodide.globals.set("imagelol.src", imageValue))

        pygame.display.flip()
        clock.tick(FPS)

        if pyodideAvailable:
            await asyncio.sleep(1/FPS)
        else:
            await asyncio.sleep(0)

    print("VIDEO END")
    video.release()
    pygame.quit()

asyncio.run(main())
