import numpy as np
from scipy import interpolate
from scipy.integrate import trapezoid
import matplotlib.pyplot as plt
import route_nyc as rn

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
    
    a1 = 546.8
    a2 = 50.31
    a3 = 0.2584
    a4 = 0.008210
    
    c = a1 * v**(-1) + a2 + a3*v + a4 * v**(2)
    
    return c


    #raise NotImplementedError('consumption not implemented yet!')

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
    v = interpolate.pchip_interpolate(distance_km, speed_kmph,x)
    return v







### PART 2A ###
def time_to_destination(x, route, n):
    
    def f(z):
        return 1/(velocity(z, route))

    h = x/n
    y = np.linspace(0, x, n+1)
    f_x_arr_1 = f(y)
    I = h * (np.sum(f_x_arr_1) - (f_x_arr_1[0] + f_x_arr_1[-1]) / 2)
    
    return I
    raise NotImplementedError('time_to_destination not implemented yet!')



def Check_suitable_n(x, route, tol, function): 
    n = 1

    I_exakt = function(x, route, 10000000) * 60
    print(I_exakt)
    
    while abs(I_exakt - (function(x, route, n)*60 )) > tol:
        
        if abs(I_exakt - (function(x, route, n))*60) > tol*4:
            n += 30
        elif abs(I_exakt - (function(x, route, n))*60) > tol*2:
            n += 10
        elif abs(I_exakt - (function(x, route, n))*60) < tol*2:
            n += 1
            
    print(function(x, route, n)*60)
    return n



tot_dist_anna, _ = load_route('speed_anna')
tot_dist_elsa, _ = load_route('speed_elsa')




'<----För Anna tar det ca 41 minuter att fördas hela sträckan (lämpligt n = 316 med feltolerand 0.5)----->'
#print(time_to_destination(tot_dist_anna[-1], "speed_anna", 10000000) * 60)
#print(time_to_destination(tot_dist_anna[-1], "speed_anna", 316) * 60)


'<----För Elsa tar det ca 57.6 minuter att fördas hela sträckan (lämpligt n = 443) med feltolerans 0.3----->'
#print(time_to_destination(tot_dist_elsa[-1], "speed_elsa", 443) * 60)
#print(time_to_destination(tot_dist_elsa[-1], "speed_elsa", 10000000) * 60)



### PART 2B ###
def total_consumption(x, route, n):
    
    def f_in(x):
       return consumption(velocity(x, route))
    
    h = x/n
    z = np.linspace(0, x, n+1)
    fx_arr = f_in(z)
    I = h*( np.sum(fx_arr) - ( fx_arr[0] + fx_arr[-1]) / 2)
    return I
    raise NotImplementedError('total_consumption not implemented yet!')







'<------Anna behöver ca 11925.3 wattimmar för att ta sig fram n=1267 ----->'
#print(total_consumption(tot_dist_anna[-1], "speed_anna", 1267))
#print(total_consumption(tot_dist_anna[-1], "speed_anna", 10000000))
#print(Check_suitable_n(tot_dist_anna[-1], "speed_anna", 0.97))


'<------Elsa behöver ca 8012.8 wattimmar för att ta sig fram n=1323----->'
#print(total_consumption(tot_dist_elsa[-1], "speed_elsa", 1323))
#print(Check_suitable_n(tot_dist_elsa[-1], "speed_elsa", 0.28))



### PART 2C ###

'Vi tar och undersöker nogrannhetsordningen för total_consumption'
'Vi sätter ett I med n=10000000 som våran sanna I'
n_check = 1000000

I_true = total_consumption(tot_dist_anna[-1], "speed_anna", 10000000)
I_check = total_consumption(tot_dist_anna[-1], "speed_anna", n_check)
#print(f"Felmarginal med n = {n_check} => {abs(I_true - I_check)}")

def konvergens_studie():
    
    delint = 6
    
    #x = np.linspace(0, tot_dist_anna[-1], delint)
    n = np.arange(0, delint, 1)
    
    n_vals = 10000*(2**np.arange(delint))
    
    
    inspected_arr = np.array(abs(I_true - np.array([total_consumption(tot_dist_anna[-1], "speed_anna", n) for n in n_vals] )))
    #inspected_arr = abs(I_true - np.array(total_consumption_chat(tot_dist_anna[-1], "speed_anna", n_vals) ))
    #print(inspected_arr)
    #inspected_arr_2 = [(abs(I_true - total_consumption(tot_dist_anna[-1], "speed_anna", 2**i))) for i in range(delint) ]
    
    
    
    E =  1e7*(1 / (n_vals**2))
    print(E)
    
    plt.loglog(n_vals, E, c='red', label="Hjälplinje vid noggrannhetsordning 2")
    
    plt.loglog(n_vals, inspected_arr, c='blue', label="Trapetsmetodens fel")
    
    
    
    plt.title('Konvergensstudie')
    plt.xlabel('Delintervall [n]')
    plt.ylabel('Integrationsfel [Wh]')
    
    plt.legend()
    plt.show()


konvergens_studie()

def distance(T, route):
    #Vi börjar definera våran startgissning
    #En lämplig startgissning skulle exempelvis kunna vara medelvärdet av hastigheten gånger tiden t
    
    def startgiss(T):
        tot_dist, _ = load_route(route)
        x_arr = np.arange(0, tot_dist[-1]) 
        vel_med = sum(velocity(x_arr, route)) / tot_dist[-1]
        
        return vel_med*T
    
    x = startgiss(T)
    print(f"Startgissning x = {x}")
    tol = 1e-4 
    i = 0
    
    #Vi bestämmer 100 då det ej ska behöva itereras mer än 100 gånger då sträckan < 100
    while i < 100:
        f_x = time_to_destination(x, route, 10000000) - T
        f_der_x = 1/ velocity(x, route)
        #vel = velocity(x, route)
        
       #Bestämmer x_n+1 enligt Newton Raphsons metod
        x_ny = x - ( f_x * (1 / f_der_x) )
        
        
        if abs(x_ny - x) < tol:
            return x_ny
        
        #uppdaterar x om ej sant
        x = x_ny
        i += 1




def plot_time_to_dest_fun():
    x = np.arange(0, 65)
    tlist_anna = np.zeros(65)
    tlist_elsa = np.zeros(65)
    for i in x:
        tlist_anna[i] = time_to_destination(i, "speed_anna", 100000)
        tlist_elsa[i] = time_to_destination(i, "speed_elsa", 100000)
    
    T_tid = 0.5    
    tlist_anna = tlist_anna - T_tid
    tlist_elsa = tlist_elsa - T_tid
    
    plt.title("T(x) - T [h]", fontsize=25)
    plt.xlabel("Sträcka [km]", fontsize=15)
    plt.ylabel(f"Tiden T - {T_tid} [h]", fontsize=15)
    
    plt.scatter(x, tlist_anna, s=4, c="blue", zorder=2, label="Anna")
    plt.plot(x, tlist_anna, c="lightblue", zorder=1)
    
    plt.scatter(x, tlist_elsa, s=4, c="red", zorder=2, label="Elsa")
    plt.plot(x, tlist_elsa, c="orange", zorder=1)
    
    plt.legend()
    plt.show()



"<-------Anna färdas ungefär 51 km------>"
#print(distance(0.5, "speed_anna"))

"<-------Elsa färdas ungefär 37 km------>"
#print(distance(0.5, "speed_elsa"))





### PART 3B ###
def reach(C, route):
    #Nu måste vi hitta en ny metod för bestämning av startgissning
    #På liknande vis tar vi medelvärdet av consumptionen och delar C med funna medelvärdet
    
    tot_dist, _ = load_route(route)
    
    def cons_medel(C):
        x_arr = np.arange(0, tot_dist[-1])
        cons_med = sum(consumption(velocity(x_arr, route))) / tot_dist[-1]
        StartGiss = C / cons_med
        return StartGiss
    
    x = cons_medel(C)
    #x = 30
    print(f"Startgissning x={x}")
    tol = 1e-4
    
    for i in range(100):
        if x >= tot_dist[-1]:
            return tot_dist[-1]
        f_x = total_consumption(x, route, 10000000) - C
        f_der_x = consumption(velocity(x, route))
        
        x_ny = x - (f_x)/(f_der_x)
        
        if abs(x_ny - x) < tol:
            return x_ny
        x = x_ny
    
    raise NotImplementedError('reach not implemented yet!')




def plot_reach_fun():
    
    x = np.arange(0, 65)
    Cons_list_anna = np.zeros(65)
    Cons_list_elsa = np.zeros(65)
    for i in x:
        Cons_list_elsa[i] = total_consumption(i, "speed_elsa", 100000)
        Cons_list_anna[i] = total_consumption(i, "speed_anna", 100000)
    
    C_cons = 10000    
    Cons_list_anna = Cons_list_anna - C_cons
    Cons_list_elsa = Cons_list_elsa - C_cons
    
    plt.title("C(x) - C [Wh]", fontsize=25)
    
    
    
    plt.xlabel("Sträcka [km]", fontsize=15)
    plt.ylabel(f"Consumptionen C(x) - {C_cons} [Wh]", fontsize=15)
    
    
    
    plt.scatter(x, Cons_list_elsa, s=4, c="red", zorder=2, label="Elsa")
    plt.plot(x, Cons_list_elsa, c="orange", zorder=1)
    
    
    plt.scatter(x, Cons_list_anna, s=4, c="blue", zorder=2, label="Anna")
    plt.plot(x, Cons_list_anna, c="lightblue", zorder=1)
    
    plt.legend()
    plt.show()
        

        
    
    
    
    
    
        
        
        
