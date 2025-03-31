# todo list

## code stuff

- [x] make state management possible using `State` class
- [ ] use requests module to check latest game version on gh repo via githack _<https://raw.githack.com/richkdev/Cleanup-Catastrophe/main/VERSION>_
- [x] add ability to add line breaks into `drawText` func
- [ ] custom sizes for the spritesheet, but same hitbox rect & diff image rects **(WIP)**
- [ ] log everything!!!
- [x] make a hub world for menu select
- [ ] make levels to teach new players how to play
- [x] fix normal shader
- [x] port blubberquark's crt shader for moderngl to zengl
- [ ] use `pygame.Window` instead of `pygame.display.set_mode` for creating window **(WIP)**
- [ ] make "video player" that works on:
  - [x] local, using `opencv-python` + `ffmpeg`
  - [ ] web, using all of local dependencies + pyodide/pygbag (?)
- [ ] write tests for game, using `unittest` module **(WIP)**
- [ ] use pymunk (python wrapper for box2d) for physics system, then display that data using with pygame

## art

- [ ] recolor all sprites using sega genesis palette **(might not do cuz im lazy)**
- [ ] make intro cutscene as comic, display using "video player" thingy

## ideas

- [ ] include multiple minigames from multiple fandoms!
  - [ ] melodical mess, collab with rhythm game?
- [x] add bombs which you cant pick up, decreases your fishing rod durability **(WIP)**
