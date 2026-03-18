# todo list

## code

- [ ] use requests module to check latest game version on gh repo via githack _<https://raw.githack.com/richkdev/Cleanup-Catastrophe/main/VERSION>_
- [ ] custom sizes for the spritesheet splitter, but same hitbox rect & diff image rects, with subsurface frame pos & size stored in json
- [ ] seperate state manager from discord presence manager, for cleaner codebase
- [ ] make dialogue engine, with dialogue stored in json
- [ ] turn lobby state data into json
- [x] refactor so that each sprite takes the same params and make a custom group for supporting drawing sprites with an offset **(WIP)**
- [x] fix default frag & vert shader
- [x] port crt shader for `moderngl` to `zengl` with pygbag compat in mind
- [x] overhaul state management so that it doesnt inherit `Game` since it'll cause memory issues later and set all states as enums & as items on a dictionary
- [ ] make loading screen and loading functions (loads state, assets, etc), [reference](https://www.youtube.com/watch?v=KWGDgPldPVo)
- [ ] detect cmdline args when run thru cmd line, using `argparse` (e.g. `--debug` to log everything into the file), when using pygbag: _<https://discord.com/channels/772505616680878080/971360806287577098/1292327416957636671>_
- [x] turn discord presence into async
- [x] make loading screen and async loading functions (loads state, assets, etc) **(WIP)**
- [ ] use uv build system

## art

- [ ] recolor all sprites using sega genesis palette (might not do cuz im lazy, ill prolly make a generator for that lol)
- [ ] make intro cutscene
- [x] make new sprites **(WIP)**

## gameplay

- [x] add bombs which you cant pick up, decreases your fishing rod durability **(WIP)**
- [x] make a hub world for menu select
- [ ] make levels to teach new players how to play
- [ ] add a shop system to purchase new rods using trash (e.g. premium fishing rod with 250 durability for 500 trash?), might implement gui using `pygame-gui` with some modifs so that it can be selected via arrow keys and such
- [ ] fix catastrophe gamemode so that the trash actually moves into the screen like how animal restaurant does it, with more trash floating in as you wait more, might want to use binomial distribution for that
