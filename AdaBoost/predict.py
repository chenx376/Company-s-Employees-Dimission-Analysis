'''
通过多个模型以及每个模型的权重，对结果进行预测
陈肖
2016.8.23
'''

import os
import math

path=os.getcwd()

model_file="%s\\model"%(path)
testdata_file="%s\\testdata"%(path)
SVM_predict="%s\\libsvm-3.21\\windows\\svm-predict.exe "%(path)
result="%s\\result"%(path)
log_am="%s\\log\\am.txt"%(path)
tmpresult="%s\\tmpresult"%(path)
log_no_use=">%s\\log\\log.txt"%(path)

num_models=len(os.listdir(model_file))
num_testdata=len(os.listdir(testdata_file))

file=open(log_am,'r')
am_cont=file.read()
am_cont=am_cont.split()
file.close()

for i in range(0,num_testdata):
	print("Now,computer is processing number %d data"%(i))
	testname=testdata_file+"\\testdata%d.txt "%(i)
	sum=0
	for k in range(0,num_models):
		modelname=model_file+"\\model%d "%(k)
		outputname=tmpresult+"\\tmpresult%d.txt "%(k)
		train=SVM_predict+testname+modelname+outputname+log_no_use
		os.system(train)
		file=open(outputname)
		pre_value=file.read();pre_value=pre_value.split();pre_value=float(pre_value[0])
		sum=float(am_cont[k])*pre_value+sum
		file.close()
	if sum>=0:
		result_value=1
	else:
		result_value=-1
	result_txt=result+"\\result%d.txt"%(i)
	file=open(result_txt,'w')
	file.write(str(result_value));file.write('\n')
	file.close()
#计算正确率和混淆矩阵
confusematrix={"r1p1":0,"r1p-1":0,"r-1p1":0,"r-1p-1":0}
sum_right=0
for i in range(0,num_testdata):
    data_real=testdata_file+"\\testdata%d.txt "%(i)
    data_predict=result+"\\result%d.txt "%(i) 
    file_reality=open(data_real)
    file_predict=open(data_predict)
    real=file_reality.read();real=real.split()
    real=real[0]
    predict=file_predict.read();predict=predict.split()
    predict=predict[0]
    if real=="1" and predict=="1":
        confusematrix["r1p1"]+=1
        sum_right+=1
    elif real=="1" and predict=="-1":
        confusematrix["r1p-1"]+=1
    elif real=="-1" and predict=="1":
        confusematrix["r-1p1"]+=1
    elif real=="-1" and predict=="-1":
        confusematrix["r-1p-1"]+=1
        sum_right+=1
    file_predict.close()
    file_reality.close()   
print ("The result is:\n")
print(confusematrix,"\n")
print((sum_right/num_testdata)*100,"%")


