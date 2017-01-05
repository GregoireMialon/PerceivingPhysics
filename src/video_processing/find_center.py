import numpy as np
import math
centers = np.loadtxt('centers.csv')

xA = min(centers[:,0])
xB = max(centers[:,0])

xC = xA + (xB - xA)/2
yC = np.mean(centers[np.where(centers[:,0] == xC)[0], 1])

yA = np.mean(centers[np.where(centers[:,0] == xA)[0], 1])
yB = np.mean(centers[np.where(centers[:,0] == xB)[0], 1])

# Chercher Pivot P tel que xP = xC et PC = PB
xP = xC
yP = ((xC - xB) ** 2 + yB ** 2 - yC ** 2) / (2 * (yB - yC))

L = abs(yP - yC)
print("Length of the string :")
print(L)
print ("Coordinates of the pivot :")
print([xP, yP])

estimateLength = np.mean(np.sqrt((centers[:,0] - xP) ** 2 + (centers[:,1] - yP ) ** 2))