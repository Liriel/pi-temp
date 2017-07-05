import curses

class TempUI:
    def __init__(self):
        # setup ncurses
        self.__screen = curses.initscr()
        # turn off key echo
        curses.noecho()
        # enable instant keycode scanning
        curses.cbreak()
        # enable color
        curses.start_color()
        # define our color pairs
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_GREEN)
        # make getch non-blocking
        self.__screen.nodelay(1)

    def RenderUI(self, temperature, humidity, msg):
        # get current window size
        (maxY, maxX) = self.__screen.getmaxyx()

        self.__screen.addstr(2, (maxX / 2) - 15, "PI Temperature/Humidity Sensor", curses.A_UNDERLINE | curses.A_BOLD)
        self.__screen.clrtoeol()

        xOffset = 2 
        self.__screen.addstr(7, xOffset, "Temperature: {0:0.1f}*C".format(temperature))
        self.__screen.clrtoeol()

        xOffset = maxX / 2 
        self.__screen.vline(7, xOffset, curses.ACS_VLINE ,maxY)
        xOffset += 2
        #self.__screen.addstr(7, xOffset, "Humidity:")
        self.__screen.addstr(7, xOffset, "Humidity: {0:0.1f}%".format(humidity))

        if(len(msg)>0):
            self.__screen.addstr(maxY - 2, 2, msg)
            msg = ""

        self.__screen.border(0)
        self.__screen.refresh()

    def End(self):
        curses.nocbreak(); self.__screen.keypad(0); curses.echo()
        curses.endwin()
