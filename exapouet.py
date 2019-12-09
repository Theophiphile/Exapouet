import os
import requests
from struct import unpack_from
from operator import itemgetter
from collections import defaultdict
from colorama import init, Fore, Back
init()

def ppt2(values, leader, a, b, c):
	best = sorted(values, key=itemgetter(a,b,c))[0]
	if best[a] < leader[a] or (best[a] == leader[a] and best[b] < leader[b]) or (best[a] == leader[a] and best[b] == leader[b] and best[c] < leader[c]):
		return Fore.WHITE + '/'.join(map(str, best)) + Fore.RESET
	if best == leader:
		return Fore.GREEN + '/'.join(map(str, best)) + Fore.RESET
	return Fore.BLUE + '/'.join(map(str, best)) + Fore.RESET

levels = {
    "PB000" : (50, 'TW1'),
	"PB001" : (50, 'TW2'),
	"PB037" : (50, 'TW3'),
	"PB002" : (50, 'TW4'),
    "PB003B": (50, 'Pizza'),
	"PB004" : (50, 'Left Arm'),
	"PB005" : (50, 'Snaxnet 1'),
	"PB006B": (50, 'Zebros'),
	"PB007" : (50, 'Highway'),
	"PB008" : (50, 'UN1'),
	"PB009" : (75, 'Berkeley'),
	"PB010B": (75, 'Workhouse'),
	"PB012" : (50, 'Bank 1'),
	"PB011B": (50, 'Heart'),
	"PB013C": (50, 'TW5'),
	"PB015" : (50, 'Redshift'),
	"PB016" : (75, 'Library'),
	"PB040" : (100, 'Modem 1'),
	"PB018" : (75, 'Emersons'),
	"PB038" : (75, 'Left Hand'),
	"PB020" : (100, 'Sawayama'),
	"PB021" : (75, 'APL'),
	"PB023" : (100, 'XLB'),
	"PB024" : (100, 'KRO'),
	"PB028" : (100, 'KGOG'),
	"PB025" : (75, 'Bank 2'),
	"PB026B": (100, 'Modem 2'),
	"PB029B": (100, 'Snaxnet 2'),
	"PB030" : (75, 'Visual Cortex'),
	"PB032" : (150, 'Holman'),
	"PB033" : (150, 'USGov'),
	"PB034" : (75, 'UN2'),
	"PB035B": (100, 'Modem 3'),
	"PB036" : (150, 'Cerebral Cortex'),
	"PB054" : (150, 'mutex8021'),
	"PB053" : (100, 'NthDimension'),
	"PB050" : (150, 'Ghast'),
	"PB056" : (150, 'hydroponix'),
	"PB051" : (150, '=plastered'),
	"PB057" : (150, 'selenium_wolf'),
	"PB052" : (150, 'x10x10x'),
	"PB055" : (150, 'deadlock'),
	"PB058" : (100, 'Moss'),
}
solutions = defaultdict(list)
leaderboard = defaultdict(list)
header = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0'
}
req = requests.get('https://old.reddit.com/r/exapunks/wiki/index', headers=header).text

def pouet(a):
	if '[' not in a:
		return a.strip()
	return a.split('[')[1].split(']')[0]

table = req.split('---|---|----|----')[1].split('###')[0] + req.split('---|---|----|----')[2].split('###')[0]
name = ""
for l in table.splitlines():
	if '|' not in l:
		continue
	newname = l.split('|')[0].strip()
	if newname != "":
		name = newname
		s = l.split('|')
		cs = tuple([int(i) for i in pouet(s[1]).split('/')])
		sc = tuple([int(i) for i in pouet(s[2]).split('/')])
		ac = tuple([int(i) for i in pouet(s[3]).split('/')])
		leaderboard[name] = [cs, sc, ac, cs, sc, ac]
	else:
		s = l.split('|')
		cs = pouet(s[1]).split('/')
		sc = pouet(s[2]).split('/')
		ac = pouet(s[3]).split('/')
		if cs != ['']:
			leaderboard[name][3] = tuple([int(i) for i in cs])
		if sc != ['']:
			leaderboard[name][4] = tuple([int(i) for i in sc])
		if ac != ['']:
			leaderboard[name][5] = tuple([int(i) for i in ac])

exadir = os.environ['UserProfile'] + "/Documents/My Games/EXAPUNKS/"
for d in os.listdir(exadir):
    os.chdir(exadir + d)
    for filename in [x for x in os.listdir('.') if x.endswith('.solution') ]:
        f = open(filename, "rb")
        _, id_size = unpack_from("ii", f.read(8))
        id = f.read(id_size).decode("utf-8") 
        (name_size,) = unpack_from("i", f.read(4))
        name = f.read(name_size).decode("utf-8") 
        vs, redshift, win = unpack_from("iii", f.read(12))
        if vs != 0 or redshift != 0 or win == 0 or id not in levels:
            continue
        _, cycle, _, size, _, activity = unpack_from("iiiiii", f.read(24))
        if levels[id][0] < size:
            continue
        solutions[id].append((cycle, size, activity))
for id, values in solutions.items():
    l = leaderboard[levels[id][1]]
    cs = ppt2(values, l[0], 0, 1, 2)
    ca = ppt2(values, l[3], 0, 2, 1)
    sc = ppt2(values, l[1], 1, 0, 2)
    sa = ppt2(values, l[4], 1, 2, 0)
    ac = ppt2(values, l[2], 2, 0, 1)
    asc = ppt2(values, l[5], 2, 1, 0)
    levels[id] = f'{levels[id][1]:20} {cs:30} {ca:30} {sc:30} {sa:30} {ac:30} {asc:30}'
for level in levels.values():
    print(level)
