import member
from typing import List, Tuple

class Scheduler:
    def __init__(self, meeting_time: int, team_members: List['member.TeamMember']):
        """Initialize with the desired meeting time in hours and the list of team members."""
        self.meeting_time = meeting_time  # meeting duration in hours
        self.team_members = team_members  # list of team members
    
    def find_optimal_meeting_time(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """ Find the optimal meeting time for one hour and the best time range/slot to meet """
        # initialize time slots (all 24 hours in UTC)
        time_slots = [0] * 24
        
        # if i had more time, i would optimize this section here
        # fill time slots with weighted availability
        for member in self.team_members:
            # calculate the seniority as 1.5 so we don't confuse a seniority of 2 for 2 people of seniority 1
            seniority_weight = 1.5 if member.seniority == 2 else member.seniority
            
            # Iterate over the UTC time range
            for start, end in member.get_utc():
                # add the seniority_weight to the appropriate time slots
                for hour in range(start, end):
                    time_slots[hour] += seniority_weight

        # variables to track the sliding window and results
        lpointer = 0  # left pointer for sliding window
        max_sum = 0   # max sum of most people available  
        max_value = 0 # max value of most people available

        temp_sum = time_slots[lpointer] # sum of people for current window
        
        optimal_range = (0, 1)   # optimal range of times
        optimal_time = 0         # optimal time to start (for one hour time)

        print(time_slots)

        # sliding window search
        for rpointer in range(1, 24):
           
            # add current rpointer time slot to the sum
            temp_sum += time_slots[rpointer]

            # move the lpointer to rpointer's current location if
            # the start/end time only has one person in it
            # because any subarrays from the current lpointer to the current rpointer will always be smaller
            # and we only care about if any other time ranges will be greater than the current one
            if time_slots[lpointer] <= 1.5 or time_slots[rpointer] <= 1.5:
                temp_sum = 0
                lpointer = rpointer
                continue

            # check for the optimal sum of people available
            if temp_sum > max_sum:
                max_sum = temp_sum
                optimal_range = (lpointer, rpointer) # updates the optimal range to the current subarray range
            
            # check for the new optimal single-hour time
            if time_slots[rpointer] > max_value:
                max_value = time_slots[rpointer]
                optimal_time = rpointer

        # returns both the optimal time range and optimal time
        return optimal_range, optimal_time


# Example usage:
# Assume the `TeamMember` class is defined in a module called `member`
# and that time zones have been correctly defined in `timezones`.

# Define team members with availability and seniority
member1 = member.TeamMember(name="Alice", availability=[(9, 11), (14, 16)], state="CA", seniority=2)
member2 = member.TeamMember(name="Bob", availability=[(10, 12), (13, 15)], state="NY", seniority=1)
member3 = member.TeamMember(name="Charlie", availability=[(15, 18), (11, 13)], state="TX", seniority=1)
member4 = member.TeamMember(name="David", availability=[(8, 10), (15, 19)], state="UT", seniority=1)
member5 = member.TeamMember(name="Eve", availability=[(7, 9), (12, 14)], state="FL", seniority=2)
member6 = member.TeamMember(name="Frank", availability=[(9, 11), (14, 16)], state="WA", seniority=3)
member7 = member.TeamMember(name="Grace", availability=[(13, 15), (16, 18)], state="AZ", seniority=2)
member8 = member.TeamMember(name="Hank", availability=[(6, 8), (12, 14)], state="MA", seniority=1)
member9 = member.TeamMember(name="Ivy", availability=[(10, 12), (15, 17)], state="NV", seniority=3)
member10 = member.TeamMember(name="Jack", availability=[(11, 13), (14, 17)], state="IL", seniority=1)

# Create the scheduler with a specific meeting duration in hours (e.g., 2 hours)
team = [member1, member2, member3, member4, member5, member6, member7, member8, member9, member10]
scheduler = Scheduler(meeting_time=2, team_members=team)

# Find the optimal meeting time
optimal_slots, optimal_time = scheduler.find_optimal_meeting_time()
print(f"The optimal meeting time in UTC is between {optimal_slots}, with the best hour-long meeting time at {optimal_time}:00")