import numpy as np

def transformation(Vx, Vy, W, Lenght):
    O1 = np.pi / 3
    O2 = np.pi / 6
    coefficients1 = np.zeros((3, 3), dtype=float)
    velocities = np.array((Vx, Vy,W), dtype=float)
    coefficients1[0] = [0.0, 1.0, Lenght]
    coefficients1[1] = [-np.sin(O1), -np.cos(O1), Lenght]
    coefficients1[2] = [np.cos(O2), -np.sin(O2),Lenght]
    return np.round(np.dot(coefficients1, velocities), 10)



