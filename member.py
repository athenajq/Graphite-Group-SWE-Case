from typing import List, Tuple
import timezones
class TeamMember:
   def __init__(self, name: str, availability: List[Tuple[int, int]], state: str, seniority: int):
       self.name = name
       self.availability = availability
       self.state = state
       self.seniority = seniority
       self.utc_availability = []
       self.utc_availability = self.get_utc()
  
   def getName(self) -> str:
       """Return the name of the team member."""
       return self.name


   def getAvailability(self) -> List[Tuple[int, int]]:
       """Return the availability of the team member."""
       return self.availability


   def getState(self) -> int:
       """Return the state of the team member."""
       return self.state


   def getSeniority(self) -> int:
       """Return the seniority of the team member, which is based on seniority."""
       return self.seniority


   def __repr__(self) -> str:
       return (f"TeamMember(name={self.name}, "
               f"availability={self.availability}, "
               f"state={self.state}, "
               f"seniority={self.seniority})")
   
   def get_utc(self):
        """ Return the availability of the team member in UTC """

        # only calculate the utc times if we haven't already before
        if len(self.utc_availability) == 0:
            conversion = 0
            zone = timezones.state_time_zones[self.state]
            
            # set conversion rates for different time zones
            if zone == "Pacific":
                conversion = 7
            elif zone == "Mountain":
                conversion = 6
            elif zone == "Central":
                conversion = 5
            elif zone == "Eastern":
                conversion = 4
            
            # change each availability to utc and add it to the utc availability list
            for start, end in self.availability:
                # add the conversion rate to the time slots, mod 24 if it goes past midnight 
                temp = ((start + conversion) % 24, (end + conversion) % 24)
                self.utc_availability.append(temp)

        return self.utc_availability

# Example usage
member1 = TeamMember(name="Alice", availability=[(9, 11), (14, 16)], state="CA", seniority=2)
member2 = TeamMember(name="Bob", availability=[(10, 12), (13, 15)], state="NY", seniority=1)


print(member1.get_utc())
print(member2.get_utc())