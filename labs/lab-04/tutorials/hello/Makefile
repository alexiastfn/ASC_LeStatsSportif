CC = nvcc

all: hello

%: %.cu
	$(CC) $^ -o $@

clean:
	rm -f hello
