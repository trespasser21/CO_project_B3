opcode={"add":"00000","sub":"00001","mov_imm":"00010","mov":"00011","ld":"00100","st":"00101","mul":"00110","div":"00111","rs":"01000","ls":"01001","xor":"01010","or":"01011","and":"01100","not":"01101","cmp":"01110","jmp":"01111","jlt":"11100","jgt":"11101","je":"11111","hlt":"11010"}
Registers_code = {'R0': "000", 'R1': "001", 'R2': "010", 'R3': "011", 'R4': "100", 'R5': "101", 'R6': "110", 'FLAGS': "111"}
Type_A = ['add', 'sub', 'mul', 'xor', 'or', 'and']
Type_B = ['mov_imm', 'rs', 'ls']
Type_C = ['mov', 'div', 'not', 'cmp']
Type_D = ['ld', 'st']
Type_E = ['jmp', 'jlt', 'jgt', 'je']
complete_list = ['add', 'sub', 'mul', 'xor', 'or', 'and', 'mov', 'rs', 'ls', 'div', 'not', 'cmp', 'ld', 'st', 'jmp',
                 'jlt', 'jgt', 'je', 'hlt', 'var']
variables={}
labels={}
Type_F = ['hlt']
def TA(opd,reg1,reg2,reg3):
    z=opcode[opd]
    z+="00"
    z+=Registers_code[reg1]
    z+=Registers_code[reg2]
    z+=Registers_code[reg3]
    return z
def TB(opd,reg1,immval):
    z=opcode[opd]
    z+="0"
    z+=Registers_code[reg1]
    z+=immval
    return z
def TC(opd,reg1,reg2):
    z=opcode[opd]
    z+="00000"
    z+=Registers_code[reg1]
    z+=Registers_code[reg2]
    return z
def TD(opd,reg1,memaddr):
    z=opcode[opd]
    z+="0"
    z+=Registers_code[reg1]
    z+=memaddr
    return z
def TE(opd,memaddr):
    z=opcode[opd]
    z+="0000"
    z+=memaddr
    return z
def TF(opd):
    z=opcode[opd]
    z+="00000000000"
    return z
def reverse(strs):
    return strs[::-1]
def dec_bin(num):
    strs = ""
    if(num==0):
        return "0"
    while num:
        if (num & 1):
            strs += "1"
        else:
            strs += "0"
        num >>= 1
    return reverse(strs)
f=open("f.txt","r")
f=f.readlines()
s=[]
for i in range(len(f)):
    a=(f[i].split())
    if (a!=[]):
        s.append(a)
count_step_for_var_mem=0
hc=0                
for i in range(len(s)):
    for j in range(len(s[i])):
        p=s[i][j]
        if(p=='hlt'):
            hc+=1
if hc < 1:
    print('Missing hlt instruction')
    quit()
if hc > 1:
    print('Excess use of hlt instruction.')
    quit()
if 'hlt' not in s[-1]:
    print('hlt is not used as last instruction')
    quit()
for i in range(len(s)):
    if(s[i][0]!="var"):
        count_step_for_var_mem+=1
xy=len(s)-count_step_for_var_mem
for i in range(xy,len(s)):
    if(s[i][0]=="mov"):
        if(s[i][2] not in Registers_code.keys()):
            s[i][0]="mov_imm"
    elif(s[i][0][-1]==":"):
        if(s[i][1]=="mov"):
            if(s[i][3] not in Registers_code.keys()):
                s[i][1]="mov_imm"
label_addr=0
label_addr_lst=[]
for i in range(len(s)):
    if (s[i][0] in Type_E):
        ab=s[i][1]+":"
        for j in range(len(s)):
            if(s[j][0]==ab):
                label_addr=j-xy-1
                label_addr_lst.append(label_addr)
count=0
output=[]
binary=[]
itr=0
line_num=0
error_halt=0
en=0
label=0
c = 0
for i in range(len(s)):
        sub = s[i]
        if len(sub)>0:
            if sub[0] == '':  
                continue
            if sub[0] != 'var':
                c += 1
            if sub[0][-1] == ':':  
                for h in sub[0][:-1]:  
                    if not (h.isalnum()) and h != "_":
                        print("error")
                        quit()
                labels[sub[0][:-1]] = c - 1
n = 0
v = 0
flag = False
var_val=0
for i in range(len(s)):
    sub = s[i]
    if len(sub)>0:
        if sub[0] == '': 
            continue 
        if sub[0] == 'var' and flag ==False:
            if len(sub) == 2:
                variables[sub[1]] = c 
                c += 1  
            else:
                print('Variable error.')
                quit()
        elif sub[0]== 'var' and flag ==True:
            print('Variable not declared in the beginning')
            quit()
        else:
            flag = True
        if sub[0][:-1] in labels.keys():
            sub = sub[1:]
        n += 1
        if sub[0] in Type_A:
            if len(sub)>4:
                print("Contains more than 3 parameters on line", n)
                quit()
            elif len(sub)<4:
                print("Contains less than 3 parameters on line", n)
                quit()
            elif sub[1] in Registers_code.keys() and sub[2] in Registers_code.keys() and sub[3] in Registers_code.keys() and len(sub) == 4:
                if 'FLAGS' in sub:
                    print("Illegal use of flags register at line ",n)
                    quit()
                print(TA(sub[0], sub[1], sub[2], sub[3]))            
            elif sub[1] not in Registers_code.keys() or sub[2] not in Registers_code.keys() or sub[3] not in Registers_code.keys() and len(sub) == 4:
                print("Register name error on line", n)
                quit()                        
            else:
                print("general syntax error at line", n)
                quit()
        elif sub[0] in Type_B:
            if len(sub)>3:
                print("Contains more than 2 parameters on line", n)
                quit()
            elif len(sub)<3:
                print("Contains less than 2 parameters on line", n)
                quit()
            elif sub[1] in Registers_code.keys() and len(sub) == 3 and sub[2][0]=="$" and 0<=int(sub[2][1:])<=256:
                imm_val=sub[2][1:]
                imm_val=int(imm_val)
                imm_val=dec_bin(imm_val)
                if(len(imm_val)<7):
                    imm_val="0"*(7-len(imm_val))+imm_val
                print(TB(sub[0], sub[1], imm_val))
            elif sub[1] not in Registers_code.keys() and len(sub) == 3:
                print("Register name error on line", n)
                quit()
            elif sub[2][0]!="$" and len(sub) == 3:
                print("Immediate Value Syntax Error at Line", n)
                quit()
            elif int((sub[2][1:]) not in [0,256]) and len(sub) == 3:
                print("Immediate Value out of range at line", n)
                quit()
            else:
                print("general syntax error at line", n)
                quit()
        elif sub[0] in Type_C:
            if len(sub)>3:
                print("Contains more than 2 parameters on line", n)
                quit()
            elif len(sub)<3:
                print("Contains less than 2 parameters on line", n)
                quit()
            elif sub[1] in Registers_code.keys() and sub[2] in Registers_code.keys() and len(sub) == 3:
                # if 'FLAGS' in sub:
                #     print("Illegal use of flags register at line ",n)
                #     quit()
                print(TC(sub[0], sub[1], sub[2]))
            elif sub[1] not in Registers_code.keys() or sub[2] not in Registers_code.keys() and len(sub) == 3:
                print("Register name error on line", n)
                quit()
            elif len(sub) > 3:
                print("You can not compare more than two elements at line", n)
                quit()
            else:
                print("general syntax error at line", n)
                quit()
        elif sub[0] in Type_D:
            if len(sub)>3:
                print("Contains more than 2 parameters on line", n)
                quit()
            elif len(sub)<3:
                print("Contains less than 2 parameters on line", n)
                quit()
            elif sub[2] in variables.keys() and sub[1] in Registers_code.keys() and len(sub)==3:
                if 'FLAGS' in sub:
                    print("Illegal use of flags register")
                    quit()
                count=count_step_for_var_mem+var_val
                count=dec_bin(count)
                if(len(count)<7):
                    count="0"*(7-len(count))+count
                print(TD(sub[0], sub[1], count))
                var_val+=1
            elif sub[1] not in Registers_code.keys() and len(sub)==3:
                print("Register name error on line", n)
                quit()
            elif sub[2] not in variables.keys() and len(sub)==3:
                print('Use of undefined variables at line', n)
                quit()
            else:
                print("General sybtax error on line", n)
                quit()
        elif sub[0] in Type_E:
            if len(sub)>2:
                print("Contains more than 1 parameters on line", n)
                quit()
            elif len(sub)<2:
                print("Contains less than 1 parameters on line", n)
                quit()
            if sub[1] not in labels.keys():
                print('Use of undefined labels at line', n)
                quit()
            if 'FLAGS' in sub:
                print("Illegal use of flags register at line ",n)
                quit()
            count=label_addr_lst[label]+1
            count=dec_bin(count)
            if(len(count)<7):
                count="0"*(7-len(count))+count
            print(TE(sub[0], count))
            label+=1
        elif sub[0] == 'hlt':
            print(TF(sub[0]))
        elif(sub[0] not in complete_list) and (sub[0][-1]==":"):
            if sub[1] in Type_A:
                if len(sub)>5:
                    print("Contains more than 3 parameters on line", n)
                    quit()
                elif len(sub)<5:
                    print("Contains less than 3 parameters on line", n)
                    quit()
                elif sub[2] in Registers_code.keys() and sub[3] in Registers_code.keys() and sub[4] in Registers_code.keys() and len(sub) == 5:
                    if 'FLAGS' in sub:
                        print("Illegal use of flags register at line ",n)
                        quit()
                    print(TA(sub[1], sub[2], sub[3], sub[4]))
                elif sub[2] not in Registers_code.keys() or sub[3] not in Registers_code.keys() or sub[4] not in Registers_code.keys() and len(sub) == 5:
                    print("Register name error on line", n)
                    quit()
                elif len(sub)>4:
                    print("Contains more than 3 parameters on line", n)
                    quit()
                elif len(sub)<4:
                    print("Contains less than 3 parameters on line", n)
                    quit()
                else:
                    print("general syntax error at line", n)
                    quit()
            elif sub[1] in Type_B:
                if len(sub)>4:
                    print("Contains more than 2 parameters on line", n)
                    quit()
                elif len(sub)<4:
                    print("Contains less than 2 parameters on line", n)
                    quit()
                elif sub[2] in Registers_code.keys() and len(sub) == 4 and sub[3][0]=="$" and 0<=int(sub[3][1:])<=256:
                    imm_val=sub[3][1:]
                    imm_val=int(imm_val)
                    imm_val=dec_bin(imm_val)
                    if(len(imm_val)<7):
                        imm_val="0"*(7-len(imm_val))+imm_val
                    print(TB(sub[1], sub[2], imm_val))
                elif sub[2] not in Registers_code.keys() and len(sub) == 4:
                    print("Register name error on line", n)
                    quit()
                elif sub[3][0]!="$" and len(sub) == 4:
                    print("Immediate Value Syntax Error at Line", n)
                    quit()
                elif int((sub[3][1:]) not in [0,256]) and len(sub) == 4:
                    print("Immediate Value out of range at line", n)
                    quit()
                else:
                    print("general syntax error at line", n)
                    quit()
            elif sub[1] in Type_C:
                if len(sub)>4:
                    print("You can not compare more than two elements at line", n)
                    quit()
                elif len(sub)<4:
                    print("Contains less than 2 parameters on line", n)
                    quit()
                elif sub[2] in Registers_code.keys() and sub[3] in Registers_code.keys() and len(sub) == 4:
                    if 'FLAGS' in sub:
                        print("Illegal use of flags register at line ",n)
                        quit()
                    print(TC(sub[1], sub[2], sub[3]))
                elif sub[2] not in Registers_code.keys() or sub[3] not in Registers_code.keys() and len(sub) == 4:
                    print("Register name error on line", n)
                    quit()
                else:
                    print("general syntax error at line", n)
                    quit()
            elif sub[1] in Type_D:
                if len(sub)>4:
                    print("Contains more than 2 parameters on line", n)
                    quit()
                elif len(sub)<4:
                    print("Contains less than 2 parameters on line", n)
                    quit()
                elif sub[3] in variables.keys() and sub[2] in Registers_code.keys() and len(sub)==4:
                    if 'FLAGS' in sub:
                        print("Illegal use of flags register")
                        quit()
                    count=count_step_for_var_mem+var_val
                    count=dec_bin(count)
                    if(len(count)<7):
                        count="0"*(7-len(count))+count
                    print(TD(sub[1], sub[2], count))
                    var_val+=1
                elif sub[2] not in Registers_code.keys() and len(sub)==4:
                    print("Register name error on line", n)
                    quit()
                elif sub[3] not in variables.keys() and len(sub)==4:
                    print('Use of undefined variables at line', n)
                    quit()
                else:
                    print("General sybtax error on line", n)
                    quit()  
            elif sub[1] in Type_E:
                if len(sub)>3:
                    print("Contains more than 2 parameters on line", n)
                    quit()
                elif len(sub)<3:
                    print("Contains less than 2 parameters on line", n)
                    quit()
                if sub[2] not in labels.keys():
                    print('Use of undefined labels at line', n)
                    quit()
                if 'FLAGS' in sub:
                    print("Illegal use of flags register at line ",n)
                    quit()
                count=label_addr_lst[label]+1
                count=dec_bin(count)
                if(len(count)<7):
                    count="0"*(7-len(count))+count
                print(TE(sub[1], count))
                label+=1
            elif sub[1] == 'hlt':
                print(TF(sub[1]))
        elif(sub[0] not in complete_list) and (sub[0][-1]!=":"):
            print("typo error at line ",n)
            quit()
            
f.close()
# for input : for kx in sys.stdin:
#                  cmd_list.append(kx)
# for output : sys.stdout.write("YourAnsString")  
