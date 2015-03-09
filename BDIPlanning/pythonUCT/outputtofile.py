import subprocess
import sys

fname = sys.argv[1]
print("Writing results to "+fname+".txt")
with open(fname+".txt", "w+") as output:
	subprocess.call(["python", "./riskUCT.py"], stdout=output);
print("Done!")
