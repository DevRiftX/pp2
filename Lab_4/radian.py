import math

# 2
height = int(input("Height: "))
base1 = int(input("Base, first value: "))
base2 = int(input("Base, second value: "))

area = (base1 + base2)/2*height

print(f"Expected output: {area}")

# 3 
sides = int(input("Input number of sides: "))
length = int(input("Input the length of a side: "))
apothem = length/(2 * math.tan(180/sides))
area = sides * length * apothem / 2

print(f"The area of the polygon is: {area}")