# todo list

## code stuff

- [ ] use requests module to check latest game version on gh repo via githack _<https://raw.githack.com/richkdev/Cleanup-Catastrophe/main/VERSION>_
- [x] add ability to add line breaks into `drawText` func
- [ ] custom sizes for the spritesheet splitter, but same hitbox rect & diff image rects
- [ ] refactor so that each sprite takes the same params and make a custom group for supporting drawing sprites with an offset
- [x] fix default frag & vert shader
- [x] port blubberquark's crt shader for `moderngl` to `zengl` with pygbag compat in mind
- [x] make "video player" that works on local (using `opencv-python` + `ffmpeg`) and web
- [ ] write unit tests, using `unittest` module
- [ ] write integration tests, using github ci/cd workflows
- [-] use `pymunk` (python wrapper for box2d) for physics system, then display that data using with pygame
- [x] overhaul state management so that it doesnt inherit `Game` since it'll cause memory issues later and set all states as enums & as items on a dictionary
- [ ] make loading screen and loading functions (loads state, assets, etc), reference: _<https://www.youtube.com/watch?v=KWGDgPldPVo>_
- [ ] detect cmdline args when run thru cmd line, using `argparse` (e.g. `--debug` to log everything into the file), when using pygbag: _<https://discord.com/channels/772505616680878080/971360806287577098/1292327416957636671>_
- [x] turn discord presence into async for easier

## art

- [ ] recolor all sprites using sega genesis palette (might not do cuz im lazy, ill prolly make a generator for that lol)
- [ ] make intro cutscene as comic, display using "video player" thingy
- [x] make new sprites **(WIP)**

## gameplay

- [ ] include multiple minigames from multiple fandoms!
  - [ ] melodical mess, collab with rhythm game?
- [x] add bombs which you cant pick up, decreases your fishing rod durability **(WIP)**
- [x] make a hub world for menu select with platformer physics and collisions
- [ ] make levels to teach new players how to play
- [ ] add a shop system to purchase new rods using trash (e.g. premium fishing rod with 250 durability for 500 trash?), might implement gui using `pygame-gui` with some modifs so that it can be selected via arrow keys and such
