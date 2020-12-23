SOURCES = vMixScoreboardTest.c
OBJECTS = $(SOURCES:%.c=%.o)

TARGET = vMixScoreboardTest.exe

$(TARGET): $(OBJECTS)
	gcc $^ -O3 -o $@ -lwiringPi

%.o: %.c
	gcc -Wall -O3  -std=c11  -c $< -o $@

.PHONY: clean debug

clean: rm *.o

debug: $(TARGET)-debug.exe
