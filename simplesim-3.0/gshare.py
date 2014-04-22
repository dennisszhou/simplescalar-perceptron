from tempfile import mkstemp
from shutil import move
from os import remove, close


import os

# def calculateSize(c, b, s):
# 	#tag sizes
# 	tag = 64 - (c - s)
# 	cachelines = 2**(c - b)
# 	dirtybits = 2**(c - b)
# 	fifo = (2**(c - b)) * 4
# 	validbits = 2**(c-b)
# 	total = tag * cachelines + dirtybits + fifo + validbits
# 	total /= 8
# 	total += 2**c
# 	return total

# totalsize = 49152
# for c in range(0, 16):
# 	for b in range(0, 16):
# 		for s in range(0, 16):
# 			if calculateSize(c, b, s) <= totalsize:
# 				os.system("./cachesim -c "+str(c)+" -b "+str(b)+" -s "+str(s)+" -f E -r L < traces/astar.trace")
# for c in range(0, 16):
# 	for b in range(0, 16):
# 		for s in range(0, 16):
# 			if calculateSize(c, b, s) <= totalsize:
# 				os.system("./cachesim -c "+str(c)+" -b "+str(b)+" -s "+str(s)+" -f B -r L < traces/astar.trace")
# for c in range(0, 16):
# 	for b in range(0, 16):
# 		for s in range(0, 16):
# 			if calculateSize(c, b, s) <= totalsize:
# 				os.system("./cachesim -c "+str(c)+" -b "+str(b)+" -s "+str(s)+" -f E -r N < traces/astar.trace")

# for c in range(0, 16):
# 	for b in range(0, 16):
# 		for s in range(0, 16):
# 			if calculateSize(c, b, s) <= totalsize:
# 				os.system("./cachesim -c "+str(c)+" -b "+str(b)+" -s "+str(s)+" -f B -r N < traces/astar.trace")

def replace(file_path, size):
    #Create temp file
    fh, abs_path = mkstemp()
    new_file = open(abs_path,'w')
    old_file = open(file_path)
    index = 0
    for line in old_file:
    	if index == 20:
    		new_line = "-bpred:2lev 1 " + str(size) + " "+str(2**size)+" 1\n"
    		new_file.write(new_line)
    	else:
        	new_file.write(line)
        index += 1
    #close temp file
    new_file.close()
    close(fh)
    old_file.close()
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)


#startingValue = 1
cfgPath = "/home/victor/CS7290/Simplescalar/simplesim-3.0/config/default.cfg"
#replace(cfgPath, startingValue)

#branchSize = 32
#os.system("""./sim-outorder -config config/default.cfg tests/bin/test-math > output"""+str(branchSize)+".txt 2>&1")

for branchSize in xrange(16, 17):
    
    if branchSize%2 != 0 and branchSize != 1:
        print "Skipping value ", branchSize
        continue
    replace(cfgPath, branchSize)
    inputValues = "1_"+str(branchSize)+"_"+str(2**branchSize)+"_1"
    print "Looking at values ", inputValues
    #os.system("""./sim-outorder -config config/default.cfg tests/bin/test-math > /home/victor/Dropbox/CS7290/bimodal/bimodal"""+str(branchSize)+".txt 2>&1")
    os.system("./sim-outorder -config config/default.cfg tests/benchmarks/cc1.alpha -O tests/benchmarks/1stmt.i > /home/victor/Dropbox/CS7290/gshare/gshare"+inputValues+".txt 2>&1")

    os.system("mv tests/benchmarks/1stmt.s ~/Dropbox/CS7290/gshare/1stmt"+inputValues+".s")
    print "Finished "+str(branchSize)

print "Finished Everything!"

exit()