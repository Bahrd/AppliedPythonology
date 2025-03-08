module ally(std, caption, font, ang = $t*360)
{
   /* It won't work well with the text wider than 
      four characters made out of these two */
   h = 1/5*std;
   // LY
   rotate([ang, ang, -ang])
   linear_extrude(height = h)
      text(caption, font = font, size = h);
   // ⅄⅂
   rotate([-ang, -ang, ang])
   translate([0, h, 0])
      rotate([180, 180, 0]) // == mirror([1, 0, 0]) mirror([0, 1, 0])
         linear_extrude(height = h)
            text(caption, font = font, size = h);
}