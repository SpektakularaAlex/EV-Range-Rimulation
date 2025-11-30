# Electric Vehicle Range Simulation
**Numerical Methods · Scientific Computing · Python**

This project implements numerical algorithms to model the behaviour of an electric vehicle travelling along real-world routes. Given route data, energy consumption models, and time-dependent speed profiles, the program estimates travel time, energy usage, reachable distance, and simulates entire trips using classic numerical methods.

The project was completed as part of a course in Scientific Computing.

---

## Overview

The program uses numerical techniques to analyse a Tesla Roadster’s range along predefined routes. The following core components are implemented:

### **Numerical Methods Used**
- **Trapezoidal Rule**  
  - Travel time estimation  
  - Total energy consumption  
  - Convergence study (expected order: 2)

- **Newton–Raphson Method**  
  - Distance travelled within a given time  
  - Maximum reachable distance given battery capacity  

- **Explicit Euler Method**  
  - Solving the ODE  
    \[
    x'(t) = f(t, x),\quad x(t_0) = 0
    \]
  - Simulation of a 60 km route in New York with time-dependent speed profiles

- **PCHIP Interpolation**  
  - Creates a continuous velocity function from discrete route measurements

---

## 📁 Repository Structure

