/**
 * A simple rubber wedge for a front LED lamp mounted to 
   a 35mm steerer tube [with spacers]
   
   "Power, courage and audacity!" [ https://youtu.be/yQhHsCcyKE0?t=144 ]
   - MP in 1999
   - TP in 2024
 */
$fa = 1; $fs = 1; // '$fs = 12' results in a "Stormtrooper" effect

module ally(std, caption, font = "Arial Black")
{
   /* It won't work well with the text wider than 
      four characters made out of these two */
   h = 1/5*std;
   // ⅄⅂
   translate([0, h, 0])
   rotate([180, 180, 0]) // == mirror([1, 0, 0]) mirror([0, 1, 0])
   linear_extrude(height = h)
      text(caption, font = font, size = h);
   // LY
   linear_extrude(height = h)
      text(caption, font = font, size = h);
}

module wedge(std, caption)
{
   /* Wedge in the making...
      - the shape should be read from the most inner part:
        -- wedge  (the main shape)
        -- medge  (a.k.a. edge milling ;)
        -- dredge (the excavated "⅄⅂LY" logo)
   
      In order to employ additive‡ manufacturing
      [a virtual] subtractive† one needs to be applied first!
   */
   str = 1/2*std;
   translate([0, 0, 21/10*str])              // place and...
   rotate([180, 0, 0]) rotate([0, -20, 0])   // flip for printing‡
      difference()         // extract† the logo from the wedge
      {
         minkowski()       // cut† all corners of the wedge
         {
            sphere(1/20*str);
            difference()   // drill† a cylinder through a cylinder to...
            {              // get two wedges and drop the other one
               rotate([0, 20, 0])
                  cylinder(h = 4*str, r = str, center = true);
               cylinder(h = 5*str, r = 9/8*str, center = true);
               translate([-1, 0, -1]*str) 
                  cube([11/5*str, 11/5*str, 11/5*str], true);
            }
         }
         translate([8/7, 0, 1]*str)
         rotate([0, 105, 0]) rotate(90, [0, 0, 1])
            ally(std, caption);
      }
}

module wedge_twin(std, caption)
{
   translate([-7, 0, 0]) mirror([1, 0, 0]) 
      wedge(std, caption);
   wedge(std, caption);
}

/* A steerer tube diameter (incl. spacers) of the Lapierre X2 Fit 
   tandem bike is 35mm - according to our caliper */
if(true != false)
{
   wedge_twin(35, caption = "LY");
}
else
{
   wedge(35, caption = "LY");
}