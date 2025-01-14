import numpy as np

def generate_balanced_growth(start, steps=10, seed=None):
    if seed is not None:
        np.random.seed(seed)
    traj = [start]
    for _ in range(1, steps):
        nxt = traj[-1] + (0.05 * np.random.randn() + 0.06)
        traj.append(min(max(2.0, nxt), 4.0))
    return traj

def generate_high_achiever(start, steps=10, seed=None):
    if seed is not None:
        np.random.seed(seed)
    traj = [start]
    for _ in range(1, steps):
        nxt = traj[-1] + (0.10 * np.random.randn() + 0.09)
        traj.append(min(max(2.0, nxt), 4.0))
    return traj

def generate_downfall_recovery(start, steps=10, seed=None):
    if seed is not None:
        np.random.seed(seed)
    traj = [start]
    for i in range(1, steps):
        nxt = traj[-1] - 0.1 * np.random.rand() if i < 4 else traj[-1] + 0.15 * np.random.rand()
        traj.append(min(max(2.0, nxt), 4.0))
    return traj

def generate_up_down(start, steps=10, seed=None):
    if seed is not None:
        np.random.seed(seed)
    traj = [start]
    for _ in range(1, steps):
        direction = 1 if np.random.rand() > 0.5 else -1
        nxt = traj[-1] + direction * (0.15 + 0.1 * np.random.rand())
        traj.append(min(max(2.0, nxt), 4.0))
    return traj

def generate_perfectionist(start, steps=10, seed=None):
    if seed is not None:
        np.random.seed(seed)
    traj = [start]
    for i in range(1, steps):
        nxt = traj[-1] - 0.15 * np.random.rand() if i in [3, 6] else traj[-1] + (0.08 + 0.07 * np.random.rand())
        traj.append(min(max(2.0, nxt), 4.0))
    return traj

def generate_consistent_improvement(start, steps=10, seed=None):
    if seed is not None:
        np.random.seed(seed)
    traj = [start]
    for _ in range(1, steps):
        nxt = traj[-1] + 0.07 + 0.02 * np.random.randn()
        traj.append(min(max(2.0, nxt), 4.0))
    return traj

def generate_chaotic(start, steps=10, seed=None):
    if seed is not None:
        np.random.seed(seed)
    traj = [start]
    for i in range(1, steps):
        nxt = traj[-1] + (0.2 * np.random.randn()) + 0.05 * ((-1) ** i)
        traj.append(min(max(2.0, nxt), 4.0))
    return traj

def generate_late_bloomer(start, steps=10, seed=None):
    if seed is not None:
        np.random.seed(seed)
    traj = [start]
    for i in range(1, steps):
        nxt = traj[-1] - 0.02 * np.random.rand() if i < 5 else traj[-1] + 0.15 + 0.05 * np.random.rand()
        traj.append(min(max(2.0, nxt), 4.0))
    return traj

def generate_spike_plateau(start, steps=10, seed=None):
    if seed is not None:
        np.random.seed(seed)
    traj = [start]
    for i in range(1, steps):
        nxt = traj[-1] + 0.25 + 0.05 * np.random.randn() if 3 <= i <= 5 else traj[-1] + 0.02 * np.random.randn()
        traj.append(min(max(2.0, nxt), 4.0))
    return traj

def generate_senioritis(start, steps=10, seed=None):
    if seed is not None:
        np.random.seed(seed)
    traj = [start]
    for i in range(1, steps):
        nxt = traj[-1] + 0.08 + 0.02 * np.random.randn() if i < 7 else traj[-1] - (0.1 * np.random.rand())
        traj.append(min(max(2.0, nxt), 4.0))
    return traj

def generate_no_study(start, steps=10, seed=None):
    if seed is not None:
        np.random.seed(seed)
    traj = [start]
    for _ in range(1, steps):
        nxt = traj[-1] - (0.05 + 0.05 * np.random.rand())
        traj.append(min(max(2.0, nxt), 4.0))
    return traj

def generate_burnout(start, steps=10, seed=None):
    if seed is not None:
        np.random.seed(seed)
    traj = [start]
    for i in range(1, steps):
        nxt = traj[-1] - (0.1 + 0.1 * np.random.rand()) if 3 <= i <= 5 else traj[-1] + (0.05 * np.random.randn())
        traj.append(min(max(2.0, nxt), 4.0))
    return traj

def generate_triumph_over_adversity(start, steps=10, seed=None):
    if seed is not None:
        np.random.seed(seed)
    traj = [start]
    for i in range(1, steps):
        nxt = traj[-1] - 0.05 * np.random.rand() if i < 4 else traj[-1] + 0.12 + 0.08 * np.random.rand()
        traj.append(min(max(2.0, nxt), 4.0))
    return traj
