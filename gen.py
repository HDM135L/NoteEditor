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
	if (random.random() < 0.7):
		add_str(f, rdt(), start, start, random.choice([fast, mid, mid, slow, slow]))
	start += convert_steps(16)

print("\t]")
print("}")
print(note_num)