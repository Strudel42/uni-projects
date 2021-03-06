from scipy import random
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


def ellipsoid_plot(a, b, c,grid_count = 35):
    '''
    a,b,c are the values for the x,y and z axis multipliers
    grid_count is the relative amount of grid lines, 35 works best
    returns a 3d plot of an ellipsoid with radius in x,y,z directions of a,b,c
    '''


    # it is recommended to not eneter a very large number for the grid count as it can me very performance intensive stick to 100 as a max value

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    u = np.linspace(0, 2 * np.pi, 100) #array for u
    v = np.linspace(0, np.pi, 100) #array for v

    #parametres for an elipsoid in polar coordinates

    x = a * np.outer(np.cos(u), np.sin(v))
    y = b * np.outer(np.sin(u), np.sin(v))
    z = c * np.outer(np.ones(np.size(u)), np.cos(v))

    # Surface plot
    ax.plot_surface(x, y, z,rcount=grid_count,ccount=grid_count,shade=True,color='green', edgecolors='k', lw=0.4)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    max_radius = max(a, b, c) #limits of plot
    for axis in 'xyz':
        getattr(ax, 'set_{}lim'.format(axis))((-max_radius, max_radius))

    return plt.show()

def ellipsoid_integration(a, b, c, accuracy=5 * (10 ** (-3))):
    '''
    a,b,c are values for x,y and z axis multipliers
    accuracy is the difference of the monte carlo integration with the volume of a given ellipsoid (volume of ellipsoid is 4/3*pi*a*b*c
    returns a value for the value for the volume of the desired ellipsoid with radii a,b,c and an error of this abs(volume - 4/3*pi*abc)
    '''

    N = 10000000 # Number of points used in space

    volume_of_box = 2*a * 2*b * 2*c # Formula for box that surrounds the ellipsoid
    volume_of_ellipsoid = (4/3)*np.pi*a*b*c # Formula that is the true value of the volume of the ellipsoid

    x_rand = random.uniform(-a, a, size=(N, 1))# These are arrays generated by the scipy random function (which is the essentialy sampe as the numpy random function.)
    y_rand = random.uniform(-b, b, size=(N, 1))
    z_rand = random.uniform(-c, c, size=(N, 1))

    x = (x_rand**2)/a**2 # Note the equation of an ellipsoid is x^2/a^2 + y^2/b2 +z^2/c^2 = 1
    y = (y_rand**2)/b**2 # The purpose of these variables x,y,z is to make it easier to read
    z = (z_rand**2)/c**2

    final_array = (x+y+z) # the final array will give values between 0 and a maximum of the boxes max coordinate ie (2a,2b,2c) and add them (2a+2b+2c)

    final_array_bool = final_array <= 1
    # From the equation of the ellipsoid we know that if x+y+z = 1 the point is on the surface of the ellipsoid.
    # This means that any value greater than 1 is therefore outside the ellipsoid and as we are interest in points inside or surface points of the ellipsoid
    # We can discard the values that are above 1 and replace them with a value of "False" and less than 1 is set to "True"

    final_array_int = final_array_bool.astype(int)
    # This converts all the bool values ("True" and "False") to 1 or 0 (1 == True, 0 == false)

    points_inside_ellipsoid = sum(final_array_int)
    # Simple sum of the array

    final_result = volume_of_box * (points_inside_ellipsoid/N)
    # Volume will be the volume of the box times the proportion of points insede the ellipsoid i.e points inside/total points


    while np.abs(final_result-volume_of_ellipsoid) > accuracy:
    # This while loop will break when the required accuracy is met or beaten.
    # The absolute difference bbetween the real volume and the MC prediction is regarded as the accuracy measurement as the equation is the true value.

        x_rand = random.uniform(-a, a, size=(N, 1))
        y_rand = random.uniform(-b, b, size=(N, 1))
        z_rand = random.uniform(-c, c, size=(N, 1))

        x = (x_rand ** 2) / a ** 2
        y = (y_rand ** 2) / b ** 2
        z = (z_rand ** 2) / c ** 2

        #This is just recalculating the value of the volume until the condtion is fulfilled at which point is prints the volume

        point_array = (x + y + z)
        final_array_bool = point_array <= 1
        final_array_int = final_array_bool.astype(int)
        points_inside_ellipsoid = sum(final_array_int)
        final_result = volume_of_box * (points_inside_ellipsoid / N)

    print(final_result,'error in volume = ',np.abs(final_result-volume_of_ellipsoid))
