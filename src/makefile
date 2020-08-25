# vMixScoreboard makefile
# Author: Remco van den Enden

SOURCES = vMixScoreboard.c
OBJECTS = $(SOURCES:%.c=%.o)

TARGET = vMixScoreboard.exe

$(TARGET): $(OBJECTS)
	gcc $^ -Wall -O3 -o $@ -lwiringPi -pthread

%.o: %.c
	gcc -c -Wall -O3 $< -o $@ -lwiringPi -pthread

clean:
	rm *.o $(TARGET)
