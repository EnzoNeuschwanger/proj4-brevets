"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#

brevet_distances = [0, 200, 400, 600, 1000, 1300]

min_speed = [0, 15.0, 15.0, 15.0, 11.428, 13.333]

max_speed = [0, 34.0, 32.0, 30.0, 28.0, 26.0]


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    #Handle erronious values
    if(control_dist_km < 0):
        return "NEGATIVE_DISTANCE"
    
    if brevet_dist_km not in brevet_distances:
        return "INCORRECT_BREVET"

    #Handle some of the edge cases first before calculating
    if(control_dist_km == 0.0):     # Control Distances at 0 always have an open time of 0
        return brevet_start_time.isoformat()

    if(control_dist_km > brevet_dist_km): # Any control distances larger than the brevet distance are treated as the brevet distance
        control_dist_km = brevet_dist_km

    previous_times = 0.0 
    left_over_dist = control_dist_km

    #Find our brevet_distance we're in 
    brevet_index = 1
    while(control_dist_km > brevet_distances[brevet_index]):
        previous_times += (brevet_distances[brevet_index] - brevet_distances[brevet_index-1])/max_speed[brevet_index]
        left_over_dist -= (brevet_distances[brevet_index] - brevet_distances[brevet_index-1])
        brevet_index += 1
    shift_time = previous_times + left_over_dist/max_speed[brevet_index]
    opening_time = brevet_start_time.shift(hours=+shift_time)
    return opening_time.isoformat()

closing_times = []

def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    
    #Handle erronious values
    if(control_dist_km < 0):
        return "NEGATIVE_DISTANCE"

    if brevet_dist_km not in brevet_distances:
        return "INCORRECT_BREVET"

    

    #Handle some of the edge cases first before calculating
    if(control_dist_km == 0.0):     # Control Distances at 0 always have a close time of 1 hour
        return brevet_start_time.shift(hours=1.0).isoformat()

    if(control_dist_km > brevet_dist_km): # Any control distances larger than the brevet distance are treated as the brevet distance
        control_dist_km = brevet_dist_km

    if(control_dist_km == 200.0 and brevet_dist_km == 200.0): #End time for a 200 Brevet is always 13:20 
        return brevet_start_time.shift(hours=13.5).isoformat()

    if(control_dist_km == 400.0 and brevet_dist_km == 400.0): #End time for a 400 Brevet is always 27:00
        return brevet_start_time.shift(hours=27.0).isoformat()

    if(control_dist_km < 60.0): #Times less than 60 use this formula for closing times
        return brevet_start_time.shift(hours=(control_dist_km/20 + 1)).isoformat()
    
    previous_times = 0.0 
    left_over_dist = control_dist_km 

    #Find our brevet_distance we're in 
    brevet_index = 1
    while(control_dist_km > brevet_distances[brevet_index]):
        previous_times += (brevet_distances[brevet_index] - brevet_distances[brevet_index-1])/min_speed[brevet_index]
        left_over_dist -= (brevet_distances[brevet_index] - brevet_distances[brevet_index-1])
        brevet_index += 1


    shift_time = previous_times + left_over_dist/min_speed[brevet_index]
    closing_time = brevet_start_time.shift(hours=+shift_time)
    return closing_time.isoformat()
