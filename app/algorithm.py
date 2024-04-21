import concurrent.futures
import heapq
import threading
from math import radians, sin, cos, sqrt, atan2
from collections import defaultdict

class Cargo:
  def __init__(self, id, src, dest, weight,volume):
    self.id = id
    self.src = src
    self.dest = dest
    self.weight = weight
    self.volume = volume

class Vehicle:
  def __init__(self, id, location, capacity_mass, capacity_volume):
    self.id = id
    self.location = location
    self.capacity_mass = capacity_mass
    self.capacity_volume = capacity_volume
    self.current_mass = 0
    self.current_volume = 0

cargos = [
    Cargo(1, (40.7128, -74.0060), (34.0522, -118.2437), 10, 10),
    Cargo(2, (51.5074, -0.1278), (40.7128, -74.0060), 20, 20),
    Cargo(3, (34.0522, -118.2437), (51.5074, -0.1278), 30, 30),
]

def create_cargos_graph(cargos):
  graph = {}

  for cargo in cargos:
    graph[cargo.id] = ({
      "lat" : cargo.src[0],
      "long" : cargo.src[1],
      "type" : "src",
      "picked_up" : False
    },
    {
      "lat" : cargo.dest[0],
      "long" : cargo.dest[1],
      "type" : "dest",
      "delivered" : False
    })

  distances = {}
  for point1 in graph.items():
    for point2 in graph.items():
      if point1 != point2:
        p1_src = (graph[point1][0]["lat"], graph[point1][0]["long"])
        p1_dest = (graph[point1][1]["lat"], graph[point1][1]["long"])
        p2_src = (graph[point2][0]["lat"], graph[point2][0]["long"])
        p2_dest = (graph[point2][1]["lat"], graph[point2][1]["long"])
        distances[(point1,point2)] =(
          calculate_distance(p1_src, p2_src),
          calculate_distance(p2_src, p2_dest),
          calculate_distance(p2_dest, p1_dest),
          calculate_distance(p1_dest, p2_dest),
        )

  return graph

def create_vehicle_graph(vehicles):
  graph = defaultdict(dict)
  for vehicle in vehicles:
    graph[vehicle.location].append(vehicle.id)
  return graph


def calculate_distance(point1, point2):
  lat1,long1 = map(radians,point1)
  lat2,long2 = map(radians,point2)

  dlong = long2 - long1
  dlat = lat2 - lat1
  a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlong/2)**2
  c = 2 * atan2(sqrt(a), sqrt(1 - a))
  distance = 6373.0 * c
  return distance

def process_vehicle(vehicle, orders,lock):
   pass

def assign_vehicle_to_cargos(cargos, vehicles):
   lock = threading.lock()
   with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
      for vehicle in vehicles:
         executor.submit(process_vehicle, vehicle, cargos,lock)



def main():
  cargos_graph = create_cargos_graph(cargos)
  print(cargos_graph)


if __name__ == '__main__':
    main()