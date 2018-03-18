CC=gcc
CFLAGS=-O2 -Wall

lzhuf:
	$(CC) $(CFLAGS) lzhuf.c -o lzhuf

install: lzhuf
	mkdir -p /usr/share/d-rats/libexec/
	install lzhuf /usr/share/d-rats/libexec/
