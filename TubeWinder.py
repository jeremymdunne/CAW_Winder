from math import cos, tan, radians

"""
Simple engine for winding straight tubes with filaments

"""

class TubeWinder:
    def __init__(self, file, diameter, length, start_offset, head_offset):
        self.file = file
        self.diameter = diameter
        self.length = length
        self.start_offset = start_offset
        self.head_offset = head_offset
        self.x_loc = 0
        self.y_loc = 0
        self.z_loc = 0
        self.e_loc = 0
        self.cur_feedrate = 0
        # set the feedrates for the machine
        self.file.write("\n\n; Set the correct units and feedrates\n")
        self.calculate_step_units_and_feedrates()

    """
        reset the relative axis (e axis for now) in case of special circumstances.
    """
    def reset_relative_axis(self):
        # use this just for safety measures...
        self.file.write("G92 E0\n");
        self.e_loc = 0

    """
        calculates appropriate step units and feedrates for each axis
        assigns an appropriate unit to the e axis dependent on the tube diameter.
    """

    def calculate_step_units_and_feedrates(self):
        # first do x steps just to make sure everything's in place correctly
        # default x steps per mm is 142.782152231 steps/mm
        self.x_steps_per_mm = 142.782152231 / 16.0
        self.max_x_feedrate = 22500 # this was found through experimentation
        self.file.write("M92 X" + str(round(self.x_steps_per_mm,4)) + "\n")
        self.file.write("M203 X" + str(int(self.max_x_feedrate/60)) + "\n")
        self.file.write("M201 X900\n")
        # then y steps
        # default y steps per mm is 203.937007874
        self.y_steps_per_mm = 203.937007874
        self.max_y_feedrate = 3000 # this was found throughF experimentation
        self.file.write("M92 Y" + str(round(self.y_steps_per_mm,4)) + "\n")
        self.file.write("M203 Y" + str(int(self.max_y_feedrate/60)) + "\n")
        print("Max Y feedrate: " + str(round(self.max_y_feedrate,4)))
        # then do the z axis (ratary head)
        # because the head size *should* never change, treat like the x and y axis
        # meaning that we don't need to go from a max deg/s to a max mm/m calculation
        # unlike the e axis (body) whose dimensions change based on the diameter of the mandrel
        # don't write these values yet, as this will prevent correct homing of the z axis. see home_axis for an explination
        # default z steps per deg is 115.111111111 steps/deg
        self.z_steps_per_deg = 115.111111111
        z_steps_per_rotation = self.z_steps_per_deg * 360
        # okay, the idea is to map this out to the outer diameter of the head gear
        # gear ratio is a 40 tooth .2" pitch
        self.z_circumference = 40 * .2 * 25.4
        self.z_steps_per_mm = z_steps_per_rotation / self.z_circumference
        #self.file.write("M92 E" + str(self.z_steps_per_mm) + "\n")
        self.max_z_feedrate = 9000 # this was found through experimentation
        #self.file.write("M203 Z" + str(self.max_z_feedrate/60) + "\n")
        print("Z steps per mm: " + str(round(self.z_steps_per_mm,2)))
        print("Z steps per deg: " +str(round(self.z_steps_per_deg,2)))
        self.z_mm_per_deg = self.z_circumference / 360

        # and now the e axis
        # feedrate calculation is done from a max rpm to an equivelant mm/m
        # default e steps per degree is 60.4444444444 steps/deg
        # do an rpm conversion and set it to steps per mm of radial travel
        self.e_steps_per_rotation = 60.444444444 * 360 / 16.0
        self.e_circumference = self.diameter * 3.14159
        self.e_steps_per_mm = self.e_steps_per_rotation / self.e_circumference
        # write this to the controller
        self.file.write("M92 E" + str(round(self.e_steps_per_mm,4)) + "\n")
        print("E Steps per mm: " + str(round(self.e_steps_per_mm,4)))
        # go and set an appropriate max feedrate in rpm in equiv mm/s
        default_max_rpm = 60
        self.max_e_feedrate = (default_max_rpm * self.diameter * 3.14159)
        # convert to mm/s and tell the device
        self.file.write("M203 E" + str(int(self.max_e_feedrate/60)) + "\n")
        self.file.write("M201 E01500\n")
        print("Max e feedrate: " + str(int(self.max_e_feedrate)))
        print("Max e feedrate/s: " + str(round(self.max_e_feedrate/60)))
        # go and limit the feedrate of everything based on the e axis
        self.write_move(feedrate = self.max_e_feedrate * .75)
        self.e_mm_per_deg = self.e_circumference/360
        print("E MM per Deg: " + str(self.e_mm_per_deg))



    """
        performs heat gun passes on the tube
        @param e_to_length_ratio: ratio of e rotations for every length of travel
        @param passes: number of passes (back and forth) to perform
        @param feedrate: speed at which to perform motion
    """
    def heat_gun(self, e_to_length_ratio, passes, feedrate):
        # reset axis for safety
        self.reset_relative_axis()
        # write a quick comment in the gcode
        self.file.write("\n\n; Heat Gun\n")
        # calculate against the ratio
        e_per_move = self.e_mm_per_deg * 360 * e_to_length_ratio
        # move to the start
        self.file.write("M0 Move to starting position\n")
        self.write_move(x = self.start_offset)
        # tell the user what to do
        self.file.write("M0 Attatch Heat Gun\n")
        # preform the passes
        for i in range(passes):
            self.file.write("M117 Pass " + str(i+1) + " of " + str(passes) + "\n")
            self.write_move_rel(x = self.length, e = e_per_move, feedrate = feedrate)
            self.write_move_rel(x = -1*self.length, e = e_per_move, feedrate = feedrate)


    """
        tie down wrap: preform a tie down operation to get the filament to start correctly
        @param extension_dist: distance behind the holder to start the wrap at
        @param start_wrap_rotations: number of rotations to perform to keep the filament down
        @param feedrate: speed at which to perform this action
    """
    def tie_down_wrap(self, extension_dist, start_wrap_rotations, feedrate):
        # write a comment in the gcode
        self.file.write("\n\n; Wrap\n")
        # tell the user what's going on
        self.file.write("M0 Moving to behind the holder\n")
        self.write_move(x = self.start_offset - extension_dist, feedrate = feedrate)
        # tell the user to tie down the filament
        self.file.write("M0 Tie Down Filament\n")
        #now rotate to hold down the filament
        self.write_move(e = 360*start_wrap_rotations*self.e_mm_per_deg, feedrate = feedrate)

    """
        perform a wrap of the tube

        @param filament_width: width of the filament in mm
        @param filament_overlap_multiplier: multiplier applied to overlap filament passes. < 1 means strands overlap
        @param wind_angle: angle to perform the wind at
        @param layers: number of layers to wrap using these parameters
        @param feedrate: speed at which to perform winding
        @param extension_dist: distance to extend behind the holder when starting and finishing a pass. This helps ensure the filament catches
            on the holders
    """
    def wrap(self, filament_width, filament_overlap_multiplier = 1, wind_angle = 45, layers = 1, wanted_rpm = 20, extension_dist = 40):
        # start the wrapping cycle
        self.file.write("\n\n; Wrap\n")
        # some calculations are necessary
        # write now we only support a 45 deg wrap
        self.reset_relative_axis()
        print("Filament Overlap Multiplier: " + str(filament_overlap_multiplier))
        print("Filament Width: " + str(filament_width))
        a = tan(radians(90-wind_angle)) * filament_width/filament_overlap_multiplier
        effective_filament_width = pow(pow(filament_width/filament_overlap_multiplier,2) + pow(a,2),.5)
        print("Width: " + str(effective_filament_width))
        wraps_per_layer = int(self.e_circumference / effective_filament_width + 1.5)
        print("Wraps per Layer: " + str(wraps_per_layer))
        extraTurnDeg = effective_filament_width/self.e_circumference * 360
        print("Extra turn:" + str(extraTurnDeg))
        # now start the wrap
        # for now, just go over and back
        # have a 'lead in' in which the head turns to follow the path
        lead_in_dist = 1 * 25.4
        linear_move_dist = self.length + 2*extension_dist - 2*lead_in_dist
        # calculate the ratio of e per x for different angles
        e_per_x = tan(radians(wind_angle))
        previous_start_wrap = self.e_loc
        # make sure we're at the start_offset - extension dist
        self.write_move(x = self.start_offset - extension_dist)
        for i in range(wraps_per_layer):
            self.file.write("M117 Pass " + str(i + 1) + " of " + str(wraps_per_layer) + "\n")
            previous_start_wrap = self.e_loc
            self.write_move_rel(x = lead_in_dist, e = lead_in_dist * e_per_x, z = -1*(90-wind_angle), feedrate = self.determine_feedrate(x = lead_in_dist, e = lead_in_dist * e_per_x, z = -1*(90-wind_angle), rpm = wanted_rpm))
            self.write_move_rel(x = linear_move_dist + lead_in_dist, e = (linear_move_dist + lead_in_dist)*e_per_x, feedrate = self.determine_feedrate(x = linear_move_dist + lead_in_dist, e = (linear_move_dist + lead_in_dist)*e_per_x,rpm=wanted_rpm))
            # roatate ~ 360 degrees before moving back
            # but we need to rotate over 60 degrees to make sure the filament makes it
            self.write_move_rel(e = 45*self.e_mm_per_deg,feedrate = self.determine_feedrate(e = 45*self.e_mm_per_deg,rpm = wanted_rpm))
            # then move the head over to 0 deg
            self.write_move(e = self.e_loc + 60*self.e_mm_per_deg, z = 0,feedrate = self.determine_feedrate(e=60*self.e_mm_per_deg,z = self.z_loc,rpm = wanted_rpm))
            self.write_move_rel(e = (240-15) * self.e_mm_per_deg, feedrate = self.determine_feedrate(e = (240-15) * self.e_mm_per_deg, rpm = wanted_rpm))
            # then start moving back
            self.write_move_rel(x = -lead_in_dist, e = lead_in_dist*e_per_x, z = 90-wind_angle, feedrate = self.determine_feedrate(x = -lead_in_dist, e = lead_in_dist*e_per_x, z = 90-wind_angle,rpm = wanted_rpm))
            self.write_move_rel(x = -1 * (linear_move_dist + lead_in_dist), e = (linear_move_dist + lead_in_dist)*e_per_x, feedrate = self.determine_feedrate(x = -1 * (linear_move_dist + lead_in_dist), e = (linear_move_dist + lead_in_dist)*e_per_x,rpm = wanted_rpm))
            # roatate ~ 360 degrees before moving back
            # but we need to rotate over 60 degrees to make sure the filament makes it
            self.write_move_rel(e = 45*self.e_mm_per_deg, feedrate = self.determine_feedrate(e = 45*self.e_mm_per_deg,rpm = wanted_rpm))
            # then move the head over to 0 deg
            self.write_move(e = self.e_loc + 60*self.e_mm_per_deg, z = 0, feedrate = self.determine_feedrate(e = 60*self.e_mm_per_deg, z = self.z_loc,rpm = wanted_rpm))
            # now rotate to the closest previous_start_wrap + extraTurnDeg
            current_e_deg = (self.e_loc / self.e_mm_per_deg) % 360 # get the current 'deg'
            last_e = (previous_start_wrap / self.e_mm_per_deg) % 360 # get the deg we entered on
            required_e_delta_deg = last_e - current_e_deg # get the difference in the values
            # make sure this is a positive number < 360
            if(required_e_delta_deg < 0):
                required_e_delta_deg = required_e_delta_deg + 360
            if(required_e_delta_deg > 360):
                required_e_delta_deg = required_e_delta_deg - 360
            self.write_move_rel(e = (required_e_delta_deg) * self.e_mm_per_deg, feedrate = self.determine_feedrate(e = (required_e_delta_deg + extraTurnDeg) * self.e_mm_per_deg, rpm = wanted_rpm))


    def determine_feedrate(self, x = None, y = None, z = None, e = None, rpm = None):
        # so determine the feedrate such that the e axis is the driving feedrate
        e_feedrate = rpm * self.e_mm_per_deg * 360
        if x == None and y == None and z == None:
            return e_feedrate
        # now, given the external feedrates, increase them to match
        dist = []
        total_dist = 0
        if x is not None:
            x = abs(x)
            dist.append(x)
        if y is not None:
            y = abs(y)
            dist.append(y)
        if z is not None:
            z = abs(z)
            dist.append(z)
        e = abs(e)
        dist.append(e)
        for i in dist:
            total_dist = total_dist + pow(i,2)
        total_dist = pow(total_dist,1.0/2)
        #print(total_dist)
        # now use ratios
        feedrates = []
        actual_feedrate = 0
        if x is not None:
            feedrates.append(e_feedrate * x / e)
            #print("X",end="")
        if y is not None:
            feedrates.append(e_feedrate * y / e)
            #print("Y",end="")
        if z is not None:
            feedrates.append(e_feedrate * z * self.z_mm_per_deg / e)
            #print("Z",end="")
        #print("E")
        feedrates.append(e_feedrate)
        for i in feedrates:
            actual_feedrate = actual_feedrate + pow(i,2)
            #print("Sub feedrate: " + str(i))
        actual_feedrate = pow(actual_feedrate, 1.0/2)
        #print("Feedrate: " + str(actual_feedrate))
        return actual_feedrate


    """
        applies shrink tape to the tube
        @param shrink_tape_width: width of the shrink tape in mm
        @param overlap_multiplier: multiplier applied to overlap tape passes. < 1 means the tape overlaps
        @param feedrate: speed at which to perform the process
    """

    def shrink_tape(self, shrink_tape_width, overlap_multiplier, feedrate):
        # write a comment in the gcode
        self.file.write("\n\n; Shrink Tape\n")
        # make sure the head's back at the offset
        self.reset_relative_axis()
        self.file.write("M0 Please Remove Filament\n")
        self.write_move(x = self.start_offset + shrink_tape_width)
        # attatch shrink tape
        self.file.write("M0 Please Attatch Shrink Tape\n")
        # wind 360 degrees
        self.write_move(e = self.e_loc + 360 * self.e_mm_per_deg, feedrate = feedrate)
        # do a slow progression
        e_rotation = (self.length - 2*shrink_tape_width) / (shrink_tape_width * overlap_multiplier) * 360
        self.write_move_rel(x = self.length - shrink_tape_width, e = e_rotation * self.e_mm_per_deg, feedrate = feedrate)

    """
        handles all necessary pre wrapping steps
        @param home_before_winding: Indicates whether to perform an automatic homing
        @param manual_home: Indicates whether to perform a manual (user driven) homing
        @param check_holder_locations: Indicates whether to move the head to the interpreted locations of the holders. Useful to check, or setup
            the holders when setting up a new mandrel
        @param move_feedrate: feedrate at which to move while performing non rotational moves
        @param feedrate: feedrate at which to move while performing rotational moves
    """

    def pre_wrap(self, home_before_winding = True, manual_home = False, check_holder_locations = True, feedrate = 2000):
        # pre wrap
        self.file.write("\n\n; Pre Wrap\n")

        #go home if required
        if(home_before_winding == True):
            self.home_axis()
        #do a manual home if required
        if(manual_home == True):
            if(home_before_winding == False):
                self.home_axis()
            self.file.write("M18\n")
            self.file.write("M0 Manual Home X")
            self.file.write("M17\n")
            # void the start offset!
            self.file.write("G92 X0\n")
            # tell the user about to perform automatic on Y and Z
            self.file.write("M0 Homing Y Z\n")
            self.file.write("G28 Y Z\n")
            self.start_offset = 0
            # go and home the y and z axis
        # move the head out to the start, let the user tape down the start, then wrap a certain amount, go from there
        self.reset_relative_axis()
        self.write_move(x = self.start_offset, feedrate = feedrate)
        #move the head out
        self.file.write("M0 Moving Head Out\n")
        self.write_move(y = 4.5*25.4-self.diameter/2 - self.head_offset, feedrate = feedrate)

        if check_holder_locations == True:
            #do a test wrap to make sure the part and the fingers are in the right
            # test the wrap
            #self.file.write("\n\n; Perform a test wrap\n")
            # tell the user we are about to perform a test wrap
            self.file.write("M0 Checking Holder Locations\n")
            self.write_move(feedrate = feedrate)
            self.write_move(x = self.start_offset)
            #move the head out
            self.write_move(y = 4.5*25.4-self.diameter/2 - self.head_offset)
            self.file.write("M0 This Should Be Centered On Holder\n")
            self.write_move(x = (self.start_offset + self.length))
            self.file.write("M0 This Should Be Centered On Holder\n")
            self.write_move(x = self.start_offset)
        #done


    """
        home the machine
        Homes the Y axis first (to prevent crashes), then the other axis
        Handles reseting and setting axis units in special cases
    """
    def home_axis(self):
        self.file.write("\n\n; Home the machine\n")
        # home the y axis first to prevent collisions
        self.file.write("G28 Y\n")
        # home the other axis
         # important: I've overriden the steps/mm on the Z axis (rotatry head) but the firmware
        # the machine is running expects to set the 0 location using a steps/deg.
        # solution: only write the updated z calculations after homing the z axis!
        # to catch any weird running programs after a run, go ahead and set the standard values
        self.file.write("M92 Z115.111111 (make sure the z axis will home correctly)\n")
        self.file.write("M203 Z2000 (make sure the z axis won't move too fast)\n")
        self.file.write("G28 X Z\n")
        # the Z axis is roughly 132 degrees from horizontal, move it there and re zero
        # get the z axis back to its 'Zero' pos
        self.write_move(z = 0)
        # now go and write the new units to the z axis
        self.file.write("M92 Z" + str(self.z_steps_per_mm) + " (now write the correct units)" + "\n")
        self.file.write("M203 Z" + str(self.max_z_feedrate/60) + " (set the correct max feedrate)" + "\n")
        self.file.write("M201 Z900\n")
        # reset the e axis to 0
        self.file.write("G92 E0\n");

    """
        writes a move (G1) command to the file
        @param x: x position in mm
        @param y: y position in mm
        @param z: z position in mm
        @param e: e position in mm
        @param feedrate: speed at which to move
    """
    def write_move(self, x = None, y = None, z = None, e = None, feedrate = None):
        # doing G1's for now, combine everything
        line = "G1 "
        if(x is not None):
            line += "X" + str(round(x,3)) + " "
            self.x_loc = x
        if(y is not None):
            line += "Y" + str(round(y,3)) + " "
            self.y_loc = y
        if(z is not None):
            # z axis is still treated in deg, convert to mm before sending over
            line += "Z" + str(round(z*self.z_mm_per_deg,3)) + " "
            self.z_loc = z
        if(e is not None):
            line += "E" + str(round(e,3))+ " "
            self.e_loc = e
        if(feedrate is not None):
            line += "F" + str(int(feedrate))
            self.cur_feedrate = feedrate
        line += "\n"
        # write it to the file
        self.file.write(line)
        #print(line)


    """
        writes a relative move (G1) command to the file. Uses the last recorded absolute position in this class to handle relative moves.
        @param x: delta x position in mm
        @param y: delta y position in mm
        @param z: delta z position in mm
        @param e: delta e position in mm
        @param feedrate: speed at which to move
    """
    def write_move_rel(self, x = None, y = None, z = None, e = None, feedrate = None):
        # initialize temp variables
        act_x = None
        act_y = None
        act_z = None
        act_e = None
        # reassign those if necessary
        if(x is not None):
            act_x = self.x_loc + x
        if(y is not None):
            act_y = self.y_loc + y
        if(z is not None):
            act_z = self.z_loc + z
        if(e is not None):
            act_e = self.e_loc + e
        # execute an absolute move with the new absolute coordinates
        self.write_move(act_x, act_y, act_z, act_e, feedrate)


def main():
    print("Hello World!")
    #tube = TubeWinding(2.716 * 25.4,18 * 25.4,1 * 25.4,.1 * 25.4,1*25.4,1*25.4,45,.5 * 25.4)



if __name__ == "__main__":
    main()
