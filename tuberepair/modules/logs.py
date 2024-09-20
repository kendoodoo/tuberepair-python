class color:
    HEADER = '\033[95m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def seperator(length):
    if length == 0:
        return "--------"
    return ''.ljust(len(length), '-')

# print out the version
def version(version):
    print('\n' + color.GREEN + 'TubeRepair server ' + version + color.END)
    # just, forgive me.
    print(seperator('TubeRepair server ' + version) + '\n')

# idk, i just really like to use "dookie"
def text(dookie, colors=None):
    print(seperator(dookie))
    if colors == None:
        print(color.GREEN + dookie + color.END)
    if colors == 'red':
        print(color.RED + dookie + color.END)
    print(seperator(dookie))