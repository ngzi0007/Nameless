"""
Created on Wed Apr 22 08:00:26 2020
@author: weetee
"""

from __future__ import print_function
import math
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from params import DataModel

def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    total_distance = 0
    route_soln = {}
    plan_outputs = ''
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_path = []
        while not routing.IsEnd(index):
            loc_index = manager.IndexToNode(index)
            
            if loc_index != 0:
                plan_output += ' {} -> '.format(loc_index)
                route_path.append(loc_index)
            
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        
        route_soln[vehicle_id] = route_path
        
        #if loc_index != 0:
        #    plan_output += '{}\n'.format(loc_index)
        plan_output += 'Distance of the route: {} km\n'.format(route_distance)
        plan_outputs = plan_outputs + '\n' + plan_output
        total_distance += route_distance
    print(plan_outputs)
    print('Total Distance of all routes: {} km'.format(total_distance))
    return route_soln, plan_outputs

def main_solver(data):
    """Entry point of the program."""
    # Instantiate the data problem.

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Define cost of each arc.
    def distance_callback(from_index, to_index):
        """Returns the manhattan distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'Distance to delivery point'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        math.ceil(data['max_dist']),  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Define Transportation Requests.
    for request in data['pickups_deliveries']:
        pickup_index = manager.NodeToIndex(request[0])
        delivery_index = manager.NodeToIndex(request[1])
        routing.AddPickupAndDelivery(pickup_index, delivery_index)
        routing.solver().Add(
            routing.VehicleVar(pickup_index) == routing.VehicleVar(
                delivery_index))
        routing.solver().Add(
            distance_dimension.CumulVar(pickup_index) <=
            distance_dimension.CumulVar(delivery_index))

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    print(solution, '\n')
    if solution:
        route_soln = print_solution(data, manager, routing, solution)
    else:
        route_soln = None, 'No solution found.'
    return route_soln

if __name__ == '__main__':
    dm = DataModel()
    data = dm.data
    route_soln, plan_outputs = main_solver(data=data)