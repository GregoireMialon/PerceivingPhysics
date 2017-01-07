import numpy as np


def find_pivot(f='../../data/m_hist.csv'):
    centers = np.loadtxt(f)

    xA = min(centers[:, 0])
    xB = max(centers[:, 0])

    xC = (xB - xA) / 2
    idx = np.argmin(np.abs(centers[:, 0] - xC))
    yC = centers[idx, 1]
    yA = np.mean(centers[np.where(centers[:, 0] == xA)[0], 1])
    yB = np.mean(centers[np.where(centers[:, 0] == xB)[0], 1])

    # Chercher Pivot P tel que xP = xC et PC = PB
    xP = xC
    yP = ((xC - xB) ** 2 + yB ** 2 - yC ** 2) / (2 * (yB - yC))

    L = abs(yP - yC)
    print("Length of the string :")
    print(L)
    print ("Coordinates of the pivot :")
    print([xP, yP])

    estimateLength = np.mean(np.sqrt((centers[:, 0] - xP) ** 2 + (centers[:, 1] - yP) ** 2))

    return estimateLength, (xP, yP), centers
