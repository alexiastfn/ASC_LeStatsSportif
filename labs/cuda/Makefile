# Configurable variables
NVCC     ?= nvcc
CC_FLAGS ?=
CPPFLAGS ?=
LDFLAGS  ?=
LIBS     ?=
EXECS    ?=

# Default rule
build: $(EXECS)

# Build each executable
$(EXECS): %: %.cu
	$(NVCC) $(NVCCFLAGS) $(CPPFLAGS) $^ -o $@ $(LDFLAGS) $(LIBS)

clean:
	rm -f $(EXECS)
