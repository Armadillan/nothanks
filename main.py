import neat

import visualize

import evaluator
import env

GROUP_SIZE = 4
CONFIG_FILENAME = "NoThanks.config"
ENVIRONMENT = env.NoThanks

config = neat.Config(
    neat.DefaultGenome,
    neat.DefaultReproduction,
    neat.DefaultSpeciesSet,
    neat.DefaultStagnation,
    CONFIG_FILENAME,
)

evaluator_instance = evaluator.Evaluator(
    config=config,
    environment=ENVIRONMENT,
    group_size=GROUP_SIZE
)

p = neat.Population(config)


stats = neat.StatisticsReporter()
p.add_reporter(stats)
p.add_reporter(neat.StdOutReporter(True))

w = p.run(evaluator_instance.eval_genomes, 200)

# visualize.draw_net(config, w)
# visualize.draw_net(config, w, prune_unused=True)
# visualize.plot_stats(stats, ylog=False, view=True)
# visualize.plot_species(stats, view=True)
