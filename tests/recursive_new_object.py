# File created by Felipe Fernandes (2017)

# This file presents a minimum working example of the recursive creation of
# new objects used by some of the methods defined in this package

# copy package is used to make deep copies of the object
import copy

class Ball2(object):
    def __init__(self, color = 'red'):
        self.color = color

    # Definition of the method that uses the recursive object creation
    def paint(self, new_color, return_new_Ball = False):

        # Applying the recursive method
        if return_new_Ball:

            # If a new object is to be returned, first create it as a copy of
            # the original one
            new_Ball = copy.deepcopy(self)

            # Then call the method again, not for self, but for the copy, giving
            # the same value for all other parameters, while setting
            # return_new_Ball to false to stop the loop. This will also
            # evaluate the method for the new_Ball.
            new_Ball.paint(new_color, return_new_Ball=False)

            # Return the newly created object
            return new_Ball

        # This is where the method's code actually goes. It's usually way more
        # code than this.
        else:
            # In this case, we only update the Ball's color.
            self.color = new_color



# So lets test it.

# Lets create a red ball
Ball1 = Ball(color = 'red')
print "The Ball1 color is: " + Ball1.color

# Now lets paint it,
print "\nNow, painting the Ball blue:"
Ball1.paint(new_color ='blue')
print "The Ball1 color is: " + Ball1.color

# Now, assume we want to actually clone Ball1, keeping all other characteristics
# but changing its color.
# (in this case, it only has color, but it could have other attributes as
# 'size', 'owner', 'condition', and also methods, like 'kick', 'throw', etc,
# that we might want to clone to a new_object with only a different color)
print ("\nApplying the same method, but in this case cloning Ball1 while "
       "changing its color")
Ball2 = Ball1.paint(new_color='green', return_new_Ball=True)
print "The Ball1 color is: " + Ball1.color
print "The Ball2 color is: " + Ball2.color
