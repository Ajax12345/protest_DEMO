import random, typing, copy
import warnings, networkx as nx
import matplotlib.pyplot as plt
from actor_genotype import Genotype, node
import statistics, collections, numpy as np
import json, datetime, itertools
from sympy.logic import POSform
from sympy import symbols
import sympy

TRAITS = [
    'a',
    'b',
    'c',
    'd'
]

ALL_TRAITS = [*itertools.product(*[range(2) for _ in range(len(TRAITS))])]

assert len(ALL_TRAITS) == 2**4

class Actor:
    """
    Traits derived in part from https://www.annualreviews.org/doi/pdf/10.1146/annurev-polisci-051010-111659

    empathy
    aggression
    narcissism
    leadership
    honesty
    resilience
    assertiveness
    persuasiveness
    agreeableness
    """
    def __init__(self, env = None) -> None:
        self.traits = self.__class__.random_trait()
        self.genotype = self.build_genotype()
        self._outputs = {}
        self.score = 0
        self.optimal_score = 0
        self.id = None
        if env is not None:
            self.id = max([*env.agent_bindings]+[0]) + 1
            env.agent_bindings[self.id] = self

    def reset(self) -> 'Actor':
        self.genotype = self.build_genotype()
        self._outputs = {}
        self.score = 0
        self.optimal_score = 0
        return self

    def mutate(self, prob:float = 0.01) -> None:
        if random.random() >= 1 - prob:
            '''
            for ind in random.sample([*range(len(self.traits))], random.randint(1, 2)):
                self.traits[ind] = int(not self.traits[ind])
            '''
            ind = random.choice([*range(len(self.traits))])
            self.traits[ind] = int(not self.traits[ind])
            self.genotype.mutate_v2()

    def complexity(self, min_circuit:bool = False) -> int:
        if not min_circuit:
            return self.genotype.complexity

        def traverse(expr:sympy, d:dict) -> None:
            if isinstance(expr, int):
                return 

            if isinstance(expr, sympy.core.symbol.Symbol):
                d[1].add(str(expr))
                return
            
            if isinstance(expr, sympy.logic.boolalg.Not):
                d[0].append('Not')
            
            else:
                d[0].extend([type(expr).__name__ for _ in range(len(expr.args) - 1)])
            
            for i in expr.args:
                traverse(i, d)

        minterms = []
        for trait in ALL_TRAITS:
            if trait in self._outputs:
                if self._outputs[trait]:
                    minterms.append([*trait])
            
            else:
                with self.genotype:
                    if self.genotype(*trait)[0]:
                        minterms.append([*trait])

        #print('in here')
        expr = POSform([*symbols(f'a:{len(TRAITS)}')], minterms, [])
        d = {1:set(), 0:[]}
        traverse(expr, d)
        return len(d[1]) + len(d[0])

    @classmethod
    def random_trait(cls) -> typing.List[int]:
        return [int(random.random() >= 1 - float(i.split(': ')[1])) for i in filter(None, cls.__doc__.split('\n')) if i.strip().lstrip()]

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.traits})'


def DEFAULT_GENOTYPE():
    return Genotype(
        inputs = [
            node.Input(int, 0),
            node.Input(int, 1),
            node.Input(int, 2),
            node.Input(int, 3),
            node.Input(int, 4),
            node.Input(int, 5),
            node.Input(int, 6),
            node.Input(int, 7),
            node.Input(int, 8)
        ],
        constants = [
            node.Constant(int, 9),
            node.Constant(int, 10)
        ],
        gates = [
            node.operator.OR(11, inputs=[9, 4]),
            node.operator.OR(12, inputs=[0, 9]),
            node.operator.NAND(13, inputs=[9, 3]),
            node.operator.OR(14, inputs=[2, 1]),
            node.operator.AND(15, inputs=[5, 5]),
            node.operator.OR(16, inputs=[10, 4]),
            node.operator.NOR(17, inputs=[5, 8]),
            node.operator.OR(18, inputs=[3, 7]),
            node.operator.NAND(19, inputs=[7, 7]),
            node.operator.NOR(20, inputs=[0, 9]),
            node.operator.OR(21, inputs=[16, 12]),
            node.operator.NAND(22, inputs=[20, 5]),
            node.operator.NAND(23, inputs=[14, 16]),
            node.operator.OR(24, inputs=[11, 13]),
            node.operator.OR(25, inputs=[2, 5]),
            node.operator.NOR(26, inputs=[18, 3]),
            node.operator.NAND(27, inputs=[12, 5]),
            node.operator.OR(28, inputs=[10, 9]),
            node.operator.NAND(29, inputs=[17, 19]),
            node.operator.OR(30, inputs=[21, 27]),
            node.operator.OR(31, inputs=[18, 29]),
            node.operator.NOR(32, inputs=[28, 27]),
            node.operator.AND(33, inputs=[21, 25]),
            node.operator.NOR(34, inputs=[21, 16]),
            node.operator.AND(35, inputs=[12, 25]),
            node.operator.NAND(36, inputs=[14, 29]),
            node.operator.NAND(37, inputs=[26, 24]),
            node.operator.OR(38, inputs=[31, 8]),
            node.operator.NOR(39, inputs=[37, 24]),
            node.operator.NOR(40, inputs=[35, 34]),
            node.operator.NOR(41, inputs=[34, 33]),
            node.operator.NOR(42, inputs=[32, 32]),
            node.operator.NOR(43, inputs=[35, 33]),
            node.operator.NAND(44, inputs=[36, 31])
        ],
        outputs = [
            node.Output(int, 45)
        ]
    )

def DEFAULT_GENOTYPE_1():
    return Genotype(
        inputs = [
            node.Input(int, 0),
            node.Input(int, 1),
            node.Input(int, 2),
            node.Input(int, 3)
        ],
        constants = [
            node.Constant(int, 4, 1),
            node.Constant(int, 5, 0)
        ],
        gates = [
            node.operator.NOR(6, inputs=[3, 4]),
            node.operator.AND(7, inputs=[0, 3]),
            node.operator.NAND(8, inputs=[2, 2]),
            node.operator.OR(9, inputs=[2, 2]),
            node.operator.NAND(10, inputs=[4, 2]),
            node.operator.AND(11, inputs=[8, 6]),
            node.operator.NAND(12, inputs=[1, 10]),
            node.operator.NOR(13, inputs=[5, 9]),
            node.operator.NOR(14, inputs=[9, 7]),
            node.operator.AND(15, inputs=[11, 4]),
            node.operator.NAND(16, inputs=[14, 12]),
            node.operator.OR(17, inputs=[12, 14]),
            node.operator.OR(18, inputs=[17, 15]),
            node.operator.NOR(19, inputs=[17, 16])
        ],
        outputs = [
            node.Output(int, 20, 18)
        ]
    )

def DEFAULT_GENOTYPE_2():
    return Genotype(
        inputs = [
            node.Input(int, 0),
            node.Input(int, 1),
            node.Input(int, 2),
            node.Input(int, 3)
        ],
        constants = [
        ],
        gates = [
            node.operator.OR(4, inputs=[3, 0]),
            node.operator.NAND(5, inputs=[3, 2]),
            node.operator.OR(6, inputs=[1, 2]),
            node.operator.NOR(7, inputs=[3, 2]),
            node.operator.NOR(8, inputs=[6, 5]),
            node.operator.NAND(9, inputs=[3, 0]),
            node.operator.NOR(10, inputs=[4, 6]),
            node.operator.NOR(11, inputs=[2, 7]),
            node.operator.NAND(12, inputs=[1, 11]),
            node.operator.NOR(13, inputs=[8, 5]),
            node.operator.OR(14, inputs=[5, 11]),
            node.operator.NAND(15, inputs=[7, 9]),
            node.operator.AND(16, inputs=[5, 12]),
            node.operator.AND(17, inputs=[9, 4]),
            node.operator.AND(18, inputs=[5, 8]),
            node.operator.NOR(19, inputs=[6, 8])
        ],
        outputs = [
            node.Output(int, 20, 17),
            node.Output(int, 21, 18),
            node.Output(int, 22, 19),
            node.Output(int, 23, 16)
        ],
        params = {
            'inputs':4,
            'constants':0,
            'depth':4,
            'outputs':4,
            'levels_back':3
        }
    )

class Protestor(Actor):
    """
    a: 0.8
    b: 0.4
    c: 0.4
    d: 0.4
    """

    def build_genotype(self) -> typing.Any:
        #return Genotype.random_genotype(4, 2, 4)
        #return copy.deepcopy(DEFAULT_GENOTYPE_1())
        return Genotype.random_genotype_m1(4, 0, 4, 4, 3)
    

class Police(Actor):
    """
    a: 0.4
    b: 0.8
    c: 0.4
    d: 0.4
    """

    def build_genotype(self) -> typing.Any:
        #return Genotype.random_genotype(4, 2, 4)
        #return copy.deepcopy(DEFAULT_GENOTYPE_1())
        return Genotype.random_genotype_m1(4, 0, 4, 4, 3)

class CounterProtestor(Actor):
    """
    a: 0.4
    b: 0.4
    c: 0.8
    d: 0.4
    """

    def build_genotype(self) -> typing.Any:
        #return Genotype.random_genotype(4, 2, 4)
        #return copy.deepcopy(DEFAULT_GENOTYPE_1())
        return Genotype.random_genotype_m1(4, 0, 4, 4, 3)


class Public(Actor):
    """
    a: 0.4
    b: 0.4
    c: 0.4
    d: 0.8
    """

    def build_genotype(self) -> typing.Any:
        #return Genotype.random_genotype(4, 2, 4)
        #return copy.deepcopy(DEFAULT_GENOTYPE_1())
        return Genotype.random_genotype_m1(4, 0, 4, 4, 3)


class Environment:
    def __init__(self) -> None:
        self.agents = {}
        self.agent_bindings = {}
        self.interactions = {}
        self.generation = 1
        self.generation_complexities = {}
        self.trait_actor_associations = {self.generation:collections.defaultdict(dict)}
        self.actor_decision_evolutions = {self.generation:collections.defaultdict(dict)}

    def activate(self, outputs:typing.List[int]) -> int:
        '''majority voting'''
        return max(collections.Counter(outputs).items(), key=lambda x:x[1])[0]

    def update_trait_associations(self, a_name:str, a_traits:typing.List[int], a_id:int) -> None:
        if a_name not in self.trait_actor_associations[self.generation][str(a_traits)]:
            self.trait_actor_associations[self.generation][str(a_traits)][a_name] = set()

        self.trait_actor_associations[self.generation][str(a_traits)][a_name].add(a_id)

    def update_actor_evolutions(self, a1_name:str, a2_name:str, a2_traits:typing.List[int], a1_decision:int, a1_payout:int, a1_optimal:int) -> None:
        if a1_name not in self.actor_decision_evolutions[self.generation]:
            self.actor_decision_evolutions[self.generation][a1_name] = collections.defaultdict(dict)

        '''
        if str(a2_traits) not in self.actor_decision_evolutions[self.generation][a1_name]:
            self.actor_decision_evolutions[self.generation][a1_name][str(a2_traits)] = collections.defaultdict(int)
        
        self.actor_decision_evolutions[self.generation][a1_name][str(a2_traits)][str([a1_decision, a1_payout, a1_optimal])] += 1
        '''
        if a2_name not in self.actor_decision_evolutions[self.generation][a1_name]:
            self.actor_decision_evolutions[self.generation][a1_name][a2_name] = collections.defaultdict(int)

        self.actor_decision_evolutions[self.generation][a1_name][a2_name][a1_decision] += 1

    def run_interactions(self) -> None:
        print('-'*40)
        matrix_cache = {}
        for (a1, a2), [agent1, agent2, matrix] in self.interactions.items():
            for actor1 in agent1.population:
                self.update_trait_associations(a1, actor1.traits, actor1.id)
                for actor2 in agent2.population:
                    self.update_trait_associations(a2, actor2.traits, actor2.id)
                    a1_decision = self.activate(actor1.genotype(*actor2.traits))
                    a2_decision = self.activate(actor2.genotype(*actor1.traits))
                    actor1._outputs[tuple(actor2.traits)] = a1_decision
                    actor2._outputs[tuple(actor1.traits)] = a2_decision
                    a1_payout, a2_payout = matrix[a1_decision][a2_decision]
                    actor1.score += a1_payout
                    actor2.score += a2_payout
                    if (s_c:=str(matrix)) not in matrix_cache:
                        matrix_cache[s_c] = (max(a for row in matrix for a, _ in row), max(b for row in matrix for _, b in row))
                    
                    a_opt, b_opt = matrix_cache[s_c]
                    actor1.optimal_score += a_opt
                    actor2.optimal_score += b_opt

                    self.update_actor_evolutions(a1, a2, actor2.traits, a1_decision, a1_payout, a_opt)
                    self.update_actor_evolutions(a2, a1, actor1.traits, a2_decision, a2_payout, b_opt)
                    '''
                    if (k:=str((a1, a2))) not in self.generation_population_details[self.generation]:
                        self.generation_population_details[self.generation][k] = []
                
                    self.generation_population_details[self.generation][k].append({
                        a1:{
                            'id':actor1.id,
                            'traits':actor1.traits,
                            'decision':a1_decision,
                            'payout':a1_payout,
                            'optimal_payout':a_opt
                        },
                        a2:{
                            'id':actor2.id,
                            'traits':actor2.traits,
                            'decision':a2_decision,
                            'payout':a2_payout,
                            'optimal_payout':b_opt
                        }
                    })
                    '''
                    #print('score after', [actor1.score, actor2.score])

    def increment_generation(self) -> None:
        self.generation += 1
        self.trait_actor_associations[self.generation] = collections.defaultdict(dict)
        self.actor_decision_evolutions[self.generation] = collections.defaultdict(dict)

    def fitness_score_offsets(self, population:typing.List['Agent']) -> typing.List[float]:
        min_score = min(i.score for i in population)
        return [i.score + (abs(min_score) if min_score < 0 else 0) for i in population]

    def fractional_fitness_score(self, population:typing.List['Agent']) -> typing.List:
        return sorted([(i.score if i.score >= 0 else 0)/i.optimal_score for i in population])

    def compute_complexities(self, c_func:typing.Callable = statistics.median) -> None:
        self.generation_complexities[self.generation] = {
                a:{'complexity':c_func(sorted([i.complexity() for i in b.population])),
                    'fitness':c_func(self.fractional_fitness_score(b.population))}
            for a, b in self.agents.items()}

    def reproduction(self, control:bool = False) -> None:
        for a_name, agent in self.agents.items():
            min_score = min(i.score for i in agent.population)
            sum_fitness = sum(i.score + (abs(min_score) if min_score < 0 else 0) for i in agent.population)
            if not sum_fitness:
                #return 0, a_name
                sum_fitness = 1

            #print(a_name, [i.score for i in agent.population])
            #USE THE SAME SEED FOR RANDOM.CHOICE!!
            fitness_probability = [(i.score + (abs(min_score) if min_score < 0 else 0))/sum_fitness for i in agent.population]
            new_population = []
            for _ in range(agent.size):
                if not control:
                    try:
                        parent = copy.deepcopy(agent.population[np.random.choice(agent.size, p = fitness_probability)])
                    except:
                        print('got fitness issue', fitness_probability)
                        print('more error info', min_score, sum_fitness)
                        print([i.score for i in agent.population])
                        parent = copy.deepcopy(random.choice(agent.population))
                else:
                    parent = copy.deepcopy(random.choice(agent.population))

                parent.mutate()
                parent.score = 0
                parent.optimal_score = 0
                new_population.append(parent)

            agent.population = new_population

        return 1, None
                
    def plot_complexities(self, proc:int, cached:bool = False, suppress_plot:bool = False) -> None:
        if cached:
            with open('run_complexities.json') as f:
                self.generation_complexities = json.load(f)

        else:
            file_ext = f"{proc}_{str(datetime.datetime.now()).replace(' ', 'T').replace('.', '')}.json"
            with open(f"run_complexities_{file_ext}", 'a') as f:
                json.dump(self.generation_complexities, f)

            with open(f'generation_evolutions_{file_ext}', 'a') as f:
                json.dump({'trait_actor_associations':{a:{j:{K:len(J) for K, J in k.items()} for j, k in b.items()} for a, b in self.trait_actor_associations.items()}, 'actor_decision_evolutions':self.actor_decision_evolutions}, f)

        agent_complexities = collections.defaultdict(list)
        agent_fitness = collections.defaultdict(list)
        all_generations = []
        for generation, agents in self.generation_complexities.items():
            all_generations.append(generation)
            for agent, metrics in agents.items():
                if not isinstance(metrics, dict):
                    agent_complexities[agent].append(metrics)
                
                else:
                    agent_complexities[agent].append(metrics['complexity'])
                    agent_fitness[agent].append(metrics['fitness'])
            

        if not suppress_plot:
            for agent, complexities in agent_complexities.items():
                plt.plot(all_generations, complexities, label = agent)
            
            plt.xlabel('Generation')
            plt.ylabel('Median complexity')
            plt.title('Complexities')
            plt.legend()
            plt.show()

            if agent_fitness:
                for agent, fitness in agent_fitness.items():
                    plt.plot(all_generations, fitness, label = agent)
                
                plt.xlabel('Generation')
                plt.ylabel('Median fitness')
                plt.title('Fitness')
                plt.legend()
                plt.show()

    def graph(self) -> None:
        G = nx.Graph()
        for a, b in self.interactions:
            G.add_node(a)
            G.add_node(b)
            G.add_edge(a, b)
        
        nx.draw(G, with_labels = True, arrows = True)
        plt.show()

    def __enter__(self) -> 'Environment':
        return self
    
    def __exit__(self, *_) -> None:
        self.interactions = {}
        self.generation = 1
        for agent in self.agents.values():
            agent.population = [i.reset() for i in agent.population]
            agent.interactions = []

        return
    
    def agent(self, a_func:typing.Callable) -> 'Agent':
        _env_self = self
        class Agent:
            def __init__(self, a_func) -> None:
                self.name = a_func.__name__
                self.agent_details = a_func()
                self.interactions = []

            @property
            def population(self) -> typing.List['Actor']:
                return self.agent_details['population']

            @population.setter
            def population(self, new_population:typing.List['Actor']) -> None:
                self.agent_details['population'] = new_population

            @property
            def size(self) -> int:
                return self.agent_details['size']

            def __iter__(self) -> typing.Iterator:
                yield from self.population

            def interaction(self, agent:'Agent', payoff_matrix) -> None:
                self.interactions.append(agent)
                _env_self.interactions[(self.name, agent.name)] = [self, agent, payoff_matrix]
                _env_self.agents[self.name] = self
                _env_self.agents[agent.name] = agent
                 
            
            def __repr__(self) -> str:
                return f'<agent "{self.name}" pop_size={len(self.agent_details["population"])}>'

        return Agent(a_func)

if __name__ == '__main__':
    
    print('Protestor random trait', Protestor().traits)
    print('Police random trait', Police().traits)
    print('CounterProtestor random trait', CounterProtestor().traits)
    print('Public random trait', Public().traits)

    '''
    g = DEFAULT_GENOTYPE_1()
    g.render()
    for _ in range(10):
        g.render()
        g.mutate()
    g = DEFAULT_GENOTYPE_2()
    g.render()
    '''