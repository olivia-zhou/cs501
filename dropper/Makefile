CC = gcc
CXX = g++

CCFLAGS = -municode

LD_FLAGS = -lwinhttp

all: dropper

dropper: main.cpp httpClient.cpp loader.cpp;
	$(CXX) $(CCFLAGS) $^ -o $@ $(LD_FLAGS)

clean:
	rm -f dropper.exe