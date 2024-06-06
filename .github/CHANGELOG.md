# change log lol

## v.0.2.1 - a heck of catastrophe

### details

- fixed `RuntimeError` with discord rpc ~~thread~~ process, had to use nest-asyncio _<https://pypi.org/project/nest-asyncio>_ and turn it into asyncio process that sleeps for 10 seconds then updates
- added state management with my own finite state-machine
- fixed a problem, since moderngl stuffs needs to refer to a context, i turn it into a ~~main thread~~ async process

### notes

1. SAY HELLO TO @TheRealRyanHajj AND @tea-enjoyer11 !!! this thing is gonna be real and not just a side project of mine!!
2. might pump out demo build for sage 2024? only if i manage to make finish most of stuff in the new todo

## v.0.2.0 - the extra awesome update

### details

- added multithreading so processes can work in parallel
- restructured files (again)
- actually made the game core
- added local highscore as proof-of-concept for a cloud server (will prob using apache db using my raspi zero as a web server)
- made classes for each sprite so they can be easily called
- added emscripten detection for web building
- added `_MEIPASS` detection for native building

### notes

made a proof-of-concept for the 20 seconds jam 2023: _<https://richkdev.itch.io/cleanup-catastrophe-proto>_

**NOTE 2:** porting pygame to wasm is tiring, might scrap it next update

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
