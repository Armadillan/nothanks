import random
import os

import neat

class Evaluator:

    def __init__(self, config, environment, group_size, *env_args):
        self.config = config
        self.environment = environment
        self.group_size = group_size
        self.env_args = env_args

    def get_random_groups(self, pop_size):
        random_order = [x for x in range(pop_size)]
        random.shuffle(random_order)
        groups = []
        for i in range(0, pop_size, self.group_size):
            groups.append(random_order[i:i+self.group_size])

        if pop_size % self.group_size != 0:
            groups[-1] += random_order[0:(pop_size % self.group_size)]

        return groups

    def epoch(self, network_groups):

        scores = []
        for group in network_groups:
            group_scores = self.environment(self.env_args).play(list(group))
            scores.append(group_scores)

        return scores

    def eval_genomes(self, genomes, *_):
        pop_size = len(genomes)
        groups = self.get_random_groups(pop_size)
        ordered_genomes = list(zip(*genomes))[1]

        network_groups = []
        for group in groups:
            tmp_group = map(lambda i: ordered_genomes[i], group)
            tmp_group = map(
                lambda genome: neat.nn.FeedForwardNetwork.create(genome, self.config),
                tmp_group
                )
            network_groups.append(tmp_group)

        scores = self.epoch(network_groups)
        flat_scores = [score for group in scores for score in group]
        # ordered_genome indices in the same order as flat_scores
        flat_groups = [g_i for group in groups for g_i in group]

        for index, genome_id in enumerate(flat_groups):
            #notmakes sure every genome is assigned fitness once
            #shouldn't make a difference, but easier to test/debug
            if index == pop_size:
                break
            ordered_genomes[genome_id].fitness = -flat_scores[index]
