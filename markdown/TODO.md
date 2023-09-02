# todo list

## issues during development (bugs)

- [ ] fix glsl compatibility (especially the crt frag & vert shaders)
- [x] surf_to_texture copies the texture on the xy pos of the window (not the screen), but doesnt release the prev texture, so causes textures to stack on each other = **fixed** with ctx.clear(0) = sets bg as black
- [ ] make the code for fishing rod (i lost the old code)

## for future updates

- [ ] use noise module or opensimplex to generate coordinates of trash spawning _<https://pypi.org/project/opensimplex>_
- [ ] use requests module to check game version on my site & update it using itch io game download _<https://www.w3schools.com/python/module_requests.asp>_ or mb for account verification
- [ ] add bombs which you cant pick up and just decreases your helth
- [ ] make animated cutscenes in pixel art
- [ ] add saving to the game
- [ ] recolor all stuffs using genesis palette
- [ ] port game to html using _<https://pygame-web.github.io/wiki/pygame-script>_ or just do _<https://pygame-web.github.io/showroom/python.html?-d#https://raw.githubusercontent.com/richkdev/Cleanup-Catastrophe/main/main.py>_ (remember to change the dirs of the game and file stuffs later)
- [ ] add ending for demo (after 100 trash, "paul has cleaned a lot of trash, but in the end, he still can't do it without your help. help marine pollution by ...")

## sideshit stuff

- [ ] make jp ver. for tagajo high school students
- [ ] make pico8 port for the game cuz i w anna play it on my pico8 console
- [ ] add newgrounds support becauase i fuckign love newgrounds (idea: maybe use js2py module with NewgroundsIO-JS or killedbyapixel's newgrounds js wrapper)
- [ ] maybe add gamejolt support instead of newgrounds? idfk i love ng
- [ ] might make a newgrounds api wrapper in python (basically a port of newgroundsio-js) as a side project (not really related to cleanup catastrophe)
