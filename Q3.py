opcode={"add":"00000","sub":"00001","mov_imm":"00010","mov":"00011","ld":"00100","st":"00101","mul":"00110","div":"00111","rs":"01000","ls":"01001","xor":"01010","or":"01011","and":"01100","not":"01101","cmp":"01110","jmp":"01111","jlt":"11100","jgt":"11101","je":"11111","hlt":"11010","addf":"10000","subf":"10001","movf":"10010"}
Registers_code = {'R0': "000", 'R1': "001", 'R2': "010", 'R3': "011", 'R4': "100", 'R5': "101", 'R6': "110", 'FLAGS': "111"}
Type_A = ["00000", "00001", "00110", "01010","01011", "01100","10000","10001"]
Type_B = ["00010", "01000", "01001"]
Type_Bf=["10010"]
Type_C = ["00011", "00111", "01101","01110"]
Type_D = ["00100", "00101"]
Type_E = ["01111","11100", "11101", "11111"]
Type_F = ["11010"]
complete_list = ['add', 'sub', 'mul', 'xor', 'or', 'and', 'mov', 'rs', 'ls', 'div', 'not', 'cmp', 'ld', 'st', 'jmp',
                 'jlt', 'jgt', 'je', 'hlt', 'var']
# variables={}
# labels={}
f=open("C:/Users/shubh/Downloads/simulatortestcases.txt","r")
g=f.readlines()
inputs=[]
flag="0"*16
# r1_v=r2_v=r3_v=r4_v=r5_v=r6_v=r0_v= 0
mem_val={}
reg_val={"000":0,"001":0,"010":0,"011":0,"100":0,"101":0,"110":0,"111":int(flag,2)}
items=opcode.items()
def binaryOfFraction(fraction):
	binary = str()
	while (fraction):
		fraction *= 2
		if (fraction >= 1):
			int_part = 1
			fraction -= 1
		else:
			int_part = 0
		binary += str(int_part)
	return binary
def floatingPoint(real_no):
	real_no = abs(real_no)
	int_str = bin(int(real_no))[2 : ]
	fraction_str = binaryOfFraction(real_no - int(real_no))
	ind = int_str.index('1')
	exp_str = bin((len(int_str) - ind - 1) + 3)[2 : ]
	exp_str = exp_str + ('0' * (3 - len(exp_str)))
	mant_str = int_str[ind + 1 : ] + fraction_str
	mant_str = mant_str + ('0' * (5 - len(mant_str)))
	return exp_str, mant_str

itemsr=Registers_code.items()
def d2b(decimal,bits):
    binary=bin(decimal)[2:]  
    binary=binary.zfill(bits)  
    return binary
def print_reg(x):
    ab=d2b(x,7)
    print(ab+" "*8,end="")
    for j,i in reg_val.items():
        if j=="111":
            print(flag)
            break
        if isinstance(i,float) :
            xyz,abc=floatingPoint(i)
            fi="00000000"+xyz+abc
            print(fi,end=" ")
            continue
        cb=d2b(i,16)
        print(cb,end=" ")
    # print("\n")
for i in range(len(g)):
    inputs.append(g[i].strip())
k=0
for j in range(len(inputs)):
    if j<k:
        continue

    i=inputs[j]
    a=i[0:5]
    if a in Type_A:             #TYPE A
        val1=a
        func=[key for key,value in items if value==val1]
        reg1=i[7:10]
        reg2=i[10:13]
        reg3=i[13:16]
        val=func[0]
        x=reg_val[reg2]
        y=reg_val[reg3]
        if val=="add":
            z=x+y
            # z=d2b(z,16)
            reg_val[reg1]=z
            print_reg(j)
            
        if val=="sub":
            z=x-y
            # reg1=d2b(z,16)
            reg_val[reg1]=z
            print_reg(j)
        if val=="mul":
            z=x*y
            # reg1=d2b(z,16)
            reg_val[reg1]=z
            print_reg(j)
        if val=="xor":
            z=x^y
            # reg1=d2b(z,16)
            reg_val[reg1]=z
            print_reg(j)
        if val=="or":
            z=x|y
            # reg1=d2b(z,16)
            reg_val[reg1]=z
            print_reg(j)
        if val=="and":
            z=x&y
            # reg1=d2b(z,16)
            reg_val[reg1]=z
            print_reg(j)
        if val=="addf":
            z=x+y
            if  z<0 or z>127:               #Assuming overflow condition
                flag=flag[0:12]+"1"+"000"
                reg_val[reg1]=0
                reg_val["111"]=1
                print_reg(j)
            else:
                reg_val[reg1]=z
                print_reg(j)
        if val=="subf":
            z=x-y
            if  y>x:
                flag=flag[0:12]+"1"+"000"
                reg_val[reg1]=0
                reg_val["111"]=1
                print_reg(j)
            else:
                reg_val[reg1]=z
                print_reg(j)
    if a in Type_B:             #TYPE B
        val1=a
        func=[key for key,value in items if value==val1]
        val=func[0]
        if val=="mov_imm":
            reg1=i[6:9]
            imm_val=i[9:16]
            # reg1="000000000"+imm_val
            reg_val[reg1]=int(imm_val,2)
            print_reg(j)
        
        elif val=="rs":
            reg1=i[6:9]
            imm_val=i[9:16]
            imm_val=int(imm_val,2)
            ax=reg_val[reg1]
            ax=ax>>imm_val
            # reg1=d2b(reg1,16)
            reg_val[reg1]=ax
            print_reg(j)
        elif val=="ls":
            reg1=i[6:9]
            imm_val=i[9:16]
            imm_val=int(imm_val,2)
            ax=reg_val[reg1]
            ax=ax<<imm_val
            # reg1=d2b(reg1,16)
            reg_val[reg1]=ax
            print_reg(j)
    if a in Type_C:
        val1=a
        func=[key for key,value in items if value==val1]
        val=func[0]
        reg1=i[10:13]
        reg2=i[13:16]
        if val=="mov":
            reg_val[reg1]=reg_val[reg2]
            flag="0"*16
            reg_val["111"]=0
            print_reg(j)
            
        elif val=="div":
            if reg_val[reg2]==0:
                flag=flag[0:12]+"1"+"000"
                reg_val["000"]=0
                reg_val["001"]=0
                print_reg(j)
            else:
                reg_val["000"]=reg_val[reg1]/reg_val[reg2]
                reg_val["001"]=reg_val[reg1]%reg_val[reg2]
                print_reg(j)
        elif val=="not":
            reg_val[reg1]=~reg_val[reg2]
            print_reg(j)
        elif val=="cmp":
            if reg_val[reg1]<reg_val[reg2]:
                flag=flag[0:13]+"1"+"00"
                reg_val["111"]=1
                print_reg(j)
                

            elif reg_val[reg1]>reg_val[reg2]:
                flag=flag[0:14]+"1"+"0"
                reg_val["111"]=1
                print_reg(j)
                
            
            elif reg_val[reg1]==reg_val[reg2]:
                flag=flag[0:15]+"1"
                reg_val["111"]=1
                print_reg(j)
                

    if a in Type_D:
        val1=a
        func=[key for key,value in items if value==val1]
        val=func[0]
        reg1=i[6:9]
        mem_addr=i[9:16]
        if val=="ld":
            if mem_addr in mem_val.keys():
                reg_val[reg1]=mem_val[mem_addr]
                print_reg(j)
            else:
                reg_val[reg1]=0
                mem_val[mem_addr]=0
                print_reg(j)
        elif val=="st":
            mem_val[mem_addr]=reg_val[reg1]
            print_reg(j)
    if a in Type_E:
        val1=a
        func=[key for key,value in items if value==val1]
        mem_addr=i[9:16]
        mem_addr=int(mem_addr,2)
        val=func[0]
        if val=="jmp":
            
            flag="0"*16
            reg_val["111"]=0
            print_reg(j)
            k=mem_addr
        elif val=="jlt":
            if flag[13]=="1":
                
                flag="0"*16
                reg_val["111"]=0
                print_reg(j)
                k=mem_addr
            else:
                reg_val["111"]=0
                print_reg(j)
        elif val=="jgt":
            if flag[14]=="1":
                
                flag="0"*16
                reg_val["111"]=0
                print_reg(j)
             
                k=mem_addr
               
            else:
                reg_val["111"]=0
                print_reg(j)
        elif val=="je":
            if flag[15]=="1":
                
                flag="0"*16
                reg_val["111"]=0
                print_reg(j)
                k=mem_addr
            else:
                reg_val["111"]=0
                print_reg(j)
    if a in Type_Bf:
        val1=a
        func=[key for key,value in items if value==val1]
        reg1=i[5:8]
        imm_val=i[8:16]
        reg_val[reg1]=imm_val
        print_reg(j)
        
    if a in Type_F:
        print_reg(j)
        break

for i in range(len(g)):
    print(g[i].strip())
wwe=128-len(inputs)
for i in range(wwe):
    print("0"*16)