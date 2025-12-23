
import math

# Task 5: Extending a class
class Point:
  # a point representing a point in 2D space
  def __init__(self, x, y):
    self.x = x
    self.y = y

  # string...
  def __str__(self):
    return f"Point({self.x}, {self.y})"
  
  # equality...
  def __eq__(self, other):
    # compare points or subclasses of points
    if not isinstance(other, Point):
      return NotImplemented
    return self.x == other.x and self.y == other.y
  
  # euclidean...
  def distance_to(self, other):
    if not isinstance(other, Point):
      raise TypeError("distance_to expects a Point (or subclass).")
    
    dx = other.x - self.x
    dy = other.y - self.y
    return math.sqrt(dx * dx + dy * dy)
  

  # Vector class
class Vector(Point):
  # inherits __int__ from Point
    
  # override string representation for vectors
  def __str__(self):
    return f"Vector<{self.x}, {self.y}>"
    
  # override + operator for vector addition
  def __add__(self, other):
    if not isinstance(other, Vector):
      return NotImplemented
    return Vector(self.x + other.x, self.y + other.y)
  

if __name__ == "__main__":
  p1 = Point(0, 0)
  p2 = Point(3, 4)
  p3 = Point(3, 4)

  print("Point printing:")
  print(p1)
  print(p2)

  print("\nPoint equality:")
  print(p2 == p3) #true
  print(p1 == p2) #false

  print("\nPoint distance:")
  print(p1.distance_to(p2)) #should be 5.0

  # Vector features
  v1 = Vector(1, 2)
  v2 = Vector(3, 4)

  print("\nVector printing:")
  print(v1)
  print(v2)

  print("\nVector addition:")
  v3 = v1 + v2
  print(v3)
  print("v3 is a vector:", isinstance(v3, Vector))
