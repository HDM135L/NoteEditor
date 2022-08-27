import random

f = "flick"
h = "hold"
a = "avoid"
bpm = 130
step_len = 15 / bpm

fast = 8
mid = 24
slow = 32
note_num = 0

patternList = []#[rail, length, start, typ]
patternList[0] = [[-2, 0, 0, 1], [0, 0, 1, 1]]
patternList[1] = [[-1, 0, 0, 1], [1, 0, 1, 1]]
patternList[2] = [[-2, 1, 0, 2], [-1, 1, 1, 2], [0, 1, 2, 2], [2, 1, 3, 2], [1, 1, 4, 2], [0, 1, 5, 2]]
patternList[3] = [[0, 2, 0, 2], [-1, 0, 1, 1], [0, 2, 2, 2], [1, 0, 3, 1]]
patternList[4] = [[-2, 6, 0, 3], [2, 6, 0, 3], [1, 3, 3, 3], [1, 3, 3, 3], [0, 0, 4, 1]]
patternList[5] = [[-2, 3, 0, 2], [-2, 0, 1, 1], [-2, 0, 3, 1]]
patternList[6] = [[-2, 3, 0, 2], [2, 3, 0, 3], [-2, 3, 4, 3], [2, 3, 4, 2]]
patternList[7] = [[0, 1, 0, 2], [1, 1, 0, 2], [0, 0, 1, 1]]
patternList[8] = [[-2, 1, 0, 3], [-1, 1, 0, 3], [0, 0, 1, 1], [1, 1, 0, 3], [2, 1, 0, 3]]
patternList[9] = [[-2, 0, 0, 1], [-1, 0, 0, 1], [0, 0, 0, 1], [1, 0, 0, 1], [2, 0, 0, 1]]

def convert_steps(steps):
	return 15 / bpm * steps

def convert(steps):
	a, b = map(int, steps.split(":"))
	return convert_steps((a - 1) * 16 + b - 1)

def rdt():
	return random.randint(-2, 2)

def add(typ, rail, start_step: str, end_step: str, delay_steps):
	print("\t\t{")
	print("\t\t\t\"Type\": \"%s\"," % typ)
	print("\t\t\t\"Rail\": %d," % rail)
	print("\t\t\t\"Length\": %f," % (convert(end_step) - convert(start_step)))
	print("\t\t\t\"StartTime\": %f," % convert(start_step))
	print("\t\t\t\"DelayTime\": %f" % convert_steps(delay_steps))
	print("\t\t},")
	global note_num
	note_num += 1

def add_str(typ, rail, start_step, end_step, delay_steps):
	print("\t\t{")
	print("\t\t\t\"Type\": \"%s\"," % typ)
	print("\t\t\t\"Rail\": %d," % rail)
	print("\t\t\t\"Length\": %f," % (end_step - start_step))
	print("\t\t\t\"StartTime\": %f," % start_step)
	print("\t\t\t\"DelayTime\": %f" % convert_steps(delay_steps))
	print("\t\t},")
	global note_num
	note_num += 1


print("{")
print("\t\"NoteNum\": ,")
print("\t\"NoteList\": [")

add(f, 0, "43:02", "42:16", mid)
add(h, 0, "56:14", "57:14", mid)
add(a, 0, "66:02", "67:02", mid)

start = convert("76:06")
end = convert("116:01")

while (start < end):
	if (random.random() < 0.2):
	    add_stair(f, rdt(), start, start, random.choice([fast, mid, mid, slow, slow]))
            start += convert_steps(16)
        elif (0.2 <= random.random() < 0.5):
            i = random.randint(0,1)
            aList = patternList[i]
            for n in range(len(aList)):
                add_stair(aList[n][3], aList[n][0], aList[n][1] * step_len, start + aList[n][2] * step_len,random.choice([fast, mid, mid, slow, slow]))
            start += aList[len(aList) - 1][2] * step_len
        elif( 0.5 <= random.random() < 0.7):
            i = random.randint(2,9)
            aList = patterList[i]
            for n in range(len(aList)):
                add_stair(aList[n][3], aList[n][0], aList[n][1] * step_len, start + aList[n][2] * step_len,random.choice([fast, mid, mid, slow, slow]))
            start += aList[len(aList) - 1][2] * step_len

print("\t]")
print("}")
print(note_num)
