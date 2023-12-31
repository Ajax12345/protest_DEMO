import protest_actors as pa

env = pa.Environment()

@env.agent
def Protestors():
    return {'population': [pa.Protestor(env) for _ in range(50)], 'size':50}

@env.agent
def Police():
    return {'population': [pa.Police(env) for _ in range(50)], 'size':50}

@env.agent
def CounterProtestors():
    return {'population': [pa.CounterProtestor(env) for _ in range(50)], 'size':50}

@env.agent
def Public():
    return {'population': [pa.Public(env) for _ in range(50)], 'size':50}

'''
Protestors.interaction(Police, [[(1, 0), (0, 1)], [(3, -2), (1, 1)]])
Protestors.interaction(Public, [[(-3, -3), (-2, 0)], [(1, -2), (3, 3)]])
Protestors.interaction(CounterProtestors, [[(2, 1), (0, 1)], [(2, -1), (3, 3)]])
Public.interaction(CounterProtestors, [[(1, -1), (0, -1)], [(-1, 0), (3, 3)]])
CounterProtestors.interaction(Police, [[(-3, -3), (-1, 1)], [(1, -1), (3, 3)]])
'''
'''
Protestors.interaction(Police, [[(-3, -3), (3, 3)], [(3, 3), (-3, -3)]])
Protestors.interaction(Public, [[(3, 3), (-3, -3)], [(-3, -3), (3, 3)]])
Protestors.interaction(CounterProtestors, [[(-3, -3), (3, 3)], [(3, 3), (-3, -3)]])
Public.interaction(CounterProtestors, [[(3, 3), (-3, -3)], [(-3, -3), (3, 3)]])
CounterProtestors.interaction(Police, [[(3, 3), (-3, -3)], [(-3, -3), (3, 3)]])
'''

Protestors.interaction(Police, [[(2, 1), (-1, 2)], [(2, -2), (-1, 2)]])
Protestors.interaction(Public, [[(-2, -1), (-2, 2)], [(2, -2), (3, 3)]])
Protestors.interaction(CounterProtestors, [[(1, 1), (-1, 2)], [(2, -1), (2, 1)]])
Public.interaction(CounterProtestors, [[(2, 1), (0, 1)], [(-1, -1), (-1, 2)]])
CounterProtestors.interaction(Police, [[(-1, -1), (-1, 1)], [(2, -1), (2, 2)]])


def simulate_generation(gen_num:int, control:bool) -> bool:
    for i in range(gen_num[1]):
        print(f'generation #{i+1}')
        env.run_interactions()
        env.compute_complexities()
        if not (rep_response:=env.reproduction(control))[0]:
            print(f'{rep_response[1]} scores converged to 0')
            break

        env.increment_generation()
    
    env.plot_complexities(gen_num[0])

    return True

if __name__ == '__main__':
    _ = simulate_generation((1, 5000), True)
    '''
    import concurrent.futures

    with concurrent.futures.ProcessPoolExecutor(max_workers = 5) as executor:
        _ = executor.map(simulate_generation, [(i, 1000) for i in range(5)])
    '''
    