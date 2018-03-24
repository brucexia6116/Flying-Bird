# Flying-Bird
Using OpenGL,a program was writtern to render an animated flying bird.

Some of the features include:

1. Bird's wing should be flapping by rotating along the birds body (long axes of the cylinder) in opposite directions while the bird is flying. The maximum rotation angle should be plus or minus 45 degrees.
2. Bird should fly at the height of 50 around a center pole which is made of a cylinder. The distance of the bird to the flag pole should be 100.
3. The diameter of the pole should be 4 and the height of the pole should be 120.
4. There should be a white point light at the distance of 200 from the pole and the height of the light should be 120.
5. The viewer eye should be at the distance of 150 from the pole at the height of 150 looking at the base of the pole.
6. There should be a flag on the top of the pole. Use a bi-cubic Bezier surface to generate the flag. This flag should be waiving. The waiving effect is done by fixing two corners of the surface patch to the pole and allowing the points and vectors on the other two points (the ones which are not attached to the pole) to change. The size of the flag should be 30 by 30.
7. The projection should be set to perspective.
8. All objects should be drawn with filled triangles (No wire frames).
9. You should use appropriate lighting models for the bird by using Ka , Kd, and Ks coefficients. The value of the coefficients should initially be set to 0.5.
10. Hitting characters "a" and "A" should decrease/increase Kar (red component of Ka) coefficient.
11. Hitting characters "d" and "D" should decrease/increase Kdr coefficient.
12. Hitting characters "s" and "S" should decrease/increase Ksr coefficient.
13. Hitting the "Up-arrow" and "down-arrow" should move the viewer eye up or down 5 units.
14. Hitting the "left-arrow" and "right-arrow" should rotate the camera clock-wise or counter-clockwise  around the pole by 5 degrees..
15. Hitting the "f" and "F" causes the bird to fly slower/faster in 10 incremental steps from zero to maximum speed (limited by CPU).
16. Hitting the character "w" should stop or start waiving the flag.
