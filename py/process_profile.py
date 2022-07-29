import re
import sys
import os
from subprocess import Popen, PIPE, STDOUT

#
# use
# cargo install --git https://github.com/gimli-rs/addr2line.git --example addr2line
# to install addr2line
#

ADDR2LINE = "/home/xjd/.cargo/bin/addr2line"
PROGRAM = "/home/xjd/projects/rvv-prototype/bn128-example/target/riscv64imac-unknown-none-elf/release/alt-bn128-example-rvv-asm-bench"

# @[197698]: 581
RE = re.compile(r"@\[(\d+)\]: (\d+)")
RE2 = re.compile(r"(.+) at (.+)")


def parse_addr(addrs):
    args = [f'{ADDR2LINE}', '-C', '-p', '-f', '-e', f"{PROGRAM}"]
    p = Popen(args, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    stdout = p.communicate(input="\n".join(addrs).encode())[0]
    ret = []
    count = 0
    for line in stdout.decode().split("\n"):
        m2 = RE2.match(line)
        count += 1
        if m2:
            name = m2.group(1)
            ret += [name]
    assert(len(ret) == len(addrs))
    return ret


def merge(stats):
    d = {}
    for i in stats:
        if i[0] in d:
            d[i[0]] += i[1]
        else:
            d[i[0]] = i[1]

    return [(i, d[i]) for i in d]


stats = {}

for line in sys.stdin:
    m = RE.match(line)
    if m:
        addr = int(m.group(1))
        count = int(m.group(2))
        stats[addr] = count

# skip zero
del stats[0]

stats2 = []
total = 0
for addr in stats:
    count = stats[addr]
    total += count
    stats2 += [(f"{addr:#08x}", count)]

print(f"total sampling count = {total}")
names = parse_addr([i[0] for i in stats2])

stats3 = [(i, j) for i, j in zip(names, [i[1] for i in stats2])]

stats3 = merge(stats3)

stats3.sort(key=lambda x: x[1])

for item in stats3[-10:]:
    percent = int(item[1]/total*100)
    print(f"{item[0]} : {percent}%")
