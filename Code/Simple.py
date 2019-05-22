
from __future__ import print_function
# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

# Tutorial sample #2: Run simple mission using raw XML

from builtins import range
from math import hypot, sqrt
import MalmoPython
import os
import sys
import time
import random
import collections

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

# More interesting generator string: "3;7,44*49,73,35:1,159:4,95:13,35:13,159:11,95:10,159:14,159:6,35:6,95:6;12;"

num_seeds = 10
# forceReset="true"
missionXML_hell = '''<?xml version="1.0" encoding="UTF-8" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <About>
            <Summary></Summary>
        </About>

        <ModSettings>
            <MsPerTick>1</MsPerTick>
        </ModSettings>

        <ServerSection>
            <ServerInitialConditions>
                <Time>
                    <StartTime>6000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                </Time>
                <Weather>clear</Weather>
                <AllowSpawning>false</AllowSpawning>
            </ServerInitialConditions>
            <ServerHandlers>
                <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;8;,biome_1" />
                <DrawingDecorator>
                    <DrawCuboid x1="-50" y1="226" z1="-50" x2="50" y2="228" z2="50" type="air" />
                    <DrawCuboid x1="-50" y1="226" z1="-50" x2="50" y2="226" z2="50" type="stone" />                    
                    <DrawCuboid x1="-10" y1="226" z1="-10" x2="10" y2="226" z2="10" type="farmland" />
                    <DrawCuboid x1="0" y1="226" z1="0" x2="0" y2="226" z2="0" type="water" />
                </DrawingDecorator>
                <ServerQuitWhenAnyAgentFinishes />
            </ServerHandlers>
        </ServerSection>

        <AgentSection mode="Survival">
            <Name>Odie</Name>
            <AgentStart>
                <Placement x="0.5" y="227.0" z="0.5"/>
                <Inventory>
                    <InventoryItem slot="0" type="wheat_seeds" quantity="'''+str(num_seeds)+'''"/>
                </Inventory>
            </AgentStart>
            <AgentHandlers>
                <ContinuousMovementCommands turnSpeedDegs="480"/>
                <AbsoluteMovementCommands/>
                <SimpleCraftCommands/>
                <MissionQuitCommands/>
                <InventoryCommands/>
                <ObservationFromNearbyEntities>
                    <Range name="entities" xrange="40" yrange="40" zrange="40"/>
                </ObservationFromNearbyEntities>
                <ObservationFromFullInventory/>
                <AgentQuitFromCollectingItem>
                    <Item type="rabbit_stew" description="Supper's Up!!"/>
                </AgentQuitFromCollectingItem>
            </AgentHandlers>
        </AgentSection>

    </Mission>'''

missionXML_desert = '''<?xml version="1.0" encoding="UTF-8" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <About>
            <Summary></Summary>
        </About>

        <ModSettings>
            <MsPerTick>1</MsPerTick>
        </ModSettings>

        <ServerSection>
            <ServerInitialConditions>
                <Time>
                    <StartTime>6000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                </Time>
                <Weather>clear</Weather>
                <AllowSpawning>false</AllowSpawning>
            </ServerInitialConditions>
            <ServerHandlers>
                <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;2;,biome_1" />
                <DrawingDecorator>
                    <DrawCuboid x1="-50" y1="226" z1="-50" x2="50" y2="228" z2="50" type="air" />
                    <DrawCuboid x1="-50" y1="226" z1="-50" x2="50" y2="226" z2="50" type="stone" />                    
                    <DrawCuboid x1="-10" y1="226" z1="-10" x2="10" y2="226" z2="10" type="farmland" />
                    <DrawCuboid x1="0" y1="226" z1="0" x2="0" y2="226" z2="0" type="water" />
                </DrawingDecorator>
                <ServerQuitWhenAnyAgentFinishes />
            </ServerHandlers>
        </ServerSection>

        <AgentSection mode="Survival">
            <Name>Odie</Name>
            <AgentStart>
                <Placement x="0.5" y="227.0" z="0.5"/>
                <Inventory>
                    <InventoryItem slot="0" type="wheat_seeds" quantity="'''+str(num_seeds)+'''"/>
                </Inventory>
            </AgentStart>
            <AgentHandlers>
                <ContinuousMovementCommands turnSpeedDegs="480"/>
                <AbsoluteMovementCommands/>
                <SimpleCraftCommands/>
                <MissionQuitCommands/>
                <InventoryCommands/>
                <ObservationFromNearbyEntities>
                    <Range name="entities" xrange="40" yrange="40" zrange="40"/>
                </ObservationFromNearbyEntities>
                <ObservationFromFullInventory/>
                <AgentQuitFromCollectingItem>
                    <Item type="rabbit_stew" description="Supper's Up!!"/>
                </AgentQuitFromCollectingItem>
            </AgentHandlers>
        </AgentSection>

    </Mission>'''

# Create default Malmo objects:


def teleport(agent_host, teleport_x, teleport_z):
        """Directly teleport to a specific position."""
        tp_command = "tp " + str(teleport_x)+ " 226 " + str(teleport_z)
        agent_host.sendCommand(tp_command)
        good_frame = False

def plant_random(mapsize, num_seeds):
    planting = []
    for i in range(num_seeds):
        x = random.randint(-mapsize,mapsize)
        y = random.randint(-mapsize,mapsize)
        planting.append((x,y))

    return planting



def initialise_planting_coords(mapsize, num_seeds):
    seed_locations = []
    while(True):
        x = random.randint(-mapsize,mapsize)
        y = random.randint(-mapsize,mapsize)
        if((x,y) not in seed_locations):
            seed_locations.append((x,y))
        if (len(seed_locations) == num_seeds):
            break
    return seed_locations

def breed(parent1, parent2):
    parents = [parent1[0],parent2[0]]
    x = random.randint(0,1)
    y = random.randint(0,1)

    return ((parents[x])[0], (parents[y])[1])

def cross_over(best):
    #return a list of children
    best_tuples = []
    for i in best:
        best_tuples.append(i[0])
    newchilren = []
    for i in range(len(best)):
        parent1 = best[random.randint(0, len(best)-1)]
        parent2 = best[random.randint(0,len(best)-1)]
        new_coord = breed(parent1, parent2)
        while(True):
            if(new_coord in best_tuples or new_coord in newchilren):
                x,z = new_coord
                x = x + 1
                z = z - 1
                new_coord = (x,z)
            else:

                newchilren.append(new_coord)
                break
    return newchilren

def mutate(coordinate):
    x,y = coordinate
    offsetX = random.randint(-3, 3)
    offsetY = random.randint(-3, 3)
    x = x + offsetX
    y = y + offsetY
    return (x,y)

def select_elite_seeds(scores_tuples):
    #return top 50%- they made it to the next round
    top50 = len(scores_tuples) / 2
    return scores_tuples[0:int(top50)]

def select_weaker_seeds(scores_tuples):
    #return top 50%- they made it to the next round
    top50 = len(scores_tuples) / 2
    return scores_tuples[int(top50):]

def score_seeds(seed_locations,dirt, rock, water):
    assert(len(water) > 0)
    scores = dict()

    for seed_tup in seed_locations:
        if seed_tup in rock or seed_tup in water:
            # Invalid seed placement -> 0.0 score
            scores[seed_tup] = 0.0
        else:
            # Calculate distance from each water coordinate and score based on minimum
            water_distances = []
            for water_tup in water:
                water_distances.append( hypot(water_tup[0] - seed_tup[0], water_tup[1] - seed_tup[1]) )
            water_dist = min(water_distances)

            max_distance = sqrt(200)  # sqrt(10^2 + 10^2), will vary based on map size
            raw_score = max_distance - water_dist
            if water_dist <= 4.0:
                # Hydrated farmland
                scores[seed_tup] = raw_score
            else:
                # Dry farmland -> apply flat penalty.  Minimum score 1.0
                scores[seed_tup] = 1.0 if (raw_score - 2.0) < 1.0 else raw_score - 2.0

    '''
    for i in range(len(seed_locations)):
        scores[seed_locations[i]] = 0
    
    for f in range(len(seed_locations)):
        x,z = seed_locations[f]

        for i in range(-1,2):
            for j in range(-1,2):
                if(((x+i),(z+j)) in water and not(i == j)):
                    scores[(x,z)] = scores[(x,z)] + 1
    '''
    print(scores)
    return scores.items()

def getBestPlantingCoords(dirt,rock,water, num_seeds):
    planting_coords = initialise_planting_coords(10, num_seeds)

    #for now lets do 10 rounds
    for i in range(10):
        scores = score_seeds(planting_coords, dirt, rock, water) #as a 
        planting_coords = []
        scores = sorted(scores, key=lambda x:x[1])[::-1]

        best = select_elite_seeds(scores)

        for i in best:
            planting_coords.append(i[0])
        
        children = cross_over(best)
  
        for i in children:
            planting_coords.append(i)
        
        mutation = random.randint(0, len(planting_coords)-1)
        print("----------------------------------")
        print("The index that is mutated is: " + str(mutation))
        print(planting_coords)
        planting_coords[mutation] = mutate(planting_coords[mutation])
        print(planting_coords)
        print("----------------------------------")

    return planting_coords

agent_host = MalmoPython.AgentHost()

try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print('ERROR:',e)
    print(agent_host.getUsage())
    exit(1)
if agent_host.receivedArgument("help"):
    print(agent_host.getUsage())
    exit(0)

my_mission = MalmoPython.MissionSpec(missionXML_hell, True)
my_mission_record = MalmoPython.MissionRecordSpec()

# Attempt to start a mission:
max_retries = 3
for retry in range(max_retries):
    try:
        agent_host.startMission( my_mission, my_mission_record )
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print("Error starting mission:",e)
            exit(1)
        else:
            time.sleep(2)

# Loop until mission starts:
print("Waiting for the mission to start ", end=' ')
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
    print(".", end="")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:",error.text)

print()
print("Mission running ", end=' ')
time.sleep(5)
dirt = set()
rock = set()
water = set()

for i in range(-10,11):
    for j in range(-10,11):
        dirt.add((i,j))

water.add((0,0))

for i in water:
    dirt.remove(i)

dirt = list(dirt)
rock = list(rock)
water = list(water)

agent_host.sendCommand("pitch 0.5")

planting_coords = getBestPlantingCoords(dirt, rock, water, num_seeds)
print(planting_coords)

#planting_coords = plant_random(10,10)

planted_indices = []
for i in range(0, len(planting_coords)):
    x,z = planting_coords[i]
    print("planting: ", x, " ", z)
    if((x,z) in rock):
        print("Hit rock")
    teleport(agent_host, x, z)
    time.sleep(2);
    agent_host.sendCommand("use 1")
    planted_indices.append(i)

time.sleep(5)
for i in planted_indices:
    x,z = planting_coords[i]
    teleport(agent_host, x, z)
    time.sleep(2);
    print("removing: ", x, " ", z)
    agent_host.sendCommand("attack 1")
    time.sleep(0.1)
    agent_host.sendCommand("attack 0")


'''
# Loop until mission ends:
while world_state.is_mission_running:
    print(".", end="")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:",error.text)
'''


print()
print("Mission ended")
# Mission has ended.
agent_host.sendCommand("attack 0")
#pitch up etc