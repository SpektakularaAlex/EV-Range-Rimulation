import numpy as np
from scipy import interpolate
import roadster

def load_route(route):
    """ 
    Get speed data from route .npz-file. Example usage:

      distance_km, speed_kmph = load_route('speed_anna.npz')
    
    The route file should contain two arrays, distance_km and 
    speed_kmph, of equal length with position (in km) and speed 
    (in km/h) along route. Those two arrays are returned by this 
    convenience function.
    """
    # Read data from npz file
    if not route.endswith('.npz'):
        route = f'{route}.npz' 
    data = np.load(route)
    distance_km = data['distance_km']
    speed_kmph = data['speed_kmph']    
    return distance_km, speed_kmph

def save_route(route, distance_km, speed_kmph):
    """ 
    Write speed data to route file. Example usage:

      save_route('speed_olof.npz', distance_km, speed_kmph)
    
    Parameters have same meaning as for load_route
    """ 
    np.savez(route, distance_km=distance_km, speed_kmph=speed_kmph)

### PART 1A ###
def consumption(v):
    
    c = 546.8 * v**(-1) + 50.31 + 0.2584 * v + 0.008210 * v**2

    return c



### PART 1B ###
def velocity(x, route):
    # ALREADY IMPLEMENTED!
    """
    Interpolates data in given route file, and evaluates the function
    in x
    """
    # Load data
    distance_km, speed_kmph = load_route(route)
    # Check input ok?
    assert np.all(x>=0), 'x must be non-negative'
    assert np.all(x<=distance_km[-1]), 'x must be smaller than route length'
    # Interpolate
    v = interpolate.pchip_interpolate(distance_km, speed_kmph, x)
    return v


### PART 2A ###
def time_to_destination(x, route, n):
    
    s_array = np.linspace(0, x, n+1)

    integrand = 1/velocity(s_array, route)

    integrand[1:-1] *= 2

    h = x/n
    T = h/2 * sum(integrand)

    return T


### PART 2B ###


def total_consumption(x, route, n):

    s_array = np.linspace(0, x, n+1)

    v = velocity(s_array, route)
    integrand = consumption(v)

    integrand[1:-1] *= 2

    h = x/n
    E = h/2 * sum(integrand)

    return E

    
### PART 3A ###
def distance(T, route):

    n = 100000
    tol = 1e-4
    x = T / (time_to_destination(load_route(route)[0][-1], route, n) / load_route(route)[0][-1])   #startgissning
    print(f"Startgissning: x = {round(x, 4)} km")
    def f(x, route, n):
        return time_to_destination(x, route, n) - T         #icke-linjär ekvation vars rot ger tillryggalagd sträcka x efter T timmar
    
    def df(x, route):
        return 1/velocity(x, route)             #derivatan av f

    #NEWTON RAPHSONS METOD
    delta_x = 2 * tol                     #låter delta_x börja på ett värde som är större än toleransen
    while abs(delta_x) >= tol:            #loopar så länge vi är inte uppnår önskad tolerans
        delta_x = -f(x, route, n)/df(x, route)
        x = x + delta_x
    return x


### PART 3B ###
def reach(C, route):

    n = 100000
    tol = 1e-4
    x = C / (total_consumption(load_route(route)[0][-1], route, n) / load_route(route)[0][-1])   #startgissning
    print(f"Startgissning: x = {round(x, 4)} km")

    def f(x, route, n):
        return total_consumption(x, route, n) - C
    
    def df(x, route):
        return consumption(velocity(x, route))

    #NEWTON RAPHSONS METOD
    delta_x = 2 * tol                           #även här startar vi på ett värde större än önskad tolerans
    while abs(delta_x) >= tol:
        if x >= load_route(route)[0][-1]:       #om approximerad sträcka överstiger ruttens totala längd returnerar vi ruttens totala längd
            return load_route(route)[0][-1]
        else:
            delta_x = -f(x, route, n)/df(x, route)
            x = x + delta_x
    return x