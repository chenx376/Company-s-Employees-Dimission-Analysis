'''
尝试用批处理处理较多情况的traindata以及testdata
2016.8.11
'''

import os
exefile="C:\\Users\\chenxiao\\Desktop\\南天-工作\\员工离职概率\\libsvm-3.21\\windows"
traindatafile="C:\\Users\\chenxiao\\Desktop\\南天-工作\\员工离职概率\\traindata"
testdatafile="C:\\Users\\chenxiao\\Desktop\\南天-工作\\员工离职概率\\testdata"
modulefile="C:\\Users\\chenxiao\\Desktop\\南天-工作\\员工离职概率\\module"
resultfile="C:\\Users\\chenxiao\\Desktop\\南天-工作\\员工离职概率\\result"
tmpfile="C:\\Users\\chenxiao\\Desktop\\南天-工作\\员工离职概率\\tmpresult"
log=">C:\\Users\\chenxiao\\Desktop\\南天-工作\\员工离职概率\\logs\\log.txt"  #保存无用的打印信息
parameterfile="C:\\Users\\chenxiao\\Desktop\\南天-工作\\员工离职概率\\parameter"
parameterexe="C:\\Users\\chenxiao\\Desktop\\南天-工作\\员工离职概率\\libsvm-3.21\\tools"

#参数调节
num_module=len(os.listdir(traindatafile))
for i in range(0,num_module):
    exe="python "+parameterexe+"\\grid.py -gnuplot null -out null "
    data=traindatafile+"\\train_data%d.txt "%(i)
    parameter=">"+parameterfile+"\\parameter%d.txt"%(i)
    train=exe+data+parameter
    os.system(train)
    
#训练模型
for i in range(0,num_module):
    data=parameterfile+"\\parameter%d.txt"%(i)
    file=open(data)
    cont=file.read()
    cont=cont.split()
    exe=exefile+"\\svm-train.exe -c %s -g %s "%(cont[0],cont[1])
    data=traindatafile+"\\train_data%d.txt "%(i)
    module=modulefile+"\\module%d "%(i)
    train=exe+data+module+log
    os.system(train)
    file.close()

#测试数据
line=len(os.listdir(testdatafile))  #获得总的data数
for i in range(1,line):   
    exe=exefile+"\\svm-predict.exe "
    data=testdatafile+"\\test_data%d.txt "%(i)
    outlist=[]
    for j in range(0,num_module):           #用已经获得的n个模型进行预测然后投票
        module=modulefile+"\\module%d "%(j)
        result=tmpfile+"\\result%d.txt "%(j)
        train=exe+data+module+result+log
        os.system(train)
        #对10个已经获得的数据进行投票
        file=open(result)
        output=file.read()
        output=output.replace('\n','')
        outlist.append(output)
        file.close()
    if outlist.count("1")>outlist.count("2"):
        out="1"
    elif outlist.count("1")<outlist.count("2"):
        out="2"
    else:
        out="1"
    outresult=resultfile+"\\result%d.txt "%(i)
    file=open(outresult,'w')
    file.write(out)
    print(i," get result")
    file.close()

#计算正确率和混淆矩阵
confusematrix={"r1p1":0,"r1p2":0,"r2p1":0,"r2p2":0}
sum_right=0
for i in range(1,line):
    data_real=testdatafile+"\\test_data%d.txt "%(i)
    data_predict=resultfile+"\\result%d.txt "%(i) 
    file_reality=open(data_real)
    file_predict=open(data_predict)
    real=file_reality.read()
    real=real[0]
    predict=file_predict.read()
    predict=predict[0]
    if real=="1" and predict=="1":
        confusematrix["r1p1"]+=1
        sum_right+=1
    elif real=="1" and predict=="2":
        confusematrix["r1p2"]+=1
    elif real=="2" and predict=="1":
        confusematrix["r2p1"]+=1
    else:
        confusematrix["r2p2"]+=1
        sum_right+=1
    file_predict.close()
    file_reality.close()   
print ("The result is:\n")
print(confusematrix,"\n")
print(sum_right/line,"%")
    
    
    
            
        
    
    
        
        
    

