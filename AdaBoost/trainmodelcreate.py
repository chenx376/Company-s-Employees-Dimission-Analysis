'''
实现adaboost:
1.按照权重随机抽样
'''
import os
import xlrd
import xlwt
import random
import math

path=os.getcwd()
raw_datafile="%s\\data_excel\\digital_process.xls"%(path)
weight="%s\\weight\\weight.xls"%(path)
selectdata="%s\\weight\\selectdata.xls"%(path)
train_data="%s\\traindata\\traindata.txt"%(path)
SVM_train="%s\\libsvm-3.21\\windows\\svm-train.exe "%(path)
SVM_predict="%s\\libsvm-3.21\\windows\\svm-predict.exe "%(path)
model_file="%s\\model"%(path)
log_no_use=">%s\\log\\log.txt"%(path)
log_successrate="%s\\log\\log_successrate.txt"%(path)
log_selectdata="%s\\log\\select_log.xls"%(path)
log_am="%s\\log\\am.txt"%(path)
result="%s\\log\\result.txt "%(path)

os.remove(log_am)                      
os.remove(log_successrate)

data=xlrd.open_workbook(raw_datafile)
table=data.sheets()[0]
col=table.ncols
line=table.nrows

book=xlwt.Workbook()       
sheet1=book.add_sheet('weight',cell_overwrite_ok=True)    #计算权重的写入 
book1=xlwt.Workbook()
sheet2=book1.add_sheet('process2',cell_overwrite_ok=True)    #根据权重转化为数量
book2=xlwt.Workbook()       
sheet3=book2.add_sheet('select',cell_overwrite_ok=True)    #记录挑选了哪几个数据

#首次权重
for i in range(0,line):
	sheet1.write(i,0,1.0/line)
book.save(weight)

nround=8    #循环的次数
z=0
while z<nround:
	print("Now, computer is building number %d model"%(z))
	#1.首先按照权重创建可放回的train data
	num=0
	for i in range(0,line):
		weight_data=xlrd.open_workbook(weight)
		table_weight=weight_data.sheets()[0]
		cont=table.row_values(i)
		colcont=table_weight.col_values(0)
		cont_weight=colcont[i]
		cont_weight=round(cont_weight*line*5)
		for j in range(0,cont_weight):
			for k in range(0,col):
				sheet2.write(j+num,k,cont[k])
				if k==col-1:
					sheet2.write(j+num,k+1,i)   
		num=num+cont_weight
	book1.save(selectdata)

	#2.可放回的挑选出n个新的traindata用作训练模型，产生的txt文件存在traindata文件夹中
	new_data=xlrd.open_workbook(selectdata)
	table_newdata=new_data.sheets()[0]
	line_newdata=table_newdata.nrows
	file=open(train_data,'w')
	for i in range(0,line):
		n=random.randint(0,line_newdata-1)    #随机抽样
		sheet3.write(i,0,n)
		cont=table_newdata.row_values(n)
		cont=cont[0:col]
		k=0
		for j in cont:             #产生所需要的格式
			if k>=1:
				file.write(str(k))
				file.write(":")
			k+=1
			file.write(str(j))
			file.write(" ")
			if k==13:
				k=0
		file.write('\n')
	file.close()
	book2.save(log_selectdata)

	#3.根据权重不同的数据集重新产生新的模型
	exe=SVM_train
	data=train_data+" "
	model=model_file+"\\model%d "%(z)
	train=exe+data+model+log_no_use        
	os.system(train)                 #训练模型
	exe=SVM_predict
	train=exe+data+model+result+">>"+log_successrate
	os.system(train)                 #测试模型

	#4进行每个向量的权重修改，并保存每一个的权重
	file=open(result)
	cont=file.read()
	cont=cont.split()
	data_select=xlrd.open_workbook(log_selectdata)
	table_select=data_select.sheets()[0]                    #由于随机选择了数据，这部是打开随机选取的记录
	cont_select=table_select.col_values(0)
	cont_newdata=table_newdata.col_values(0)                #对应之前创造的按权重生成的newdata,看预测是否正确
	em=0
	#计算em
	for i in range(0,line):
		number=cont_select[i];number=int(number)            #看选择了哪一条成员信息
		a=cont_newdata[number];a=int(a)                     #对应到具体在新的扩大版的data中是哪一条信息
		b=cont[i];b=int(b)                                  #结果
		if a!=b:
			cont_tmp=table_newdata.col_values(col)                 #扩大版的data最后一列是对应之前的数据的标号
			cont_tmp=cont_tmp[number];cont_tmp=int(cont_tmp)       #得到最之前对应之前是哪一条信息
			cont_weight=table_weight.col_values(0)
			cont_weight=cont_weight[cont_tmp]                      #在权重的excel库中得到对应的权重
			wi=cont_weight
			em=em+wi*1
	if em>=0.5 or em==0:                                             #如果错误率大于0.5重新构建模型,或者为0
		continue
	#保存每次的系数am
	am=0.5*math.log((1-em)/em,math.e)
	file_tmp=open(log_am,'a')
	file_tmp.write(str(am))
	file_tmp.write('\n')
	file_tmp.close()

	#计算zm
	zm=0
	for i in range(0,line):
		number=cont_select[i];number=int(number)
		a=cont_newdata[number];a=int(a)
		b=cont[i];b=int(b)
		tmp=a*b*(-am)
		tmp=math.exp(tmp)
		cont_tmp=table_newdata.col_values(col)
		cont_tmp=cont_tmp[number];cont_tmp=int(cont_tmp)
		cont_weight=table_weight.col_values(0)
		cont_weight=cont_weight[cont_tmp]
		wi=cont_weight
		zm=zm+wi*tmp
	#更新新的权重
	for i in range(0,line):
		number=cont_select[i];number=int(number)
		a=cont_newdata[number];a=int(a)
		b=cont[i];b=int(b)
		tmp=a*b*(-am)
		tmp=math.exp(tmp)
		cont_tmp=table_newdata.col_values(col)
		cont_tmp=cont_tmp[number];cont_tmp=int(cont_tmp)
		cont_weight=table_weight.col_values(0)
		cont_weight=cont_weight[cont_tmp]
		wi=cont_weight
		wi_new=(wi/zm)*tmp
		sheet1.write(cont_tmp,0,wi_new)           #对应位置写入更新后的权重
	book.save(weight)
	file.close()
	z+=1

