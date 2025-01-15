import cProfile

if __name__ == "__main__":
    from scripts.game import Game
    with cProfile.Profile() as profiler:
        Game()
    profiler.print_stats()
