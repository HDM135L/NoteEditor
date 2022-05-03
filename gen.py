import random

f = "flick"
h = "hold"
a = "avoid"
bpm = 120
step_len = 15 / bpm

fast = 4
mid = 6
slow = 8

def convert_steps(steps):
	return 15 / bpm * steps

def convert(steps):
	a, b = map(int, steps.split(":"))
	return convert_steps(a * 16 + b - 1)

def rdt():
	return random.randint(-2, 2)

def add(typ, rail, start_step, end_step, delay_steps):
	print("{")
	print("\t\"Type\": \"%s\"," % typ)
	print("\t\"Rail\": %d," % rail)
	print("\t\"Length\": %f," % (convert(end_step) - convert(start_step)))
	print("\t\"StartTime\": %f," % convert(start_step))
	print("\t\"DelayTime\": %f" % convert_steps(delay_steps))
	print("},")

add(f, 0, "1:11", "1:11", slow)

add(f, -2, "2:03", "2:03", mid)
add(f, -1, "2:05", "2:05", mid)
add(f, 1, "2:07", "2:07", mid)
add(f, 2, "2:09", "2:09", mid)

add(f, 2, "2:11", "2:11", mid)
add(f, 1, "2:13", "2:13", mid)
add(f, -1, "2:15", "2:15", mid)
add(f, -2, "3:01", "3:01", mid)

add(f, rdt(), "3:08", "3:08", fast)
add(h, rdt(), "3:12", "3:15", fast)

