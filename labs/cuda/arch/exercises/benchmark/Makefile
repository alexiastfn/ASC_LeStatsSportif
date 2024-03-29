EXECS = $(notdir $(CURDIR))
RUN_CMD = apptainer exec --nv $(IMG) cuda-gdb -x gdb_commands.txt ./$${exec}

include ../../../Makefile
