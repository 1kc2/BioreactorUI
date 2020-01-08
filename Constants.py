#constants
SCREENWIDTH = 1280
SCREENHEIGHT = 720

#colours + font setup
MENU = "#518cb8"
BLUE = "#55beeb"
GREEN = "#49a362"
YELLOW = "#e79f3c"
RED = "#cd5542"
GREY = "#edf0f5"

FONT = 'MonacoB'
FONT_BOLD = 'MonacoB2 Bold'
FONTSIZE = SCREENWIDTH//110
MEDIUM = SCREENWIDTH//128
LARGE = SCREENHEIGHT//28

TIME_DELAY = 900
#Splash screen constants
MAX_ANGLE = 360
MAX_INCREMENT = 5
FRAMES_PER_SECOND = 16
DELAY = 500

#Login constants
USERNAME = 'ADMIN'
PASSWORD = '12345'

#Serial read constants
PORT = '/dev/ttyACM0'
BAUD_RATE = 9600
SERIAL_DELAY = 100 #100 miliseconds
MAX_DATA_POINTS = 60
RETRY_DELAY = 1000

#graph constants
OPTIMAL_VALS = {'pH of yeast': (7, 7), 'Temperature of yeast': (29, 32),
                'Stirring Speed': (1450, 1550), '': (0, 0)}
VAL_RANGES = {'ph': (0, 12, 0.5), 'speed': (1000, 3000, 50),
              'temperature': (20, 45, 1)} #if admin wants to alter current vals
FREQUENCY = 20
FRAMES = 200
