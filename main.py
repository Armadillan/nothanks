import neat

import evaluator
import env

GROUP_SIZE = 4
CONFIG_FILENAME = "NoThanks.config"
ENVIRONMENT = env.NoThanks()

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

p.run(evaluator_instance.eval_genomes, 1)
