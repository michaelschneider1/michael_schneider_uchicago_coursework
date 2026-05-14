"""
CMSC 14200, Spring 2025
Homework #1, Task #5

The rest of this file is a copy of clicker.py

----------------------------------------------------------------------

This is a simple example of a graphical application implemented
with PyGame. It opens a blank window and, every time you click on
the window, it will add a circle in that position of the window.

You can run this example by running the following from the
Linux terminal:

    python3 clicker.py

This example highlights two important aspects of PyGame (and,
more generally, of graphical applications):

1. The event loop: A graphical application will typically perform
   some setup operations (e.g., opening a window of a specific size)
   and will then enter an "event loop". This is an effectively infinite
   loop where the program just waits for "events" to happen, so we can
   react to them. Events can include mouse clicks, key presses, etc.

   For example, if the user clicks on a position of the window, we need
   to add a circle in that position. Similarly, if the user closes the
   window, we will want to break out of the infinite loop, and end the
   program.

2. Separating "drawing" from other program logic: Graphical applications
   render (or "draw") the internal state of a program graphically. For
   example, if we were implementing a game of chess, our internal state
   could be an 8x8 list of lists, where each position contains a Piece
   object, or the value None. We will perform many operations on that
   state, such as checking for valid moves, moving pieces, etc.

   In a graphical application, we want to keep the drawing of that internal
   state completely separate from the actual logic of the application. There
   will typically be a separate function whose purpose is to take the current
   internal state of the application, and to produce a graphical representation
   of it (along with any interface elements like buttons, menus, etc.)

   In the example code below, our application keeps track of a list of circles
   or, more specifically, the (x,y) coordinates of the center of each circle
   (in our example, all circles will have a radius of 20 pixels). We said
   earlier that clicking on the window will add a circle on that location
   of the window. This just means that, when a mouse click happens, we will
   add a new circle to our list of circles, but we will *not* draw that
   circle when processing the mouse click. Instead, we have a "drawing
   function" that draws all the circles; after processing the event, we will
   call this function, and the new circle will be reflected in the graphical
   representation produced by that function.

Make sure to read the code below in the order in which it is presented.
You will find additional comments below that explain what the code does.


"""

import sys

import pygame

class Clicker:
    """
    This class demonstrates how to handle mouse clicks in Pygame.
    It maintains a list of circle positions that are updated in response to
    user clicks.
    """

    circles: list[tuple[int, int, int]]
    surface: pygame.Surface
    clock: pygame.time.Clock
    spacebar_status: bool = False
    SHRINK_EVENT = pygame.USEREVENT + 1

    def __init__(self) -> None:
        """
        The constructor initializes the Pygame modules, sets up the display
        window, and initiates the event loop.
        """

        # List to store the positions of circles and radius size
        self.circles = []

        # Initialize all imported Pygame modules
        # We must include this in any PyGame application
        pygame.init()

        # Set the title of the display window
        pygame.display.set_caption("Clicker")

        # Create a window of size 600x600. This is referred to as the "surface"
        # of our application (sometimes also known as our "canvas"). We will be
        # able to refer to specific coordinates of this surface using (x,y)
        # coordinates, where the top-left corner of the window is coordinate
        # (0, 0). Note that the y coordinates grow *down* not up. For example,
        # the bottom-left corner of the window would be (0, 599)
        self.surface = pygame.display.set_mode((600, 600))

        # Create a clock object. This will later allow us to control how
        # often our window is redrawn.
        self.clock = pygame.time.Clock()

        # Begin the event loop
        self.run_event_loop()

    def run_event_loop(self) -> None:
        """
        The event loop for our application. Inside this loop, we will
        repeatedly perform the following operations:

            1. Check for new events
            2. If there are any new events, process the events.
            3. Re-draw the window
        """
        while True:
            # Retrieve the latest events. More specifically, any time
            # events happen, PyGame places them on a queue (to await
            # processing). The pygame.event.get() method retrieves any
            # events that have been placed on that queue.
            #
            # Individual events are represented as Event objects. You
            # can read more about this here:
            # https://www.pygame.org/docs/ref/event.html
            events = pygame.event.get()

            # Process each event
            for event in events:
                # In this application, we only process two events: the QUIT
                # event (which happens when the user closes the window) and the
                # MOUSEBUTTONUP (which happens when a mouse button is released,
                # i.e., when "the pressed mouse button goes back up")

                if event.type == pygame.QUIT:
                    # When the close button of the window is clicked, we...

                    # Uninitialize all Pygame modules
                    pygame.quit()

                    # And terminate the program
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONUP:

                    # When the mouse button is released, add a new circle
                    # In the MOUSEBUTTONUP event, the Event object will include
                    # a "pos" attribute telling us the position of the surface
                    # that was clicked.
                    #
                    # Notice how all we do is add a circle to the list of
                    # circles. We don't actually draw anything on the surface
                    # at this point.
                    self.circles.append((event.pos[0], event.pos[1], 50))

                    # Uncomment the following line to see the exact positions
                    # that are being clicked on the window.

                    # print(f"Mouse clicked at position {event.pos}")
                if event.type == self.SHRINK_EVENT:
                    self.shrink_circles()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        for index, position in enumerate(self.circles):
                            x_coord, y_coord, r = position
                            self.circles[index] = (x_coord - 10, y_coord, r)
                    elif event.key == pygame.K_RIGHT:
                        for index, position in enumerate(self.circles):
                            x_coord, y_coord, r = position
                            self.circles[index] = (x_coord + 10, y_coord, r)
                    elif event.key == pygame.K_DOWN:
                        for index, position in enumerate(self.circles):
                            x_coord, y_coord, r = position
                            self.circles[index] = (x_coord, y_coord + 10, r)
                    elif event.key == pygame.K_UP:
                        for index, position in enumerate(self.circles):
                            x_coord, y_coord, r = position
                            self.circles[index] = (x_coord, y_coord - 10, r)
                    elif event.key == pygame.K_SPACE:
                        if self.spacebar_status is True:
                            self.spacebar_status = False
                        else:
                            self.spacebar_status = True
                        if self.spacebar_status:
                            pygame.time.set_timer(self.SHRINK_EVENT, 24)
                        else:
                            pygame.time.set_timer(self.SHRINK_EVENT, 0)
                    elif event.key == pygame.K_ESCAPE:
                        self.circles = []
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit(0)

            # Once we're done processing events, we redraw the window:
            self.draw_window()

            # The following ensures the surface is refreshed at 24 frames per
            # second. If we omit this, the surface will be refreshed constantly
            # (which will typically result in the application running slowly,
            # because it's spending all its time constantly redrawing the
            # window)
            self.clock.tick(24)
    def shrink_circles(self: "Clicker") -> None:
        """
        decreases the circle's radius by 1 pixel every 24 fps. If radius is 0 or
        less, circle is removed. modifies existing self.circles
        Input: None
        Output: None
        """
        for index, circle in enumerate(self.circles):
            x, y, radius = circle
            self.circles[index] = (x, y, radius - 1)

    def draw_window(self) -> None:
        """
        Clears the window and redraws all circles. This method separates the
        rendering (drawing) from the application logic and event processing.

        Remember that we have a 600x600 surface to draw on. While we can
        manipulate individual pixels, PyGame provides many convenience
        functions to draw lines, circles, etc. You can find many of them here:
        https://www.pygame.org/docs/ref/draw.html
        """

        # Fill the surface with a grey color
        # (128, 128, 128) is an RGB (Red Green Blue) color code,
        # specifying the amount of each color on a scale from 0 to 255.
        self.surface.fill((0, 0, 0))

        # For each circle in our list of circles, draw the circle.
        for circle in self.circles:

            # Use pygame.draw.circle to draw a circle
            x, y, radius = circle
            pygame.draw.circle(self.surface, color = (255, 255, 255), \
            center = (x, y), radius = radius)

        # Instruct PyGame to actually refresh the window with
        # the elements we have just drawn
        pygame.display.update()


# If you're unsure about what the following lines mean, make sure to review
# this: https://book.cs-apps.org/getting_started/organization/index.html
if __name__ == "__main__":
    Clicker()
