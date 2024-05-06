/**
 * A simple rubber wedge for a front LED lamp mounted to
   a 35mm steerer tube [with spacers]

   "Power, courage and audacity!" [ https://youtu.be/yQhHsCcyKE0?t=144 ]
   - MP in 1999
   - TP in 2024
 */
$fa = 1; $fs = 1; // '$fs = 12' results in a "Stormtrooper" effect

module ally(d, txt, font = "Arial Black")
{
   /* It won't work well with the text wider than
      four characters made out of these two */
   h = 1/5*d;
   // ⅄⅂
   translate([0, h, 0])
   rotate([180, 180, 0]) // == mirror([1, 0, 0]) mirror([0, 1, 0])
   linear_extrude(height = h)
      text(txt, font = font, size = h);
   // LY
   linear_extrude(height = h)
      text(txt, font = font, size = h);
}

module wedge(d, txt)
{
   /* Wedge in the making...
      - the shape should be read from the most inner part:
        -- wedge  (the main shape)
        -- medge  (a.k.a. edge milling ;)
        -- dredge (the excavated "⅄⅂LY" logo)

      In order to employ additive‡ manufacturing
      [a virtual] subtractive† one needs to be applied first!
   */
   r = 1/2*d;
   translate([0, 0, 21/10*r])              // place and...
   rotate([180, 0, 0]) rotate([0, -20, 0])   // flip for printing‡
      difference()         // extract† the logo from the wedge
      {
         minkowski()       // cut† all corners of the wedge
         {
            sphere(1/20*r);
            difference()   // drill† a cylinder through a cylinder to...
            {              // get two wedges and drop the other one
               rotate([0, 20, 0])
                  cylinder(h = 4*r, r = r, center = true);
               cylinder(h = 5*r, r = 9/8*r, center = true);
               translate([-1, 0, -1]*r)
                  cube([11/5*r, 11/5*r, 11/5*r], true);
            }
         }
         translate([8/7, 0, 1]*r)
         rotate([0, 105, 0]) rotate(90, [0, 0, 1])
            ally(d, txt);
      }
}

module wedge_twins(d, txt) // or a wedge in a mirror
{
   translate([-7, 0, 0]) mirror([1, 0, 0])
      wedge(d, txt);
   wedge(d, txt);
}

/* The diameter of the Lapierre X2 Fit tandem bike steerer tube
   is 35mm (incl. spacers) [at least according to our caliper] */
if(true != false)
   wedge_twins(35, txt = "LY");
else
   wedge(35, txt = "LY");