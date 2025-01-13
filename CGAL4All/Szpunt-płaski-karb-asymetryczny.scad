$fa = .1; $fs = .1; $fn = 360;

r = 10; h = 10;

module ally(std, caption, font)
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

// The internal "threads" are regular and thus generated in a loop
vertices = [             [0.0,             -0.9*h], 
           for (n = [0:8], m = [0:1]) 
               (m == 0 ? [0.9*r, (-0.9 + 0.2*n)*h] : [1.0*r, (-0.7 + 0.2*n)*h]),
                         [1.0*r,            0.9*h],  [1.1*r,            1.0*h], 
                         [1.1*r,            2.5*h],  [0,                2.5*h]];
echo(vertices)
difference()
{
   translate([0, 0, 0]) 
      rotate_extrude()
         polygon(vertices);  
   translate([0, 0, 2.75*h]) 
      rotate([0, 90, 0]) 
         cylinder(h = 2.5*h, r = 1.1*r, center = true);
   translate([0, 0, 2.5*h]) 
      cube([4*r, 4*r, .5], center = true);
   translate([0, -r/4, 1.25*h]) 
      ally(25, "LY", "Arial Black");
}