# converts txt register dump from TICS Pro into a python dictionary

filename = 'lmx2594_400mhz.txt'

regs = []

REGS_PER_LINE = 8

with open(filename, 'r') as f:
    for line in f:
        l = line.split()
        reg = l[0][1:]
        value = l[1]
        regs.append((reg, value))


regs.reverse()

print('LMX_REG_DEFAULTS = {', end='')

for i,reg in enumerate(regs):
    if i % REGS_PER_LINE == 0:
        print('\\\n\t', end='')
    print('{}:{}'.format(reg[0], reg[1]),end='')
    if i != len(regs) - 1:
        print(', ', end='')

print('}')



