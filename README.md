# _Cleanup Catastrophe!_ (v.0.3.0-beta)

![cleanup catastrophe logo](/assets/img/ui/logo.png)

## ABOUT

**_Cleanup Catastrophe!_** (sometimes abbreviated as _CC!_) is an educational free-to-play indie game that aims to raise awareness about the issue of plastic pollution in the ocean among young minds. Inspired by the vibrant colors of the SEGA Genesis home console, our game introduces the player to a simple user interface as you clean various trash items scattered throughout the ocean floor. Through this game, we hope to educate our players the importance of effective solid waste management, and how to apply them in their daily lives.

## STATISTICS

[![python-version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://python.org/downloads/release/python-3120)
![stars](https://img.shields.io/github/stars/richkdev/cleanup-catastrophe)
![forks](https://img.shields.io/github/forks/richkdev/cleanup-catastrophe)
![license](https://img.shields.io/github/license/richkdev/cleanup-catastrophe)
![version](https://img.shields.io/github/release/richkdev/cleanup-catastrophe)
![downloads](https://img.shields.io/github/downloads/richkdev/cleanup-catastrophe/latest/total)
![issues](https://img.shields.io/github/issues/richkdev/cleanup-catastrophe)
![code size](https://img.shields.io/github/languages/code-size/richkdev/cleanup-catastrophe)
![repo size](https://img.shields.io/github/repo-size/richkdev/cleanup-catastrophe)

## GAMEPLAY

WIP

## INSTALLATION

1. **Clone the repository**. See this [article](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) for more information.
2. **Install all the dependencies**, listed in `requirements.txt`.

## USAGE

You can run the game by running one of the following command in your terminal:

* For local: `python main.py`
* For web: `python -m pygbag --no_opt --disable-sound-format-error main.py`

## BUILDING

* For local: `pyinstaller main.spec` (exported file type will depend on your system, e.g. `CleanupCatastrophe.exe` for Windows, `CleanupCatastrophe.app` for macOS, etc.)
* For web: `python -m pygbag --no_opt --disable-sound-format-error --build main.py`

## LICENSE

_Cleanup Catastrophe!_ is licensed under the _GNU General Public License v3.0_.

See [`LICENSE`](/LICENSE) for more information.

## CONTRIBUTE

Contributions to the _Cleanup Catastrophe!_ game repository are greatly appreciated. It helps us to improve and develop the game to appeal to the masses. If you would like to contribute to this game, please:

* fork the repository and create a pull request, or
* open an issue with the appropriate tag/tags

[![contributors](https://contrib.rocks/image?repo=richkdev/Cleanup-Catastrophe)](https://github.com/richkdev/Cleanup-Catastrophe/graphs/contributors)

## SPECIAL THANKS

The developer would like to thank:

* [RJ](https://github.com/TheRealRyanHajj), for laying the foundations for the spritesheet cutter.
* [hulahhh](https://github.com/tea-enjoyer11), for introducing me to `pygame-ce`, as well as laying on the foundations for the sound manager and multi-line text drawer.
* [wheaty](https://wheatnsticks.carrd.co/), for making custom music.
* [Paul m. p. Peny](https://github.com/pmp-p), for developing `pygbag`, a utility that allows for `pygame-ce` projects to be playable on web browsers.
* [Szabolcs Dombi](https://github.com/szabolcsdombi), for developing `zengl`.
* [DickerDackel](https://github.com/DickerDackel), for introducing me to `uv`.
* All the [`pygame-ce` contributors](https://github.com/pygame-community/pygame-ce) for making such an amazing game library.

Here is a complete list of works that are used in the game.

* [Fuzzball](https://fontstruct.com/fontstructions/show/1143200/sonic_genesis_mega_drive_font), for making the Sonic Genesis Font
* [stgiga](https://www.dafont.com/unifontexmono.font), for making the Unifont Ex Mono font
* [Blubberquark](https://blubberquark.tumblr.com/post/185013752945/using-moderngl-for-post-processing-shaders-with), for making the original CRT shader code for ModernGL
