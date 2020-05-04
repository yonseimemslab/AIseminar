# Makefile for compiling USB DrDaq control program

FILE = drdaq
CC = gcc
CFLAGS = -shared -fpic
INCL = -I/opt/picoscope/include -I/usr/include/python3.4m
# LIB = -L/usr/local/lib -L/opt/picoscope/lib -lusbdrdaq -lpython2.7
LIB = -L/usr/local/lib -L/opt/picoscope/lib -lusbdrdaq 

all: ${FILE}.c
	${CC} ${CFLAGS} ${INCL} ${LIB} -o ${FILE}.so ${FILE}.c
	mv *.so ..

clean:
	rm *.so

