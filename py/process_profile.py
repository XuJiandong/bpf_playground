import re
import sys
import os
#
# use 
# cargo install --git https://github.com/gimli-rs/addr2line.git --example addr2line
# to install addr2line
#
PROGRAM="/home/xjd/projects/rvv-prototype/bn128-example/target/riscv64imac-unknown-none-elf/release/alt-bn128-example-rvv-asm-bench"

# @[197698]: 581
RE = re.compile(r"@\[(\d+)\]: (\d+)")
RE2 = re.compile(r"(.+) at (.+)")

stats = {}

for line in sys.stdin:
    m = RE.match(line)
    if m:
        addr = int(m.group(1))
        count = int(m.group(2))
        stats[addr] = count

# skip zero
del stats[0]

stats2 = {}
total = 0
for addr in stats:
    count = stats[addr]
    total += count

    cmd = f"addr2line -C -p -f -e {PROGRAM} {addr:#08x}"
    for line in os.popen(cmd):
        m2 = RE2.match(line)
        if m2:
            name = m2.group(1)
            if name in stats2:
                stats2[name] += count
            else:
                stats2[name] = count

print(f"total sampling count = {total}")
stats3 = []
for key in stats2:
    stats3 += [(key, stats2[key])]

stats3.sort(key=lambda x: x[1])

for item in stats3[-10:]:
    percent = int(item[1]/total*100)
    print(f"{item[0]} : {percent}%")
