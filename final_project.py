from graphics import Canvas
import math
import time
import random

# Constants for canvas size and assumed floor load
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400

FLOOR_WEIGHT = 6

"""
# Soil property data: [cohesion_min, cohesion_max, 
phi_min, phi_max, unit_weight_min, unit_weight_max]
"""
LOOSE_SAND = [0, 0, 28, 32, 16, 18]
MEDIUM_DENSE_SAND = [0, 0, 32, 36, 17, 19]
DENSE_SAND = [0, 0, 36, 40, 18, 21]
SOFT_CLAY = [15, 25, 0, 5, 14, 17]
STIFF_CLAY = [40, 75, 0, 10, 17, 20]
SILTY_SAND = [5, 15, 26, 34, 16, 19]
GRAVEL = [0, 0, 36, 42, 19, 22]

"""
Adjust to change cloud size
A cloud with width that is 2 times its height 
gives best result
"""
CLOUD_WIDTH = 80
CLOUD_HEIGHT = 40

TRUNK_HEIGHT = 60
TRUNK_WIDTH = 15
LEAVES_SIZE = 60

TREE_BOTTOM_Y = CANVAS_HEIGHT - 20 
# Controls how fast the clouds move in the sky
DELAY = 0.1

def main():
    # Create canvas
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    """
    Create scene for building drawing by drawing a light blue rectangle
    representing the sky and three white clouds
    """
    canvas.create_rectangle(0, 0, 400, 120, 'light blue') # Draws sky
    
    # Draws three white clouds
    x_cloud_one = 20 # x-coordinate for first cloud
    y_cloud_one = 70 # y-coordinate for first cloud
    cloud_one = draw_cloud(canvas, x_cloud_one, y_cloud_one, "white")

    x_cloud_two = 270 # x-coordinate for second cloud
    y_cloud_two = 20 # y-coordinate for second cloud
    cloud_two = draw_cloud(canvas, x_cloud_two, y_cloud_two, "white")

    x_cloud_three = 270 # x-coordinate for third cloud
    y_cloud_three = 70 # y-coordinate for third cloud
    cloud_three = draw_cloud(canvas, x_cloud_three, y_cloud_three, "white")
    


    print("Let's see if your dream home will stand strong or sink like the Titanic") 
    print()
    print()
    wait_for_enter()
    print()
    print("First, let's choose the soil type you want to build on")
    print()
    # Ask user to input soil type
    soil_type = choose_soil_type()
    print(soil_type)
    print()
    print("Great choice!")

    # Draw soil based on user input
    soil_particles = draw_soil(canvas, soil_type)
    print()
    # Get pros and cons of selected soil type
    properties = pros_and_cons(soil_type)
    # Sort soil type to its full name
    type_name, soil_characteristics = sort_type(soil_type)
    # Display selected soil properties and related pros and cons
    print_variable_guide(soil_characteristics, type_name, properties)


    wait_for_enter("Press Enter to see the properties of your chosen soil type...")
    print()
    


    # Get foundation properties from user
    foundation_depth, foundation_width = foundation_properties()


    # Compute median values for selected soil type
    cohesion = (soil_characteristics[0] + soil_characteristics[1])/2
    friction_angle = (soil_characteristics[2] + soil_characteristics[3])/2
    unit_weight = (soil_characteristics[4] + soil_characteristics[5])/2
    
    # Get building floor area and number of floors from user
    number_of_floors, building_area = get_building_details()

    # Get foundation type from user
    foundation_type = get_foundation_type(soil_type)



    # Compute building pressure based on foundation type
    if foundation_type == "R":
        foundation_area = foundation_width ** 2
        num_footings = 1 # For raft foundation, we consider it as one footing
        
        # Calculate total load and pressure
        total_load = FLOOR_WEIGHT * number_of_floors * building_area
        q_applied = total_load / foundation_area

    elif foundation_type == "I":
        # For isolated footing, we need number of footings
        print()
        print("For an isolated footing, we need to know how many columns/footings your building has")
        print()
        num_footings = input("How many columns/footings? ")
        while (not num_footings.isdigit()) or (int(num_footings) < 1):
            print()
            print("That is not a valid number")
            num_footings = int(input("Enter a valid number: "))
            print()

        num_footings = int(num_footings) # Convert input from string to integer

        # Draw foundation
        draw_foundation(canvas, foundation_type, foundation_width, foundation_depth, num_footings)
        
        # Calculate load per footing and pressure
        foundation_area = num_footings * foundation_width ** 2
        total_load = FLOOR_WEIGHT * number_of_floors * building_area
        load_per_footing = total_load / num_footings
        area_per_footing = foundation_width ** 2
        q_applied = load_per_footing / area_per_footing
    print()
    print("Cool!")
    print()
    wait_for_enter()


    print()
    print("Awesome!")
    print()
    print("Now let's determine the amount of pressure your building is exerting")
    print()
    wait_for_enter()
    print("We first find the load your building is exerting with the formula \nTotal Load = Floor weight * No. of floors * Building area")
    print()
    print("Then determine the pressure by dividing the load by the foundation area (or area of one footing for isolated)")
    wait_for_enter()
    print()
    print("Using that formula...")
    print()
    print(f"Your building will apply {q_applied:.2f} kN/m² pressure on the soil")
    print()
    print()
    wait_for_enter()

    # Calculate ultimate bearing capacity
    print("Now let's find out amount of pressure the soil you chose can take")
    user_preference = input("Press Enter to see the formula used or type s to skip: ")
    if user_preference.lower() == 's':
        print()
        print("Alright, skipping the formula")
        time.sleep(1)
    else:
        print("""
            The formula used to calculate that is below
            q_ult = c * Nc + gamma * D * Nq + 0.5 * gamma * B * Ng

            Where:
            q_ult = ultimate bearing capacity (kN/m²)
            c      = soil cohesion (kPa or kN/m²)
            Nc     = bearing capacity factor for cohesion (depends on φ)
            gamma  = unit weight of soil (kN/m³)
            D      = depth of foundation (m)
            Nq     = bearing capacity factor for surcharge (depends on φ)
            B      = width of foundation (m)
            Ng     = bearing capacity factor for unit weight (depends on φ)
            """
        )

        print()
        print()

    print("Comparing your building pressure and ultimate pressure of your soil reveals that...")
    time.sleep(2)
    print()
    print()

    
    # Calculate ultimate bearing capacity based on soil properties
    Nc, Nq, Ng = compute_bearing_factors(friction_angle)
    q_ult = cohesion * Nc + unit_weight * foundation_depth * Nq + 0.5 * unit_weight * foundation_width * Ng
    
    
    # Check if building load is safe
    if q_applied < q_ult:
        print("Yay, your building is safe!! \nFind me now and let's bring it to life")
        time.sleep(5)
        
        # Show visual representation of building
        print()
        print("We'll now draw a simplified version of your building's foundation \nto show how its weight spreads into the soil")
        
        draw_building(canvas, number_of_floors)

        
        # Animate soil particles multiple times to simulate natural movement and settling
        for _ in range(15):
            animate_soil_particles(canvas, soil_particles)

    else:
        print("Ooops your building is pulling a Titanic! \nFind a Geotechnical Engineer(me) ASAP! \nOr use a deeper foundation, different soil or modify your foundation type (Finding me is a better option though😁)")
       
        draw_building(canvas, number_of_floors)
        # Dramatic soil movement
        animate_failure_soil_particles(canvas, soil_particles)
        # Show failure message
        show_failure_message(canvas)

    animate_clouds(canvas, cloud_one, cloud_two, cloud_three)
    canvas.wait_for_click()

    canvas.wait_for_click()
def wait_for_enter(message="Press Enter to continue..."):
    if not hasattr(wait_for_enter, "shown"):
        input(message)
        wait_for_enter.shown = True
    else:
        input()


def draw_cloud(canvas, initial_x, initial_y,color):
    """
    This function takes x and y coordinates of the top right
    corner of the cloud and its color.
    To create the cloud, it draws three different ovals with the
    top one being closer to a circle than the bottom 2
    """

    
    # To create bottom left oval
    left_x1 = initial_x 
    top_y1 = initial_y + CLOUD_HEIGHT/3
    right_x1 = initial_x + 3 * CLOUD_WIDTH/4
    bottom_y1 = initial_y + CLOUD_HEIGHT
    oval1 = canvas.create_oval(left_x1,top_y1,right_x1,bottom_y1,color)

    # To create bottom right oval. 
    left_x2 = initial_x + CLOUD_WIDTH/4
    top_y2 = initial_y + CLOUD_HEIGHT/3
    right_x2 = initial_x + CLOUD_WIDTH
    bottom_y2 = initial_y + CLOUD_HEIGHT
    oval2 = canvas.create_oval(left_x2,top_y2,right_x2,bottom_y2,color)

    # Create top oval
    left_x3 = initial_x + CLOUD_WIDTH/4
    top_y3 = initial_y 
    right_x3 = initial_x + 3 * CLOUD_WIDTH/4
    bottom_y3 = initial_y + 3 * CLOUD_HEIGHT/4
    oval3 = canvas.create_oval(left_x3,top_y3,right_x3,bottom_y3,color)

    return(oval1, oval2, oval3)

def animate_clouds(canvas, cloud_one, cloud_two, cloud_three):
    # move created clouds around the sky to create a more engaging environment
    speed = DELAY
    # Track change in x and y direction
    x1_change = 1
    y1_change = -1

    # Track change in y direction for second cloud
    y2_change = 1
    X2_change = [-250, 250]

    # Track change in x direction for third cloud
    x3_change = 1.5

    for i in range(300):
        # Move first cloud diagonally
        if canvas.get_top_y(cloud_one[2]) == -90:
            x1_change = -x1_change
            y1_change = -y1_change
        elif canvas.get_top_y(cloud_one[2]) == 150:
            x1_change = -x1_change
            y1_change = -y1_change

        for cloud_obj in cloud_one:
            canvas.move(cloud_obj, x1_change, y1_change)

        # Move second cloud downward and upward
        if canvas.get_top_y(cloud_two[2]) == 120:
            if canvas.get_left_x(cloud_two[0]) == 270:
                for cloud_obj in cloud_two:
                    canvas.move(cloud_obj, X2_change[0], -190)
            else:
                for cloud_obj in cloud_two:
                    canvas.move(cloud_obj, X2_change[1], -190)
        else:
            for cloud_obj in cloud_two:
                canvas.move(cloud_obj, 0, y2_change)

        # Move third cloud sideways
        if canvas.get_left_x(cloud_three[0]) == 600:
            for cloud_obj in cloud_three:
                canvas.move(cloud_obj, -1200, 0)
        else:
            for cloud_obj in cloud_three:
                canvas.move(cloud_obj, x3_change, 0)
        time.sleep(speed)

# Gives user soil types and prompts user to choose one
def choose_soil_type():
    # Let user choose soil type   
    print("What soil type would you prefer to build on?"
    "\n1.Loose Sand (LS)"
    "\n2. Medium Dense Sand (MDS)"
    "\n3. Dense Sand (DS)"
    "\n4. Soft Clay (SC)"
    "\n5. Stiff Clay (SIC)"
    "\n6. Silty Sand (SS)"
    "\n7. Gravel (G)"
    )
    soil_type = input("Input soil type initial here: ").upper()
    print()

    # Ensure user chooses valid soil type
    while soil_type not in ["LS", "MDS", "DS", "SC", "SIC", "SS", "G"]:
        soil_type = input("Kindly input valid soil type (LS, MDS, DS, SC, SIC, SS, G): ").upper()
        print()

    return soil_type
"""
Takes canvas and soil type choosen as inputes
Based on soil type choosen, it draws a rectangle with a unique color
and objects representing soil particles
"""
def draw_soil(canvas, soil_type):
    particle_size = 1
    initial_x = 0
    initial_y = 3 * CANVAS_HEIGHT/4

    # Map soil types to colors
    color_map = {
    "LS": "sandybrown",
    "MDS": "peru",
    "DS": "saddlebrown",
    "SC": "tan",
    "SIC": "burlywood",
    "SS": "wheat",
    "G": "gray"
    }
    color = color_map.get(soil_type, "gray") # Default to gray if not found
    soil_particle = []
    
    # Draw soil
    soil = canvas.create_rectangle(0, 3 * CANVAS_HEIGHT/4,
                                    CANVAS_WIDTH,
                                    CANVAS_HEIGHT, color)
    
    if soil_type == "LS":
        # Draw smaller particles for loose sand
        while (initial_y + particle_size) <= CANVAS_HEIGHT:
            while (initial_x + particle_size) <= CANVAS_WIDTH:

                particle_id = canvas.create_oval(initial_x,
                                        initial_y,
                                        initial_x + particle_size,
                                        initial_y + particle_size,
                                        "brown")
                soil_particle.append((particle_id, initial_x, initial_y))
                spacing = random.randint(1,25)
                # Update initial_x to begin at specified point on right 
                initial_x += (particle_size + spacing)

            spacing = 1
            # Update initial_y to begin below
            initial_y += (particle_size + spacing)
            initial_x = 0
    
    
    elif soil_type == "MDS":
        # Draw medium sized particles for medium dense sand
        while (initial_y + particle_size) <= CANVAS_HEIGHT:
            while (initial_x + particle_size) <= CANVAS_WIDTH:

                particle_id = canvas.create_oval(initial_x,
                                        initial_y,
                                        initial_x + particle_size,
                                        initial_y + particle_size,
                                        "black")
                soil_particle.append((particle_id, initial_x, initial_y))
                spacing = random.randint(10, 25)
                # Update initial_x to begin at specified point on right 
                initial_x += (particle_size + spacing)

            spacing = 5
            # Update initial_y to begin below
            initial_y += (particle_size + spacing)
            initial_x = 0
    
    elif soil_type == "DS":
        # Draw larger particles for dense sand
        while (initial_y + particle_size) <= CANVAS_HEIGHT:
            while (initial_x + particle_size) <= CANVAS_WIDTH:

                particle_id = canvas.create_oval(initial_x,
                                        initial_y,
                                        initial_x + particle_size,
                                        initial_y + particle_size,
                                        "brown")

                soil_particle.append((particle_id, initial_x, initial_y))
                spacing = 5
                # Update initial_x to begin at specified point on right 
                initial_x += (particle_size + spacing)

            spacing = 5
            # Update initial_y to begin below
            initial_y += (particle_size + spacing)
            initial_x = 0
    
    elif soil_type == "SC":
        # Draw larger, flatter particles for clay
        while (initial_y + particle_size) <= CANVAS_HEIGHT:
            while (initial_x + particle_size) <= CANVAS_WIDTH:
                particle_size_x = random.randint(3, 10) # Make particles wider
                particle_size_y = 1

                particle_id = canvas.create_oval(initial_x,
                                        initial_y,
                                        initial_x + particle_size_x,
                                        initial_y + particle_size_y,
                                        'brown')
                soil_particle.append((particle_id, initial_x, initial_y))
                spacing = random.randint(1, 20) # Random spacing for variability
                # Update initial_x to begin at specified point on right 
                initial_x += (particle_size + spacing)

            spacing = 15
            # Update initial_y to begin below
            initial_y += (particle_size + spacing)
            initial_x = 0
   
    elif soil_type == "SIC":
        # Draw rectangular particles for stiff clay
        while (initial_y + particle_size) <= CANVAS_HEIGHT:
            while (initial_x + particle_size) <= CANVAS_WIDTH:
                particle_size_x = 6 # Fixed width for rectangular particles
                particle_size_y = 3 # Fixed height for rectangular particles

                particle_id = canvas.create_rectangle(initial_x,
                                        initial_y,
                                        initial_x + particle_size_x,
                                        initial_y + particle_size_y,
                                        'gray')
                soil_particle.append((particle_id, initial_x, initial_y))
                spacing = random.randint(1, 10) # Random spacing for variability
                # Update initial_x to begin at specified point on right 
                initial_x += (particle_size + spacing)

            spacing = random.randint(7, 10)
            # Update initial_y to begin below
            initial_y += (particle_size + spacing)
            initial_x = random.randint(0, 5) # Randomize starting x for next row
   
    elif soil_type == "SS":
        # Draw larger, flatter particles for silty sand
        while (initial_y + particle_size) <= CANVAS_HEIGHT:
            while (initial_x + particle_size) <= CANVAS_WIDTH:
                particle_size_x = random.randint(1, 7) # Make particles wider
                particle_size_y = 1

                particle_id = canvas.create_oval(initial_x,
                                        initial_y,
                                        initial_x + particle_size_x,
                                        initial_y + particle_size_y,
                                        'black')
                
                soil_particle.append((particle_id, initial_x, initial_y))
                spacing = random.randint(1, 20) # Random spacing for variability
                # Update initial_x to begin at specified point on right 
                initial_x += (particle_size + spacing)

            spacing = 10
            # Update initial_y to begin below
            initial_y += (particle_size + spacing)
            initial_x = random.randint(0, 5) # Randomize starting x for next row
    
    else:
        # Draw irregular polygonal particles for gravel
        while (initial_y + particle_size) <= CANVAS_HEIGHT:
            while (initial_x + particle_size) <= CANVAS_WIDTH:
                particle_size_poly = random.randint(9,15) # Size of the polygon
                polygon_top_left = initial_x + 3
                polygon_top_right = initial_x + random.randint(7,10)
                polygon_middle_right = initial_x + random.randint(11,15)
                polygon_bottom_left = initial_x + random.randint(3,5)
                polygon_bottom_right = initial_x + random.randint(7,10) 
                particle_size_x = random.randint(7, 15) # Width of the particle
                particle_size_y = random.randint(7, 15) # Height of the particle
                
                particle_id = canvas.create_polygon(polygon_top_left,
                                                initial_y,
                                                polygon_top_right,
                                                initial_y + 2,
                                                polygon_middle_right,
                                                initial_y + (1/2 * particle_size_poly),
                                                polygon_bottom_right,
                                                initial_y + particle_size_poly,
                                                polygon_bottom_left,
                                                initial_y + particle_size_poly,
                                                initial_x,
                                                initial_y + (1/2 * particle_size_poly),
                                                fill='gray', 
                                                outline='black'
                                                )
                spacing = random.randint(0,3) # Random spacing for variability
                soil_particle.append((particle_id, initial_x, initial_y))
                # Update initial_x to begin at specified point on right 
                initial_x = (polygon_middle_right + spacing) 
            
            # Update initial_y to begin below
            initial_y += (10 + spacing)
            initial_x = random.randint(0, 3) # Randomize starting x for next row
    return soil_particle


def animate_soil_particles(canvas, soil_particles):
    base_y = 3 * CANVAS_HEIGHT / 4
    particle_size = 10
    updated_particles = []
    for i, (particle_id, x, y) in enumerate(soil_particles):
        # Get current y position
        current_y = canvas.get_top_y(particle_id)
        # The closer to base_y, the more it moves
        distance_from_base = current_y - base_y
        # Particles near the base move more, deeper ones less
        move_factor = max(1, 10 - int(distance_from_base / 8))
        dx = random.randint(-1, 1)
        dy = random.randint(move_factor // 2, move_factor)
        # Calculate new position
        new_x = canvas.get_left_x(particle_id) + dx
        new_y = current_y + dy
        new_x2 = new_x + particle_size
        new_y2 = new_y + particle_size
        overlapping = canvas.find_overlapping(new_x, new_y, new_x2, new_y2)
        # Only move if not overlapping with others (or only itself)
        if not overlapping or (len(overlapping) == 1 and overlapping[0] == particle_id):
            canvas.move(particle_id, dx, dy)
            updated_particles.append((particle_id, new_x, new_y))
        else:
            # If can't move, keep old position
            updated_particles.append((particle_id, x, y))
    # Update the soil_particles list in place
    soil_particles[:] = updated_particles
    time.sleep(0.08)
def animate_failure_soil_particles(canvas, soil_particles):
    base_y = 3 * CANVAS_HEIGHT / 4
    particle_size = 10
    for _ in range(20):  # More frames for dramatic effect
        updated_particles = []
        for i, (particle_id, x, y) in enumerate(soil_particles):
            current_y = canvas.get_top_y(particle_id)
            distance_from_base = current_y - base_y
            # Move much more on failure
            move_factor = max(5, 25 - int(distance_from_base / 8))
            dx = random.randint(-5, 5)
            dy = random.randint(move_factor // 2, move_factor)
            new_x = canvas.get_left_x(particle_id) + dx
            new_y = current_y + dy
            new_x2 = new_x + particle_size
            new_y2 = new_y + particle_size
            overlapping = canvas.find_overlapping(new_x, new_y, new_x2, new_y2)
            if not overlapping or (len(overlapping) == 1 and overlapping[0] == particle_id):
                canvas.move(particle_id, dx, dy)
                updated_particles.append((particle_id, new_x, new_y))
            else:
                updated_particles.append((particle_id, x, y))
        soil_particles[:] = updated_particles
        time.sleep(0.05)

# Gives user pros and cons of the soil type they chose
def pros_and_cons(soil_type_choosen):
    if soil_type_choosen == "LS":
        pros_and_cons = """
        Loose sand drains water quickly which reduces pore water pressure
        Don't feel pressured if you don't know what that is (lame pun intended)
        It simply means your building will have less forces working against it
        However be careful, LS has low strength and is prone to settlement
        """
    elif soil_type_choosen == "MDS":
        pros_and_cons = """
        MDS, much like its name, has medium strength and drainage
        This is good since sand is known for its low strength
        MDS also has a better load distribution than LS
        However, it is prone to settlement which can cause your beautiful home to sink
        """
    elif soil_type_choosen == "DS":
        pros_and_cons = """   
        Good choice, it has high shear strength, excellent bearing capacity and low compressibility
        But hey, I hope you aren't planning to live in an earthquake prone zone though
        Sesmic activity can cause the soil to flow like water and destroy your property
        The low compressibility also means you can't compact it well to rule out settlement
        """
    elif soil_type_choosen == "SC":
        pros_and_cons = """ 
        The soft nature of the soil makes it easy to evacuate 
        But be very careful, SC has very low strength 
        and keeps settling over long periods of time 
        Unlike the Titanic, you will have no warning that your building is sinking
        as it can take years
        """
    elif soil_type_choosen == "SIC":
        pros_and_cons = """
        Compared to SC, it has a higher bearing strength
        and reduced settlement risk
        But watch out, it can develop cracks when dry, 
        leading to water seepage and volume changes.
        """
    elif soil_type_choosen == "SS":
        pros_and_cons = """
        SS has moderate bearing capacity if compacted well
        The cons are, it retains water
        so I wouldn't recommend it if you live at a snowy place
        as it becomes prone to frost heave and reduced strength when saturated.
        """
    else:
        pros_and_cons = """
        Like the Bible said, is is wise to build on a rock 
        (or several tiny rocks as in the case of gravels)
        G has a high bearing capacity, excellent drainage and rarely compresses
        On the other hand it is hard to compact uniformly 
        and may allow water movement under foundations
        It is also hard and expensive to excavate but that's not a problem for you
        We both know Jeff Bezos has got nothing on you 😉
        """
    return pros_and_cons

def sort_type(soil_type):
    # Sort soil properties
    if soil_type == "LS":
        soil_characteristics = LOOSE_SAND
        type_name = "Loose Sand"
    elif soil_type == "MDS":
        soil_characteristics = MEDIUM_DENSE_SAND 
        type_name = "Medium Dense Sand"
    elif soil_type == "DS":
        soil_characteristics = DENSE_SAND
        type_name = "Dense sand"
    elif soil_type == "SC":
        soil_characteristics = SOFT_CLAY
        type_name = "Soft Clay"
    elif soil_type == "SIC":
        soil_characteristics = STIFF_CLAY
        type_name = "Stiff Clay"
    elif soil_type == "SS":
        soil_characteristics = SILTY_SAND
        type_name = "Silty Sand"
    else:
        soil_characteristics = GRAVEL
        type_name = "Gravel"

    return type_name, soil_characteristics  

def print_variable_guide(soil_characteristics, type_name, properties):
    print(f"You have selected: {type_name}\n{properties}")

    print(f"Typical property values for {type_name} are: ")

    if type_name in ["Loose Sand", "Gravel", "Medium Dense Sand", "Dense Sand"]:
        print("Cohesion (c): 0")
    else:
        print(f"Cohesion (c): {soil_characteristics[0]} - {soil_characteristics[1]}")
    print(f"Friction angle (φ): {soil_characteristics[2]} - {soil_characteristics[3]}"
    f"\nUnit weight (γ): {soil_characteristics[4]} - {soil_characteristics[5]}")
    print()
    print("For this program, we will use the median values of the ranges")
    print()
    print()
    

def foundation_properties():
    # Prompt user for foundation properties
    print("Now that you have your soil type its time to determine your foundation properties")
    print()
    print("Namely your foundation depth (how deep you'll dig)")
    print("and your foundation width (how wide it will be)")
    print()
    print("Please enter values in mm (typical depth: 600–3000 mm, width: 300–1500 mm)")
    print()
    
    # Depth input with limits
    while True:
        foundation_depth = input("What is your foundation depth in mm? ")
        if foundation_depth.isdigit():
            foundation_depth = float(foundation_depth)
            if 600 <= foundation_depth <= 3000:
                break
            else:
                print("Please enter a depth between 600 mm and 3000 mm.")
        else:
            print("That is not a valid number")

    print() 
    
    # Width input with limits
    while True:
        foundation_width = input("What is your foundation width in mm? ")
        if foundation_width.isdigit():
            foundation_width = float(foundation_width)
            if 300 <= foundation_width <= 1500:
                break
            else:
                print("Please enter a width between 300 mm and 1500 mm.")
        else:
            print("That is not a valid number")
    
    print()
    print("Great!")
    print()
    wait_for_enter()

    # Convert to meters for calculations
    return foundation_depth / 1000, foundation_width / 1000

def get_building_details():
    # Let user input building properties 
    print("It's finally time for you to build your house")
    # Ask user how many floors their building has (max 4)
    print("For this program we will assume each floor of your building carries a load of 6kN/m²")
    print("And hey I know you are rich but your building is limited to 4 floors here")
    print()
    number_of_floors = input("So how many floors does your dream house have? ")
    while not number_of_floors.isdigit() or int(number_of_floors) < 1 or int(number_of_floors) > 4:
        print()
        print("That is not a valid number")
        number_of_floors = input("Enter a valid number: ")
    number_of_floors = int(number_of_floors) # Convert input from string to float
    print()
    print("Nice!")
    print()
    print()
    
    # Ask user for building area (default 100m²)
    building_area = input("Enter the building area in m² or press enter to use 100m²: ")

    if building_area == "":
        building_area = 100
    else:
        while not building_area.isdigit() or float(building_area) < 1:
            print()
            print("That is not a valid number")
            building_area = input("Enter a valid number: ")
        building_area = float(building_area) # Convert input from string to float
    print()
    print("Awesome!")
    print()
    return number_of_floors, building_area


"""
Gives a background of the two foundation types the user can choose
Asks the user to select one
Returns the user's choice
"""
def get_foundation_type(soil_type):
    # Explain and choose foundation type
    print("There are several foundation types")
    print("A geotechnical engineer's choice depends on the building load, the soil type and the environment")
    print()
    wait_for_enter()

    print("For this program you have the chance to choose between two foundation types, raft and isolated footings")
    wait_for_enter()
    print()
    # Ask user to choose a foundation type: Raft or Isolated Footing
    print("A Raft(R) foundation, much like a boat is a large connected foundation, \nthat spreads across the base of the building")
    wait_for_enter()
    print()
    print("Isolated Footings(I) on the other hand consists of several columns \nholding up the building, each with it's own footing")
    wait_for_enter()
    
    # Runs if soil is prone to settlement, that is is SC, SS or LS
    # Advices user to choose raft foundation 
    if soil_type in ["SC", "SS", "LS"]:
        print()
        print("💡 Tip:")
        print("The soil you selected is prone to settlement.")
        print("Consider using a raft foundation to reduce the risk of uneven sinking.")
        wait_for_enter()

    print()
    foundation_type = input("Which foundation type will you build on? R or I: ").upper()
    while foundation_type != "I" and foundation_type != "R":
        print()
        foundation_type = input("Please choose a valid foundation type. Either R or I: ").upper()
    return foundation_type

def draw_foundation(canvas, foundation_type, foundation_width, foundation_depth, num_footings=1, color="grey"):
    # Visual scale: 1m = 10 pixels (adjust as needed)
    scale = 30
    foundation_top = 3 * CANVAS_HEIGHT / 4
    foundation_bottom = foundation_top + foundation_depth * scale

    if foundation_type == "R":
        left_x = CANVAS_WIDTH / 2 - foundation_width * scale
        right_x = CANVAS_WIDTH / 2 + foundation_width * scale
        canvas.create_rectangle(left_x, foundation_top, right_x, foundation_bottom, color)
    elif foundation_type == "I":
        # Confine footings under the building
        building_left = CANVAS_WIDTH / 2 - 50
        building_right = CANVAS_WIDTH / 2 + 50
        building_width = building_right - building_left
        footing_width = foundation_width * scale
        if num_footings == 1:
            centers = [CANVAS_WIDTH / 2]
        else:
            step = building_width / (num_footings - 1) if num_footings > 1 else 0
            centers = [building_left + i * step for i in range(num_footings)]
        for center_x in centers:
            left_x = center_x - footing_width / 2
            right_x = center_x + footing_width / 2
            canvas.create_rectangle(left_x, foundation_top, right_x, foundation_bottom, color)

def draw_building(canvas,number_of_floors):
    # Draw building above foundation
    # Each floor is represented as a blue rectangle
    left_x = CANVAS_WIDTH/2 - 50
    # Start the building just above the soil/foundation
    top_y = 3 * CANVAS_HEIGHT / 4 - number_of_floors * 70
    right_x = CANVAS_WIDTH/2 + 50
    bottom_y = 3 * CANVAS_HEIGHT / 4
    
    # Create building floors
    for i in range(number_of_floors): 
        canvas.create_rectangle(left_x, top_y, right_x, top_y + 70, "blue")
        top_y += 70 # Move up for the next floor


    # Draw windows
    left_x = CANVAS_WIDTH/2 + 10
    top_y = CANVAS_HEIGHT - 160
    right_x = CANVAS_WIDTH/2 + 40
    bottom_y = CANVAS_HEIGHT - 140
    for i in range(number_of_floors):
        canvas.create_rectangle(left_x,top_y,right_x,bottom_y,"grey")
        top_y -= 70
        bottom_y -= 70

     
def compute_bearing_factors(friction_angle):
    phi = math.radians(friction_angle)
    Nq = math.exp(2*math.pi*(0.75 - friction_angle/360)*math.tan(phi)) \
         / (2 * math.cos(math.radians(45 + friction_angle/2))**2)
    Nc = (Nq - 1) / math.tan(phi) if friction_angle > 0 else 5.7
    Kp = math.tan(math.radians(45 + friction_angle/2))**2
    Ng = 0.5 * math.tan(phi) * (Kp / math.cos(phi)**2 - 1)
    return Nc, Nq, Ng

def show_failure_message(canvas):
    # Centered horizontally and vertically, with red color
    canvas.create_text(
        CANVAS_WIDTH / 2,
        CANVAS_HEIGHT / 2,
        "FOUNDATION FAILURE!",
        color="red",
        anchor="center",
        font="Arial 20"
    )

if __name__ == '__main__':
    main()