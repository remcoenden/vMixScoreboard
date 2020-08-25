# vMixScoreboard makefile
# Author: Remco van den Enden

CC=gcc				# compiler
TARGET=vMixScoreboard.exe	# target file name

all: vMixScoreboard.o
	$ (CC) vMixScoreboard.c -Wall -O3 -o -lwiringPi

clean:
	rm *.o $ (TARGET)
