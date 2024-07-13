import xml.etree.ElementTree as ET
import numpy as np
import sys
from array import *

# script tests XML output to verify that simulation has been run with correct
# fixed parameters

# we will check:
#mass1
#mass2
#NUpdatesThisRun
#nrow
#degree
#n_smear
#rho
#FermAct
#CudaSloppyPrecision
#CudaSloppyReconstruct
#CudaRefinementPrecision
#CudaRefinementReconstruct
#lowerMin
#upperMax
#solver masses 




test_filename =sys.argv[1]                 # supply the path to the test file

# read in some parameters that we might tune
mass0_ref     =float(sys.argv[2])                 # light mass
mass1_ref     =float(sys.argv[3])                 # heavier mass
resid_ref     =float(sys.argv[4])                 # inverse residual
updates_ref   =int(sys.argv[5])               # How many updates were requested
Lx_ref        =int(sys.argv[6])        #spatial extent of lattice
Lt_ref        =int(sys.argv[7])        #time extent of lattice

#hard code some that we never change
rho_ref = 0.11
FermAct_ref="CLOVER"
CudaSloppyPrecision_ref="SINGLE"
CudaSloppyReconstruct_ref="RECONS_12"
CudaRefinementPrecision_ref="HALF"
CudaRefinementReconstruct_ref="RECONS_8"
lowerMin_ref=1e-4
upperMax_ref=100
action_degree_ref=14
force_degree_ref=8
act_inv_resid_shape_ref=(2,14)
force_inv_resid_shape_ref=(2,6)
nsmear_ref=6;
tau0_ref=1.0
integrator_nsteps_ref=1
sub_integrator_nsteps_ref=1
sub_sub_integrator_nsteps_ref=1
integrator_monomial0_ref="constdet_strange_3flav"
integrator_monomial1_ref="constdet_charm_1flav"
sub_integrator_monomial0_ref="HMC::logdet_3flav"
sub_integrator_monomial1_ref="HMC::logdet_1flav"
sub_sub_integrator_monomial0_ref="gauge"

integrator_name_ref="LCM_STS_MIN_NORM_2"
sub_integrator_name_ref="LCM_STS_MIN_NORM_2"
sub_sub_integrator_name_ref="LCM_STS_MIN_NORM_2"


act_mass_array=[]
act_inv_masses=[]
force_inv_masses=[]

action_inverse_residuals=[]
force_inverse_residuals=[]
int_monomial_names=[]
sub_int_monomial_names=[]
sub_sub_int_monomial_names=[]

#Start with the assumption of correctness
correct=1




#First hard-code some paths in the XML output file

updates_path1="Input/Params/MCControl/NUpdatesThisRun"

#information about physics is encoded in 3 places:
action_mass_path="Input/Params/HMCTrj/Monomials/elem/Action/FermionAction"
action_inv_path="Input/Params/HMCTrj/Monomials/elem/Action/ActionApprox/InvertParam"
force_inv_path="Input/Params/HMCTrj/Monomials/elem/Action/ForceApprox/InvertParam"

#polynomial approximations are needed for the force and the action
act_rat_approx_path="Input/Params/HMCTrj/Monomials/elem/Action/ActionApprox/RationalApprox"
force_rat_approx_path="Input/Params/HMCTrj/Monomials/elem/Action/ForceApprox/RationalApprox"


#We will need to check some details of the fermion action
smear_path1="Input/Params/HMCTrj/Monomials/elem/Action/FermionAction/FermState/n_smear"
smear_path2="Input/Params/HMCTrj/Monomials/elem/FermionAction/FermState/n_smear"
rho_path1="Input/Params/HMCTrj/Monomials/elem/Action/FermionAction/FermState/rho"
rho_path2="Input/Params/HMCTrj/Monomials/elem/FermionAction/FermState/rho"

integrator_path="Input/Params/HMCTrj/MDIntegrator"


# parse reference file XML
ref_tree = ET.parse(test_filename)
ref_root = ref_tree.getroot()



# find quark masses in action
for mass in ref_root.iterfind(action_mass_path):
    m=float(mass.find('Mass').text)
    act_mass_array.append(m)


#we should now have two masses --- check them
len_act_mass=len(act_mass_array)
if len_act_mass!= 2:
    print("Have ",len_act_mass, "should have 2; fail")
    correct=0
    
#Check against reference masses
if act_mass_array[0]!=mass0_ref or  act_mass_array[1]!=mass1_ref:
    print("Action Mass mismatch; fail")
    print("M0: ",act_mass_array[0]," vs ",mass0_ref )
    print("M1: ",act_mass_array[1]," vs ",mass1_ref )
    correct=0

# find quark masses and residuals in action inverter
for act_inv in ref_root.iterfind(action_inv_path):
    mass_val=float(act_inv.find('CloverParams/Mass').text)
    act_inv_masses.append(mass_val)
    rsd_vals_str=np.array((act_inv.find('RsdTarget').text).split())
    rsd_vals1=rsd_vals_str.astype(float)
    action_inverse_residuals.append(rsd_vals1)

action_inverse_residuals=np.array(action_inverse_residuals)
act_inv_resid_shape=action_inverse_residuals.shape

# first check that we have two masses for computing the action inverse
len_act_inverse_mass=len(act_inv_masses)
if len_act_inverse_mass!=2 :
    print("Have ",len_act_inverse_mass, "masses for action inverse; should have 2; fail")
    correct=0
   
#Now check these against reference masses
if act_inv_masses[0]!=mass0_ref or  act_inv_masses[1]!=mass1_ref:
    print("Action Inverse Mass mismatch; fail")
    print("M0: ",act_inv_masses[0]," vs ",mass0_ref )
    print("M1: ",act_inv_masses[1]," vs ",mass1_ref )
    correct=0


#Check that we have the correct number of action inverse residuals
if act_inv_resid_shape != act_inv_resid_shape_ref:
    print("Action Inv. residuals have shape: ",act_inv_resid_shape, "should have ",act_inv_resid_shape_ref,"; fail")
    correct=0



#Check that we have the correct number of action inverse residuals
for q in action_inverse_residuals:
    for r in q: 
        if r!=resid_ref:
            print("Mismatch in action inverse residuals.",r,"instead of ",resid_ref,";fail")
            correct=0




#Now check the Force inverter parameters
for force_inv in ref_root.iterfind(force_inv_path):
    mass_val=float(force_inv.find('CloverParams/Mass').text)
    force_inv_masses.append(mass_val)

    rsd_vals_str=np.array((force_inv.find('RsdTarget').text).split())
    rsd_vals1=rsd_vals_str.astype(float)

    force_inverse_residuals.append(rsd_vals1)


force_inverse_residuals=np.array(force_inverse_residuals)
frc_inv_resid_shape=force_inverse_residuals.shape

# first check that we have two masses for computing the force inverse
len_force_inverse_mass=len(force_inv_masses)
if len_force_inverse_mass!=2 :
    print("Have ",len_force_inverse_mass, "masses for force inverse; should have 2; fail")
    correct=0
   


#Now check these against reference masses
if force_inv_masses[0]!=mass0_ref or  force_inv_masses[1]!=mass1_ref:
    print("Force Inverse Mass mismatch; fail")
    print("M0: ",force_inv_masses[0]," vs ",mass0_ref )
    print("M1: ",force_inv_masses[1]," vs ",mass1_ref )
    correct=0


    

#Check polynomial degree for action  approximation
for act_rat_approx in ref_root.findall(act_rat_approx_path):
    act_degree_all=act_rat_approx.findall("degree")
    for d in act_degree_all:
        deg=int(d.text)
        if deg != action_degree_ref:
            print ("Action degree mismatch ", deg," vs ", action_degree_ref,"; fail")
            correct=0

#Check polynomial degree for force  approximation
for force_rat_approx in ref_root.findall(force_rat_approx_path):
    force_degree_all=force_rat_approx.findall("degree")
    for d in force_degree_all:
        deg=int(d.text)
        if deg != force_degree_ref:
            print ("Force degree mismatch ", deg," vs ", force_degree_ref,"; fail")
            correct=0




#Updates should appear just once in the XML
updates=ref_tree.findall(".//NUpdatesThisRun")
for updt in updates:
    upd=int(updt.text)
    if upd!=updates_ref :
        print("Mismatch in num updates", upd, "vs ",updates_ref, "; fail." )
        correct=0


#Check problem dimensions --  should appear just once in the XML      
dims=ref_tree.findall(".//nrow")
dims_ref=[Lx_ref, Lx_ref, Lx_ref, Lt_ref ]
for d in dims:
    dims_string=np.array(d.text.split())
    dims_ints=dims_string.astype(int)
    if dims_ints[0]!=Lx_ref  or  dims_ints[1]!=Lx_ref  or  dims_ints[2]!=Lx_ref or   dims_ints[3]!=Lt_ref:
        print("Dims mismatch:", dims_ints , "instead of ", dims_ref, "; Fail")
        correct=0

#all instances of n_smear should be the same

all_smears=ref_tree.findall(".//n_smear")
for s in all_smears:
    n_smear=int(s.text)
    if n_smear != nsmear_ref:
        print("n_smear mismatch:",n_smear, "vs ", nsmear_ref,"; Fail")
        correct=0
 
        
    
    
#all instances of rho should be the same
all_rho=ref_tree.findall(".//rho")
for r in all_rho:
    rho=float(r.text)
    if rho != rho_ref:
        print("rho mismatch:",rho, "vs ", rho_ref,"; Fail")
        correct=0
 
#all instances of FermAct should be the same
fermacts=ref_tree.findall(".//FermAct")
for f in fermacts:
    FermAct=(f.text)
    if FermAct != FermAct_ref:
        print("FermAct mismatch:",FermAct, "vs ", FermAct_ref,"; Fail")
        correct=0

    
#all instances of CudaSloppyPrecision should be the same
sloppP=ref_tree.findall(".//CudaSloppyPrecision")
for sp in sloppP:
    SloppyPrec=sp.text
    if SloppyPrec  != CudaSloppyPrecision_ref:
        print("CudaSloppyPrecision mismatch:",SloppyPrec, "vs ", CudaSloppyPrecision_ref,"; Fail")
        correct=0

#all instances of CudaSloppyReconstruct should be the same
sloppR=ref_tree.findall(".//CudaSloppyReconstruct")
for sr in sloppR:
    SloppyRecon=sr.text
    if SloppyRecon  != CudaSloppyReconstruct_ref:
        print("CudaSloppyReconstruct mismatch:",SloppyRecon, "vs ", CudaSloppyReconstruct_ref,"; Fail")
        correct=0


#all instances of CudaRefinementPrecision should be the same
refPrec=ref_tree.findall(".//CudaRefinementPrecision")
for rp in refPrec:
    RefinementPrec=rp.text
    if RefinementPrec  != CudaRefinementPrecision_ref:
        print("CudaRefinementPrecision mismatch:", RefinementPrec, "vs ", CudaRefinementPrecision_ref,"; Fail")
        correct=0

#all instances of CudaRefinementReconstruct should be the same
refRecon=ref_tree.findall(".//CudaRefinementReconstruct")
for rr in refRecon:
    RefinementRecon=rr.text
    if RefinementRecon  != CudaRefinementReconstruct_ref:
        print("CudaRefinementReconstruct mismatch:", RefinementRecon, "vs ", CudaRefinementReconstruct_ref,"; Fail")
        correct=0


#all instances of lowerMin should be the same
lowmin=ref_tree.findall(".//lowerMin")
for lm in lowmin:
    lowerMin=float(lm.text)
    if lowerMin  != lowerMin_ref:
        print("lowerMin mismatch:", lowerMin, "vs ", lowerMin_ref,"; Fail")
        correct=0


#all instances of upperMax should be the same  
upmax=ref_tree.findall(".//upperMax")
for um in upmax:
    upperMax=float(um.text)
    if upperMax  != upperMax_ref:
        print("upperMax mismatch:", upperMax, "vs ", upperMax_ref,"; Fail")
        correct=0




#Check integrator parameters
#outer integrator
#check tau0
integrator=ref_root.find(integrator_path)
tau=float(integrator.find(".//tau0").text)
if tau != tau0_ref:
    print("tau0 mismatch:", tau, "vs ", tau0_ref,"; Fail")
    correct=0

#check integrator name
integrator_name=(integrator.find(".//Integrator/Name").text)
if integrator_name !=  integrator_name_ref:
    print("integrator_name mismatch:", integrator_name, "vs ", integrator_name_ref,"; Fail")
    correct=0
  
#check integrator n_steps
integrator_nsteps=int(integrator.find(".//Integrator/n_steps").text)
if integrator_nsteps !=  integrator_nsteps_ref:
    print("integrator_nsteps mismatch:", integrator_nsteps, "vs ", integrator_nsteps_ref,"; Fail")
    correct=0

#check integrator monomials
integrator_monos=integrator.findall(".//Integrator/monomial_ids/elem")
for im in integrator_monos:
    int_monomial_names.append(im.text)

#check that we have 2
if len(int_monomial_names) !=2:
    print("wrong number of outer integrator monomials:", len(int_monomial_names), " vs 2")
    correct=0

if int_monomial_names[0] != integrator_monomial0_ref or int_monomial_names[1] != integrator_monomial1_ref:
    print("integrator monomial mismatch:")
    print( int_monomial_names[0], "vs ",integrator_monomial0_ref )
    print( int_monomial_names[1], "vs ",integrator_monomial1_ref )
    correct =0



#check SUB-integrator

#check subintegrator name
sub_integrator_name=(integrator.find(".//Integrator/SubIntegrator/Name").text)
if sub_integrator_name !=  sub_integrator_name_ref:
    print("sub-integrator_name mismatch:", sub_integrator_name, "vs ", sub_integrator_name_ref,"; Fail")
    correct=0



#check sub-integrator n_steps
sub_integrator_nsteps=int(integrator.find(".//Integrator/SubIntegrator/n_steps").text)
if sub_integrator_nsteps !=  sub_integrator_nsteps_ref:
    print("sub-integrator_nsteps mismatch:", sub_integrator_nsteps, "vs ", sub_integrator_nsteps_ref,"; Fail")
    correct=0







#check sub-integrator monomials
sub_integrator_monos=integrator.findall(".//Integrator/SubIntegrator/monomial_ids/elem")
for sim in sub_integrator_monos:
    sub_int_monomial_names.append(sim.text)

#check that we have 2
if len(sub_int_monomial_names) !=2:
    print("wrong number of SUB integrator monomials:", len(sub_int_monomial_names), " vs 2")
    correct=0

#check that the sub-integrator monomials are correct    
if sub_int_monomial_names[0] != sub_integrator_monomial0_ref or sub_int_monomial_names[1] != sub_integrator_monomial1_ref:
    print("SUB-integrator monomial mismatch:")
    print( sub_int_monomial_names[0], "vs ",sub_integrator_monomial0_ref )
    print( sub_int_monomial_names[1], "vs ",sub_integrator_monomial1_ref )
    correct =0






#check SUB-SUB-integrator

#check sub_sub_integrator name
sub_sub_integrator_name=(integrator.find(".//Integrator/SubIntegrator/SubIntegrator/Name").text)
if sub_sub_integrator_name !=  sub_sub_integrator_name_ref:
    print("SUB-SUB-integrator_name mismatch:", sub_sub_integrator_name, "vs ", sub_sub_integrator_name_ref,"; Fail")
    correct=0



#check SUB-SUB-integrator n_steps
sub_sub_integrator_nsteps=int(integrator.find(".//Integrator/SubIntegrator/SubIntegrator/n_steps").text)
if sub_sub_integrator_nsteps !=  sub_sub_integrator_nsteps_ref:
    print("sub_sub-integrator_nsteps mismatch:", sub_sub_integrator_nsteps, "vs ", sub_sub_integrator_nsteps_ref,"; Fail")
    correct=0





#check SUB-sub-integrator monomials
sub_sub_integrator_monos=integrator.findall(".//Integrator/SubIntegrator/SubIntegrator/monomial_ids/elem")
for ssim in sub_sub_integrator_monos:
    sub_sub_int_monomial_names.append(ssim.text)

#check that we have 1 --- Gauge monomial only
if len(sub_sub_int_monomial_names) !=1:
    print("wrong number of SUB-SUB integrator monomials:", len(sub_sub_int_monomial_names), " vs 1")
    correct=0
if sub_sub_int_monomial_names[0] != sub_sub_integrator_monomial0_ref:
    print("SUB-SUB-integrator monomial mismatch:")
    print( sub_sub_int_monomial_names[0], "vs ",sub_sub_integrator_monomial0_ref )

    correct =0







    
    
#Now determine whether the file passes the validation globally
if correct==1:
    print("INPUT VALIDATION: PASS")
else:
    print("INPUT VALIDATION: FAIL")
    
