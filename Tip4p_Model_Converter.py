import numpy as np

data=open('smd.data','r')
dataresult=open('Atom.txt','w')
wholestr=data.read()
(other,Atomandother)=wholestr.split("Atoms # full\n\n")
(atomstr,otherandbond)=Atomandother.split("\n\nBonds\n\n")
(bondstr,anglestr)=otherandbond.split("\n\nAngles\n\n")
dataatom=open('atomstr.txt','w')
databond=open('bondstr.txt','w')
dataatom.write(atomstr)
databond.write(bondstr)

atomlist=list(atomstr.split('\n'))
bondlist=list(bondstr.split('\n'))
anglelist=list(anglestr.split('\n'))
listOw=[]
listHw=[]
listCm=[]
listHm=[]
type_C='3'
type_Hm='4'
type_Ow='1'
type_Hw='2'
type_methane='2'
type_water='1'
# =============================================================================
# 分别将每种Type存入列表
# =============================================================================
for eachatom in atomlist:
    if eachatom != '':
        number,mtype,atype,others=eachatom.split(maxsplit=3)
    
        if atype == type_C:
            
            listCm.append([number,mtype,atype,others])
        elif atype == type_Hm:
            listHm.append([number,mtype,atype,others])
    
        elif atype== type_Ow:
            
            listOw.append([number,mtype,atype,others])
        else:
            listHw.append([number,mtype,atype,others])
                
matrixCm=np.array(listCm)
matrixHm=np.array(listHm)
matrixOw=np.array(listOw)
matrixHw=np.array(listHw)
Spc=' '
host=[]

# =============================================================================
# 将普通data文件转换为Tip4p，即O-H-H格式，且不破坏Bond、Angle等结构的顺序
# =============================================================================
# 依靠Bond列表建立关系
# =============================================================================
# =============================================================================

for eachbond in bondlist:
    numberofbond,moleculartype,Numberi,Numberj=eachbond.split()

    if moleculartype == type_methane:
        if Numberi not in host:
            where=matrixCm[:,0]==Numberi
            strCm=matrixCm[where][0]
            dataresult.write(Spc+strCm[0]+Spc+strCm[1]+Spc+strCm[2]+Spc+strCm[3]+'\n')
        where=matrixHm[:,0]==Numberj
        strHm=matrixHm[where][0]
        dataresult.write(Spc+strHm[0]+Spc+strHm[1]+Spc+strHm[2]+Spc+strHm[3]+'\n')
        host.append(Numberi)
    else:
        if Numberi not in host:
           where=matrixOw[:,0]==Numberi
           if True not in where:
               pause()
           strOw=matrixOw[where][0]
           dataresult.write(Spc+strOw[0]+Spc+strOw[1]+Spc+strOw[2]+Spc+strOw[3]+'\n')
        where=matrixHw[:,0]==Numberj
        strHw=matrixHw[where][0]
        dataresult.write(Spc+strHw[0]+Spc+strHw[1]+Spc+strHw[2]+Spc+strHw[3]+'\n')
        host.append(Numberi)
dataresult.close()
Data=open('Atom.txt','r')
result=open('result.txt','w')
LINES=Data.readlines()
dictionary=dict()
# =============================================================================
# 根据重新排列的Atom，对Angles等重新替换
#使用字典替换
# =============================================================================
for linenum in range(len(LINES)):#生成对照字典
    number,others=LINES[linenum].split(maxsplit=1)
    dictionary.update({number:str(linenum+1)})
    result.write(Spc+str(linenum+1)+Spc+others)
result.write('\n\nBonds\n\n')
for eachline in bondlist:
    numberofbond,moleculartype,Numberi,Numberj=eachline.split()
    result.write(Spc+numberofbond+Spc+moleculartype+Spc+dictionary.get(Numberi)+Spc+dictionary.get(Numberj)+'\n')
result.write('\n\nAngles\n\n') 
for eachline in anglelist:
    if eachline=='':
        continue
    numberofbond,moleculartype,Numberi,Numberj,Numberk=eachline.split()
    result.write(Spc+numberofbond+Spc+moleculartype+Spc+dictionary.get(Numberi)+Spc+dictionary.get(Numberj)+Spc+dictionary.get(Numberk)+'\n')
result.close()               