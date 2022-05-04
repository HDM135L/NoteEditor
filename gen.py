import random

f = "flick"
h = "hold"
a = "avoid"
bpm = 120
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

add(f, 0, "1:11", "1:11", slow)

add(f, -2, "2:03", "2:03", mid)

add(f, 2, "2:11", "2:11", mid)

add(f, rdt(), "3:08", "3:08", fast)

add(f, rdt(), "4:03", "4:03", mid)
add(f, rdt(), "5:11", "5:11", mid)
add(h, 0, "6:01", "6:12", mid)
add(h, -2, "7:01", "7:06", mid)
add(h, -1, "7:09", "7:12", mid)

add(f, 1, "12:07", "12:07", fast)
add(h, 1, "12:09", "12:10", fast)


start = convert("12:11")
end = convert("76:05")

while (start < end):
	if (random.random() < 0.7):
		add_str(f, rdt(), start, start, random.choice([fast, mid, mid, slow, slow]))
	start += convert_steps(16)

add(h, rdt(), "76:06", "78:02", mid)
add(h, rdt(), "78:11", "80:02", mid)
add(h, rdt(), "80:11", "81:16", mid)
add(h, rdt(), "82:11", "84:02", mid)
add(h, rdt(), "84:11", "85:16", mid)
add(h, rdt(), "86:03", "86:15", slow)
add(h, 0, "87:04", "87:13", slow)
add(a, -2, "87:04", "87:13", fast)
add(a, 2, "87:04", "87:13", fast)

print("\t]")
print("}")
print(note_num)