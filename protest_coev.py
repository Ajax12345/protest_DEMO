import protest_actors as pa

env = pa.Environment()

@env.agent
def Protestors():
    return {'population': [pa.Protestor() for _ in range(50)], 'size':50}

@env.agent
def Police():
    return {'population': [pa.Police() for _ in range(50)], 'size':50}

@env.agent
def CounterProtestors():
    return {'population': [pa.CounterProtestor() for _ in range(50)], 'size':50}

@env.agent
def Public():
    return {'population': [pa.Public() for _ in range(50)], 'size':50}

Protestors.interaction(Police, [[(2, 2), (0, 3)], [(3, 0), (0, 0)]])
Protestors.interaction(Public, [[(0, 1), (0, 3)], [(1, 0), (2, 2)]])
Protestors.interaction(CounterProtestors, [[(1, 1), (0, 2)], [(2, 0), (0, 0)]])
Public.interaction(CounterProtestors, [[(0, 0), (1, 0)], [(2, 0), (1, 1)]])
CounterProtestors.interaction(Police, [[(0, 0), (0, 2)], [(2, 0), (2, 2)]])



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
    _ = simulate_generation((1, 1000), True)
    '''
    import concurrent.futures

    with concurrent.futures.ProcessPoolExecutor(max_workers = 5) as executor:
        _ = executor.map(simulate_generation, [(i, 1000) for i in range(5)])
    '''