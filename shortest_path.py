from Graphs import Graph, Vertex
from math import cos, asin, sqrt, pi

# location = (longitude, latitude)
# Ranges that are within Austin are Langitude(30.1378, 30.5135)
# and Longitude (-97.9851, -97.5678)
air_loc = (-97.6799, 30.1831)
mus_loc = (-97.7614, 30.3185)
stp_loc = (-97.7580, 30.2730)
shp_loc = (-97.7620, 30.3906)
# htl_loc = (-97.7429, 30.2676)

#Made a distance calulator between two point of latitude and longitude 
#Using haversine function.
def dst(loc1, loc2):
  lon1, lat1 = loc1
  lon2, lat2 = loc2
  p = pi/180
  a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p)*(1-cos((lon2-lon1)*p))/2
  return 12742*asin(sqrt(a))
   
#To solve Calculation of shortest path of the graph we use a vairation of Traveling Salesman Problem (tsp) called the Halmiltonian path problem (hpp). 
#This variant starts at a vertex then visits each other vertex once until 
#its ends at the target vertex.
def build_graph(htl_loc, directed = False):
  g = Graph(directed)
  vertices = []
  for val in ['Hotel', 'Camp Mabry', 'Great Hills', '6th Street']:
    vertex = Vertex(val)
    vertices.append(vertex)
    g.add_vertex(vertex)
  htl_mus = dst(htl_loc, mus_loc)
  htl_shp = dst(htl_loc, shp_loc)
  htl_stp = dst(htl_loc, stp_loc)
  g.add_edge(vertices[0], vertices[1], htl_mus)
  g.add_edge(vertices[0], vertices[2], htl_shp)
  g.add_edge(vertices[0], vertices[3], htl_stp)
  g.add_edge(vertices[1], vertices[2], dst(shp_loc, mus_loc))
  g.add_edge(vertices[2], vertices[3], dst(stp_loc, shp_loc))
  g.add_edge(vertices[1], vertices[3], dst(mus_loc, stp_loc))
  return g
# print( dst(htl_loc, mus_loc), dst(htl_loc, shp_loc), dst(htl_loc, stp_loc), 
#       dst(shp_loc, mus_loc), dst(stp_loc, shp_loc), dst(mus_loc, stp_loc))
def check_visited(visited_vertices):
  for vertex in visited_vertices:
    if visited_vertices[vertex] == "unvisited":
      return False

  return True

def traveling_salesperson(graph,start):
  ts_path = ""
  visited_vertices = {}
  for vertex in graph.graph_dict:
    visited_vertices[vertex] = "unvisited"

  current_vertex = start
  visited_vertices[current_vertex] = "visited"
  ts_path += current_vertex 
  visited_all_vertices = check_visited(visited_vertices)
  while not visited_all_vertices:
    current_vertex_edges = graph.graph_dict[current_vertex].get_edges()
    current_vertex_edge_weights = {}
    for edge in current_vertex_edges:
      current_vertex_edge_weights[edge] = graph.graph_dict[current_vertex].get_edge_weight(edge)

    found_next_vertex = False
    next_vertex = ""
    while not found_next_vertex:
      if not current_vertex_edge_weights:
        break

      next_vertex = min(current_vertex_edge_weights, key=current_vertex_edge_weights.get)
      if visited_vertices[next_vertex] == "visited":
        current_vertex_edge_weights.pop(next_vertex)
      else:
        found_next_vertex = True

    if not current_vertex_edge_weights:
      visited_all_vertices = True

    else:
      current_vertex = next_vertex
      visited_vertices[current_vertex] = "visited"
      ts_path += '-->'+current_vertex
      
    visited_all_vertices = check_visited(visited_vertices)

  print(ts_path)

def hamiltonian_path(graph, start, target):
  ts_path = []
  visited_vertices = {}
  for vertex in graph.graph_dict:
    visited_vertices[vertex] = "unvisited"

  current_vertex = start
  visited_vertices[current_vertex] = "visited"
  ts_path.append(current_vertex) 
  visited_all_vertices = check_visited(visited_vertices)
  while not visited_all_vertices:
    current_vertex_edges = graph.graph_dict[current_vertex].get_edges()
    current_vertex_edge_weights = {}
    for edge in current_vertex_edges:
      current_vertex_edge_weights[edge] = graph.graph_dict[current_vertex].get_edge_weight(edge)

    found_next_vertex = False
    next_vertex = ""
    if len(ts_path)+1 == len(graph.graph_dict):
      visited_vertices[target] = "visited"
      ts_path.append(target)
      visited_all_vertices = True
      
    while not found_next_vertex:
      if not current_vertex_edge_weights:
        break

      next_vertex = min(current_vertex_edge_weights, key=lambda edge: current_vertex_edge_weights.get(edge) if edge != target else 100 )
      if visited_vertices[next_vertex] == "visited":
        current_vertex_edge_weights.pop(next_vertex)
      else:
        found_next_vertex = True

    if not current_vertex_edge_weights:
      visited_all_vertices = True

    else:
      current_vertex = next_vertex
      visited_vertices[current_vertex] = "visited"
      ts_path.append(current_vertex)
      
    visited_all_vertices = check_visited(visited_vertices)

  return ts_path

def cal_path(htl_loc):
  graph = build_graph(directed = False, htl_loc = htl_loc)
  return hamiltonian_path(graph, 'Hotel', '6th Street')