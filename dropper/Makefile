CC = gcc
CXX = g++

CCFLAGS = -municode

LD_FLAGS = -lwinhttp -lCrypt32

all: dropper

dropper: main.cpp httpClient.cpp loader.cpp base64.cpp;
	$(CXX) -g $(CCFLAGS) $^ -o $@ $(LD_FLAGS)

clean:
	rm -f dropper.exe