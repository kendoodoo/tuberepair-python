# Colors https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
class color:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    DEFAULT = '\033[39m'
    
# Things that aren't colors.
class other_chars:
    END = '\033[0m'
    BOLD = '\033[1m'
    HEADER = '\033[95m'

# Dictonary to turn string into color at o(1) time. Useful if we ever add more colors.
color_picker = {
    'green': color.GREEN,
    'yellow': color.YELLOW,
    'red': color.RED,
}

# Used to turn a string into a color
def str_to_color(color_string):
    # All lower case for comparing
    color_string = color_string.lower()
    # Check if we have a code for the color
    if color_string not in color_picker:
        return color.DEFAULT
    # Return the color
    return color_picker[color_string]

# Used to generate seperators
def seperator(length):
        return "-" * length

# print out the version
def version(version):
    print('\n' + color.GREEN + 'TubeRepair server ' + version + other_chars.END)
    # just, forgive me.
    print(seperator(len('TubeRepair server ' + version)) + '\n')

# Helps seperator our string for logging
def print_with_seperator(string, colors='green'):
    string = str(string)
    # Begining seperator
    print(seperator(20))
    # Get our color
    use_color = str_to_color(colors)
    # Print out using our color
    print(use_color + string + other_chars.END)
    # End  seperator
    print(seperator(20))