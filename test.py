import math

xclockpos = 400
ycenter = 400
seconds_radius = 50
angle = 180


def rotate(origin, points, angle):
    ox, oy = origin
    rotatedPoints = []
    for point in points:
        px, py = point

        qx = ox + math.cos(math.radians(angle)) * (px - ox) - math.sin(math.radians(angle)) * (py - oy)
        qy = oy + math.sin(math.radians(angle)) * (px - ox) + math.cos(math.radians(angle)) * (py - oy)
        rotatedPoints.append((qx, qy))

    return rotatedPoints

secondHand = [(xclockpos + 10, ycenter), (xclockpos - 10, ycenter), (xclockpos, ycenter - seconds_radius + 20)]

transformedSecondHand = rotate((xclockpos, ycenter), secondHand, angle)

print(secondHand)
print(transformedSecondHand)