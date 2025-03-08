//$fa = .1; $fs = .1; $fn = 256;
/** A bidon†-compatible cage for 8 Li-Ion 18650 cells [25.02.2025]

    "Kawai Tsugite" joint: https://www.youtube.com/watch?v=e1hMVlCMi1g
    Its model in STL: https://www.printables.com/model/221822-3-way-joint
    ... and how to use it: https://www.youtube.com/watch?v=KRfTj2AXiYM
    
    —
    † A.k.a. a water bottle. The throat diameter of the bottle has
    to be at least ø = 51mm.
 */


use <./⅄⅂LY.scad>;
use <MCAD/boxes.scad>

module Kawai_Tsugite()
{
   import("./STL/Kawai_Tsugite.stl");
}


base_plate_height = 2.5;
Kawai_Tsugite_height = 12.5;
// Dimensions of an 18650 cell [mm]
cell_radius = 9;
cell_height = 65;
// Heigth of a base plate with a rod and a cover plate:
h = cell_height + 2*base_plate_height - Kawai_Tsugite_height;
// Heigth of an assembly above with a Japanese joint:
H = h + Kawai_Tsugite_height;

module base_plate(r, c = true, holes = false)
{
   difference()
   {
      translate([0, 0, 2.5])
      intersection()
      {
         difference()
         {
            // Should be less than 4.0
            factor = 4;
            // https://github.com/openscad/MCAD
            roundedCube(size = [factor*r, factor*r, 5], r = r*1.5, sidesonly = true, center = true);

            for (n = [-r, r], m = [-r, r])
            {
               translate([n, m, 0])
               {
                  // recession
                  translate([0, 0, 5.0])
                     cylinder(h = 10, r = 1.02*r, center = c);
                  if(holes)
                  {
                     ball = 6/2;
                     translate([0, 0, -ball + .5])
                        sphere(r = ball);
                  }
                  else
                  {
                     ball = 3/2;
                     translate([0, 0, -2*ball/3])
                        sphere(r = ball);

                  }                        
               }
            }            
         }
      }
      union()
      {
         translate([0, 0, 5])
         cube([3*r, 3*r, 5.0], c);

         tyre_diameter = cell_radius/2;
         wheel_radius = 2*cell_radius - tyre_diameter/2;
         #rotate_extrude(angle = 360) {
             translate([wheel_radius - tyre_diameter/2, tyre_diameter])
                 circle(d = tyre_diameter);
      }
      }
   }      
}


module rod(h, r, c = true)
{
   difference()
   {
      // trzon
      translate([0, 0, 0])
         cube([4*r, 4*r, h], c);

      for (s = [[0, -2*r, 0], [0, 2*r, 0]])
      {
        translate(s)
            cube([4*r, 2*r, h], c);
      }
      for (s = [[-2*r, 0, 0], [2*r, 0, 0]])
      {
         translate(s)
            cube([2*r, 4*r, h], c);
      }
      for (n = [-r, r], m = [-r, r])
      {
         translate([n, m, 0])
         cylinder(h = h, r = 1.01*r, center = c);
      }
   }
}

module spine(h, r)
{
   union()
   {
      rod(h, r);
      translate([0, 0, .5*h])
      intersection()
      {
         translate([0, 0, .5*Kawai_Tsugite_height])
         rod(Kawai_Tsugite_height, r);
               rotate([0, 0, 47.5])
         scale([.5, .5, .5])
            translate([-25.25, -28, 0])
               Kawai_Tsugite();
      }
   }
}

module plate(r, c = true)
{
   difference()
   {
      base_plate(r, c, true);
      rod(10.0, r, c);
   }
}

module base_plate_and_rod(h, r, thru_axle = false)
{
   difference()
   {
      union()
      {
         translate([0, 0, 0.5*h])
            spine(h, r);
         base_plate(r, c = true, holes = false);
      }
      if(thru_axle)
      {
         translate([0, 0, 0.5*(h + Kawai_Tsugite_height)])
            #cylinder(h = h + Kawai_Tsugite_height + 1, r = 1, center = true);      
         translate([0, 0, 2.5])
         for(angle = [45, -45])
         {
            rotate([0, 0, angle])
               cube([3*r, r/3, 2], center = true);
         }
      }
   }
}

module battery_4_pack()
{
   r = cell_radius;
   for (n = [-r, r], m = [-r, r])
   {
      translate([n, m, 0]) 
         %cylinder(h = cell_height, r = cell_radius);
   }
}


d = 5*cell_radius; o = base_plate_height; 
module battery_pack(print3D) 
{
   if(print3D)
   {
      for (p = [[0, 0, o], [0, -d, o]])
      {
         translate(p)
            battery_4_pack();
      }
   }   
   else
   {
      o = base_plate_height; 
      for (p = [o, H+o])
      {
         translate([0, 0, p])
            battery_4_pack();
      }
   }
}

module battery_cage(print3D)
{
   if(print3D)
   {
      // All that halving is because of the object centering...
      for (offset = [[0, 0], [180, d]])
      {
         translate([offset[1], 0, 0])
         rotate([0, 0, offset[0]])
         difference()
         {
            base_plate_and_rod(H - 0.5*Kawai_Tsugite_height, cell_radius);
            translate([0, -2, 0])
               ally(4, 1, "LY", "Arial Black");
         }
      }
      for (om = [-d, d])
      {
         translate([0, om, 0])
            plate(cell_radius);
      }
   }
   else
   {
      // All that halving is because of the object centering...
      for (offset = [[0, 0], [2*H, 180]])
      {
         translate([0, 0, offset[0]])
         rotate([offset[1], 0, 0])
         difference()
         {
            base_plate_and_rod(H - 0.5*Kawai_Tsugite_height, icell_radius);
            translate([0, -2, 0])
               ally(4, 1, "LY", "Arial Black");
         }
      }
      translate([0,  0, H])
      for (om = [0, 180])
      {
         rotate([om, 0, 0])
            #plate(cell_radius);
      }
   }
}

/*
There are two arrangements:
 1. print-ready
 2. view-oriented
Pick one at will...
*/

$fa = 1;
$fs = 0.4;
print3D = true;
battery_cage(print3D);
battery_pack(print3D);