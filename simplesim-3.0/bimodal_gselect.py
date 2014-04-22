from tempfile import mkstemp
from shutil import move
from os import remove, close


import os

def replace(file_path, bimodalSize, gshareSize):
    #Create temp file
    fh, abs_path = mkstemp()
    new_file = open(abs_path,'w')
    old_file = open(file_path)
    index = 0
    for line in old_file:
    	if index == 20:
    		new_line = "-bpred:2lev 1 " + str(gshareSize) + " "+str(2**gshareSize)+" 1\n"
    		new_file.write(new_line)
        elif index == 17:
            new_line = "-bpred:bimod " + str(bimodalSize) + "\n"
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
cfgPath = "/home/victor/CS7290/Simplescalar/simplesim-3.0/config/comb.cfg"
#replace(cfgPath, 1024, 2)

#branchSize = 32
#os.system("""./sim-outorder -config config/comb.cfg tests/bin/test-math > output"""+str(branchSize)+".txt 2>&1")


gshareList = [1, 2, 4, 8]
#bimodalList = [32, 64, 128, 256, 512, 1024]
bimodalList = [2048, 4096]
for bimodal in bimodalList:
    for gshare in gshareList:
        replace(cfgPath, bimodal, gshare)
        inputValues = str(bimodal) + "-1_"+str(gshare)+"_"+str(2**gshare)+"_1"
        print "Looking at values ", inputValues
        #os.system("""./sim-outorder -config config/comb.cfg tests/bin/test-math > /home/victor/Dropbox/CS7290/bimodal/bimodal"""+str(branchSize)+".txt 2>&1")
        os.system("./sim-outorder -config config/comb.cfg tests/benchmarks/cc1.alpha -O tests/benchmarks/1stmt.i > /home/victor/Dropbox/CS7290/bimodal_gshare/bimodal_gshare"+inputValues+".txt 2>&1")

        os.system("mv tests/benchmarks/1stmt.s ~/Dropbox/CS7290/bimodal_gshare/1stmt"+inputValues+".s")
        print "Finished "+str(inputValues)

print "Finished Everything!"

exit()