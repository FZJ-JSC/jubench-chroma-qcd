import xml.etree.ElementTree as ET
import numpy as np
import sys
from array import *

# script extracts correlator from two XML output files and tests if they are numerically similar enough


ref_filename=sys.argv[1]                          # supply  the path to a reference file
test_filename=sys.argv[2]                         # supply the path to the test file


correctness_threshold=float(sys.argv[3])          # here is the relative difference threshold for PASS/FAIL


#make some emty arrays for the correlators
ref_wplaq_array=[]
ref_splaq_array=[]
ref_tplaq_array=[]
ref_p23plaq_array=[]

test_wplaq_array=[]
test_splaq_array=[]
test_tplaq_array=[]
test_p23plaq_array=[]


# parse reference file XML
ref_tree = ET.parse(ref_filename)
ref_root = ref_tree.getroot()

#print ("RR=",ref_root)


for ref_plaq in ref_root.iterfind("doHMC/MCUpdates/elem/Update/InlineObservables/elem/Plaquette"):
    wplaq=float(ref_plaq.find('w_plaq').text)
    splaq=float(ref_plaq.find('s_plaq').text)
    tplaq=float(ref_plaq.find('t_plaq').text)
    p23plaq=float(ref_plaq.find('plane_23_plaq').text)

    ref_wplaq_array.append(float(wplaq))
    ref_splaq_array.append(float(splaq))
    ref_tplaq_array.append(float(tplaq))
    ref_p23plaq_array.append(float(p23plaq))
 #   print ("plaq is",wplaq)


# parse test file XML
test_tree = ET.parse(test_filename)
test_root = test_tree.getroot()

for test_plaq in test_root.iterfind("doHMC/MCUpdates/elem/Update/InlineObservables/elem/Plaquette"):
    wplaq=float(test_plaq.find('w_plaq').text)
    splaq=float(test_plaq.find('s_plaq').text)
    tplaq=float(test_plaq.find('t_plaq').text)
    p23plaq=float(test_plaq.find('plane_23_plaq').text)


    test_wplaq_array.append(float(wplaq))
    test_splaq_array.append(float(splaq))
    test_tplaq_array.append(float(tplaq))
    test_p23plaq_array.append(float(p23plaq))
#    print ("plaq is",wplaq)


idx=len(ref_wplaq_array)-1

    
#
max_diff=0.0

#wplaq diff
rel_diff_w = abs((test_wplaq_array[idx]-ref_wplaq_array[idx])/ref_wplaq_array[idx])
if rel_diff_w > max_diff:
    max_diff=rel_diff_w

#splaq diff
rel_diff_s = abs((test_splaq_array[idx]-ref_splaq_array[idx])/ref_splaq_array[idx])
if rel_diff_s > max_diff:
    max_diff=rel_diff_s

#tplaq diff
rel_diff_t = abs((test_tplaq_array[idx]-ref_tplaq_array[idx])/ref_tplaq_array[idx])
if rel_diff_t > max_diff:
    max_diff=rel_diff_t

#p23_plaq diff
rel_diff_p23 = abs((test_p23plaq_array[idx]-ref_p23plaq_array[idx])/ref_p23plaq_array[idx])
if rel_diff_p23 > max_diff:
    max_diff=rel_diff_p23


print("w-plaquette\t",ref_wplaq_array[idx], test_wplaq_array[idx], rel_diff_w);
print("s-plaquette\t",ref_splaq_array[idx], test_splaq_array[idx], rel_diff_s);
print("t-plaquette\t",ref_tplaq_array[idx], test_tplaq_array[idx], rel_diff_t);
print("P23-plaquette\t",ref_p23plaq_array[idx], test_p23plaq_array[idx], rel_diff_p23);



print ("Threshold max relative deviation for validity test: ", correctness_threshold)
print ("\n\nMax diff = ", max_diff);    

test_pass = 0
if max_diff < correctness_threshold:
    test_pass=1
    print("CHECKVALID: PASS")
else :
    print("CHECKVALID: FAIL")


