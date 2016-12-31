'''
生成满足格式的testdata
陈肖
2016.8.23
'''

import os
import xlrd
import xlwt
import traindata_create

path=os.getcwd()
testdata_file="%s\\testdata"%(path)
raw_datafile="%s\\process_data.xls"%(path)

data=xlrd.open_workbook(raw_datafile)
table=data.sheets()[0]
col=table.ncols
row=table.nrows

num_begin=traindata_create.train_data_number+1
feature1={};feature3={};feature4={};feature6={};feature7={};feature8={}

for i in range(num_begin,row):
	testname=testdata_file+"\\testdata%d.txt"%(i-num_begin)
	file=open(testname,'w')
	tmp=[]

	row_cont=table.row_values(i)

	#1处理类标
	label={"离职":-1,"正式员工":1}
	cont=row_cont[28]
	out=label[cont]
	tmp.append(out)

	#2.处理性别
	cont=row_cont[1]
	if cont in feature1.keys():
		out=feature1[cont]
	elif not len(feature1.values()):
		out=1
		feature1[cont]=out
	else:
		out=max(feature1.values())+1
		feature1[cont]=out
	tmp.append(out)

	#3.处理年龄
	cont=row_cont[2]
	cont=cont[0:4]
	cont=int(cont)
	out=2016-cont
	tmp.append(out)

	#4.处理招聘类型
	cont=row_cont[8]
	if cont in feature3.keys():
		out=feature3[cont]
	elif not len(feature3.values()):
		out=1
		feature3[cont]=out
	else:
		out=max(feature3.values())+1
		feature3[cont]=out
	tmp.append(out)

	#5.处理文凭
	cont=row_cont[11]
	if cont in feature4.keys():
		out=feature4[cont]
	elif not len(feature4.values()):
		out=1
		feature4[cont]=out
	else:
		out=max(feature4.values())+1
		feature4[cont]=out
	tmp.append(out)

	#6.处理在职年龄
	cont=row_cont[18]
	out=cont
	tmp.append(out)

	#7.婚姻状况
	cont=row_cont[19]
	if cont in feature6.keys():
		out=feature6[cont]
	elif not len(feature6.values()):
		out=1
		feature6[cont]=out
	else:
		out=max(feature6.values())+1
		feature6[cont]=out
	tmp.append(out)

	#8.职称
	cont=row_cont[24]
	if cont in feature8.keys():
		out=feature8[cont]
	elif not len(feature8.values()):
		out=1
		feature8[cont]=out
	else:
		out=max(feature8.values())+1
		feature8[cont]=out
	tmp.append(out)	

	#输出部分
	k=0
	for j in tmp:
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




