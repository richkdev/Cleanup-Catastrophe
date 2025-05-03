# todo list

## code stuff

- [ ] use requests module to check latest game version on gh repo via githack _<https://raw.githack.com/richkdev/Cleanup-Catastrophe/main/VERSION>_
- [x] add ability to add line breaks into `drawText` func
- [ ] custom sizes for the spritesheet, but same hitbox rect & diff image rects **(WIP)**
- [ ] log everything!!!
- [x] make a hub world for menu select
- [ ] make levels to teach new players how to play
- [x] fix normal shader
- [x] port blubberquark's crt shader for `moderngl` to `zengl`
- [x] make "video player" that works on local (using `opencv-python` + `ffmpeg`) and web
- [ ] write unit tests, using `unittest` module
- [ ] write integration tests, using github ci/cd workflows
- [ ] use `pymunk` (python wrapper for box2d) for physics system, then display that data using with pygame
- [ ] overhaul state management so that it doesnt inherit `Game` since it'll cause memory issues later and set all states as enums or as items on a dictionary
- [ ] make loading screen and loading functions (loads state, assets, etc), reference: _<https://www.youtube.com/watch?v=KWGDgPldPVo>_
- [ ] add ability to detect cmdline options for game, using `argparse` module

## art

- [ ] recolor all sprites using sega genesis palette **(might not do cuz im lazy)**
- [ ] make intro cutscene as comic, display using "video player" thingy

## ideas

- [ ] include multiple minigames from multiple fandoms!
  - [ ] melodical mess, collab with rhythm game?
- [x] add bombs which you cant pick up, decreases your fishing rod durability **(WIP)**
