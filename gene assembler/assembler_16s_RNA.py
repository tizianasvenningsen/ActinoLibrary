from tkinter.filedialog import askdirectory
from datetime import datetime
from tkinter import simpledialog
import os

# FUNCTIONS

# Compute reverse complement of a DNA sequence
def reverse_complement(dna):
	process = dna[::-1]
	reversed_dna_string = ""
	for base in process:
		if base == "A":
			reversed_dna_string += "T"
		if base == "G":
			reversed_dna_string += "C"
		if base == "C":
			reversed_dna_string += "G"
		if base == "T":
			reversed_dna_string += "A"
	return reversed_dna_string

# Compute longest contiguous common subsequence
# forward: A DNA sequence representing the forward read
# reverse: A DNA sequence representing the backward read (reverse complemented)
def lcs(forward, reverse):
	# Initialize empty string
	lcs = ""

	# For every start position in the forward read
	for start in range(len(forward)):

		# For every length of possible common subsequence
		for l in range(len(forward)-start):

			# Only need to consider if longer than longest already found
			if l > len(lcs):

				# Extract subsequence from forward read
				subseq = forward[start:start+l]

				# Check if this extracted subsequence exists in reverse string
				if subseq in reverse:

					# If so, replace 'lcs' with new longer subsequence
					lcs = subseq
				else:
					break
	return lcs


# MAIN

# Ask user which directory to assemble reads from
path = askdirectory(initialdir='/Users/tizianasvenningsen/Dropbox/Uni/Bachelor projekt/Sekvenseringer/')

# Initialize empty strings
forward = ""
reverse = ""

# Loop through every file in the directory
for filename in os.listdir(path):

	# If the filename ends with 'f.seq', then that is the forward sequence.
	if filename.lower().endswith("f.seq"): # Found forward sequence

		# Open file in Python
		with open(path+"/"+filename, 'r') as file:

			# Read contents of file
			forward = file.read()

			# Remove line breaks from file
			forward = forward[forward.index('\n'):].replace('\n','')

	# If the filename ends with 'r.seq', then that is the reverse sequence.
	if filename.lower().endswith("r.seq"): # Found reverse sequence

		# Open file in Python
		with open(path+"/"+filename, 'r') as file:

			# Read contents of file
			reverse = file.read()

			# Remove line breaks from file
			reverse = reverse[reverse.index('\n'):].replace('\n','')

# Rename the forward and reverse sequences 
rawf = forward
rawr = reverse

# Find the id of the directory Example: 20-2-1 
ID = path[path.rindex('/')+1:]

# Asks the user where to cut of sequences, they are both only cut in the begining (reverse is also cut in begining before Reverse complemented)
cutoff_forward=int(simpledialog.askstring("Input settings for "+ID,"Assembling "+ID+"\nEnter the forward cutoff.\n\nNote: cutoff is the LAST base you want REMOVED."))
cutoff_backward=int(simpledialog.askstring("Input settings for "+ID,"Assembling "+ID+"\nForward cutoff was "+str(cutoff_forward)+"\nEnter the backward cutoff.\n\nNote: cutoff is the LAST base you want REMOVED."))


print("\n+-------------------------------+")
print("Loading sequences from "+ID+"...")
print("+-------------------------------+")
print("Forward cutoff: "+str(cutoff_forward)+"/"+str(len(forward)))
print("Reverse cutoff: "+str(cutoff_backward)+"/"+str(len(reverse)))
print("+-------------------------------+")

# Show user where the forward sequence was cut 
print("Forward: \n" + forward[:cutoff_forward] + "|" + forward[cutoff_forward:cutoff_forward+10]+"...")
forward  = forward[cutoff_forward:]
# Show user where the reverse sequence was cut 
print("\nReverse: \n" + reverse[:cutoff_backward] + "|" + reverse[cutoff_backward:cutoff_backward+10]+"...")
reverse = reverse[cutoff_backward:]

# Reverse compoenets the reverse string 
revcl = reverse_complement(reverse)

# Search for the longest common subsequence between the forward and the reverse compoeneted reverse string. If overlap is very small it also outputs a warning.  
common = lcs(forward, revcl)
if len(common) < 10:
	print("WARNING: Overlap may be too small.")

# Collects the sequences in one total sequence 
i = forward.index(common)
j = revcl.index(common) + len(common)
output = forward[:i] + common + revcl[j:]

print("\nThe two sequences have " + str(len(common))+" bases in common.\nThe length of the clipped sequence is "+str(len(output))+" bases.")


# Gives the raw untrimmed sequences 
print("+-------------------------------+")
print("Raw F: \n"+ rawf)
print("\nRaw R: \n"+ rawr)
print("+-------------------------------+")

#Creates two new files to the directory one with the collected FASTA sequences and one in txt format (without whitespace) 
time = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')

# Create FASTA file (with linebreaks)
out_file = path+"/"+ID+"_clipped_"+time+".fasta"
f = open(out_file, "a")
f.write(">"+ID+" clipped\n")
for i in range(0,len(output),60):
	f.write(output[i:i+60] + "\n")
f.close()

# Create txt file (without linebreaks)
out_file2 = path+"/"+ID+"_raw_"+time+".txt"
f2 = open(out_file2, "a")
f2.write("> "+ID+" clipped\n")
f2.write(output)
f2.close()

print("Output was saved to file '"+out_file+"'.")

print()
