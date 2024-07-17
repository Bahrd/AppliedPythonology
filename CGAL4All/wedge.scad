/** In order to drive a simple rubber wedge between a front LED lamp 
    and a steerer tube we need to make it from the [virtual] scratch 
    first... 
   "Power, courage and audacity!" 
   - like MP in 1999
   - and TP in 2024
   [ https://youtu.be/yQhHsCcyKE0?t=144 ] */
$fa = 1; $fs = 1; // '$fs = 12' results in a "Stormtrooper" effect

module ally(d, txt, font = "Arial Black")
{
   /* It won't add up [substract?] when 'txt' is wider than
      four characters made out of 'LY' */
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
      - the shape should be read from the most inner item:
        -- wedge  (the main shape)
        -- medge  (a.k.a. edge milling ;)
        -- dredge (the excavated "⅄⅂LY" logo)
      [Conjecture]
      Additive‡ manufacturing 
      is preceded by [a virtual] 
      subtractive† one. */
   r = 1/2*d;
   translate([0, 0, 205/100*r]) // place the resulting wedge and ...
   rotate([180, 0, 0]) rotate([0, -25, 0]) // flip it for printing‡
      difference()            // extract† the logo from the wedge
      {
         minkowski()          // cut† all corners of the wedge
         {
            sphere(1/20*r);
            difference()   // drill† a cylinder through a cylinder to...
            {              // get two wedges and remove† the other one
               rotate([0, 25, 0])   // A bit ticker wedge      
                  cylinder(h = 4*r, r = r, center = true);
               cylinder(h = 5*r, r = 9/8*r, center = true);
               translate([-1, 0, -1]*r)
                  cube([11/5*r, 11/5*r, 11/5*r], true);
            }
         }
         translate([8/7, 0, 0.75]*r)
         rotate([0, 110, 0]) rotate(90, [0, 0, 1])
            ally(d, txt);
      }
}

module wedge_twins(d, txt) // or a wedge in a mirror
{
   translate([-12, 0, 0]) mirror([1, 0, 0])
      wedge(d, txt);
   wedge(d, txt);
}

/* The diameter of the Lapierre X2 Fit tandem bike steerer tube
   is 35mm (incl. spacers) [at least according to our caliper] */
ally = "LY"; // The '⅄⅂LY' logo's scaffolding
if(true != false)
   wedge_twins(35, txt = ally);
else
   wedge(35, txt = ally);