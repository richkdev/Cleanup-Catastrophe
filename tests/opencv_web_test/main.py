# /// script
# dependencies = [
#   'numpy',
#   'opencv-python',
#   'pygame-ce'
# ]
# ///

import os
import sys
import cv2
import pygame
import asyncio

# desktop - requires ffmpeg
# pygbag - has opencv-python and ffmpeg wheel from pyodide using `--git` param AND it supports websocket connections so it just needs audio for it to become an actual video player. thanks @pmp-p for the help!
# pyodide - REMOVED since it needs pyfetch since it doesn't support websocket connections AND you gotta use pyodide's file system AND it returns "Error: Unsupported data type" which i have no idea how to fix

emscripten = sys.platform in ('emscripten', 'wasi')
print("emscripten?", emscripten)

if emscripten:
    import platform

print(cv2.getBuildInformation())

def newPath(relPath: str) -> str:
    relPath = relPath.replace(("/" if len(relPath.split("/"))>1 else "\\"), os.sep)
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        basePath = sys._MEIPASS # type: ignore -> pyinstaller temp folder
    else:
        basePath = os.path.abspath('.')
    return os.path.join(basePath, relPath)

input_video_path = newPath("assets/video.mp4")
print("FILE PATH HERE!!!", input_video_path)

async def main():
    url = input_video_path
    print("is a url?", url.__contains__(":"))

    video = cv2.VideoCapture()
    if emscripten and url.__contains__(":"): # can detect videos from web!
        async with platform.fopen(url, "rb") as data: # type: ignore
            data.rename_to("/tmp/feed.mp4")
            video.open("/tmp/feed.mp4")
    else:
        video.open(url)

    print("VIDEO OPENED", video.isOpened()) # should return True

    if video.isOpened():
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        FPS = int(video.get(cv2.CAP_PROP_FPS))
        totalFrames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        print("SUCCESS", width, height, FPS, totalFrames) # should return "SUCCESS 480 480 29"
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

        screen.fill((0, 0, 255)) # set to blue for debug purposes

        status, video_frame = video.read()
        currentFrame = int(video.get(cv2.CAP_PROP_POS_FRAMES))
        if not emscripten: # somehow is automatic on web?
            if status:
                cv2.waitKey(1)
                print(f"READ FRAME {currentFrame} of {totalFrames}", status)
            else:
                print("FAILED TO READ FRAME")
                running = False

        image = pygame.image.frombuffer(video_frame.tobytes(), video_frame.shape[1::-1], "BGR")
        screen.blit(image, (0, 0))

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)

    print("VIDEO END")
    video.release()
    pygame.quit()

if __name__ ==  '__main__':
    asyncio.run(main())
