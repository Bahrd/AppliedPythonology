$fa = .1; $fs = .1; $fn = 256;
/** A bidon†-compatible cage for 8 Li-Ion 18650 cells

    "Kawai Tsugite" joint: https://www.youtube.com/watch?v=e1hMVlCMi1g
    Its model in STL: https://www.printables.com/model/221822-3-way-joint
    ... and how to use it: https://www.youtube.com/watch?v=KRfTj2AXiYM
    
    —
    † A.k.a. a water bottle. The throat diameter of the bottle has
    to be at least ø = 51mm.
 */

base_plate_height = 2.5;
Kawai_Tsugite_height = 12.5;
// Dimensions of an 18650 cell [mm]
cell_radius = 9;
cell_height = 65;
// Heigth of a base plate with a rod and a cover plate:
h = cell_height + 2*base_plate_height - Kawai_Tsugite_height;
// Heigth of an assembly above with a Japanese joint:
H = h + Kawai_Tsugite_height;

module base_plate(r, c = true)
{
   translate([0, 0, 2.5])
   intersection()
   {
      union()
      {
         difference()
         {
            // Should be less than 4.0
            factor = 4;
            cube([factor*r, factor*r, 5.0], c);

            for (n = [-r, r], m = [-r, r])
            {
               translate([n, m, 0])
               {
                  // recession
                  translate([0, 0, 5.0])
                     cylinder(h = 10, r = 1.02*r, center = c);
                  // hole
                  translate([0, 0, -1.25])
                     cylinder(h = 2.5, r = 0.333*r, center = c);
               }
            }
         }
      }
      translate([0, 0, -5.0])
         linear_extrude(10)
         circle(2.25*r);
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

module Kawai_Tsugite()
{
   import("./Kawai_Tsugite.stl");
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
            #rod(Kawai_Tsugite_height, r);
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
      base_plate(r, c);
      rod(10.0, r, c);
   }
}

module base_plate_and_rod(h, r)
{
   union()
   {
      translate([0, 0, 0.5*h])
         spine(h, r);
      base_plate(r);
   }
}

// All that halving is because of the object centering...
base_plate_and_rod(H - 0.5*Kawai_Tsugite_height, cell_radius);
translate([5*cell_radius, 0, 0])
   rotate([0, 0, 180])
      base_plate_and_rod(H - 0.5*Kawai_Tsugite_height, cell_radius);
translate([5*cell_radius, 5*cell_radius, 0])
   plate(cell_radius);
translate([0, 5*cell_radius, 0])
   plate(cell_radius);

/* //Size check...
   translate([0, 0, 2*H])
      rotate([180, 0, 0])
         #base_plate_and_rod(H - Kawai_Tsugite_height/2, r);*/
