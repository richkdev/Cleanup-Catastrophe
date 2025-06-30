# change log lol

## v.0.2.1 - "shouldve been a seperate major version" update

### details

- switched to pygame community edition! frects are so cool
- switched from multithreading to asyncio for web compat
- added state management with my own finite state machine
- switched from moderngl to zengl for pygbag compatc
- WIP hub world for selecting gamemodes, just need to add a camera system
- custom descriptions for discord rich presence based on gamestate

### notes

WIP

## v.0.2.0 - the extra awesome update

### details

- added multithreading so processes can work in parallel
- restructured files (again)
- actually made the game core
- added local highscore as proof-of-concept for a cloud server
- made classes for each sprite so they can be easily called
- added emscripten detection for running on pygbag
- added `_MEIPASS` detection for native building

### notes

1. made a proof-of-concept for the 20 seconds jam 2023: _<https://richkdev.itch.io/cleanup-catastrophe-proto>_
2. porting pygame to wasm is tiring, might scrap it next update

## v.0.1.1 - the awesome update_

### details

- restructured files + added new files
- came up with a sick new logo
- made music in beepbox, still needs a lot of polish
- finally picked up OOP, and used it for the sprites (dirty sprites)
- fixed how PNGs are displayed (import after display so it can convert alpha) & rendered on the screen (images not upscaled anymore, window is upscaled using SCALED flag)
- added a lot of flags to the pygame screen
- added discord rich presence using pypresence
- added opengl context, which uses GPU instead of CPU (thanks DaFluffyPotato)
- tried to export using pyinstaller, it kind of works (will fix spec file later)
- removed herobrine

### notes

i should name the next update as "the extra awesome update"

## v.0.1.0 - yes

- made 'the base' of the game
- really bad
