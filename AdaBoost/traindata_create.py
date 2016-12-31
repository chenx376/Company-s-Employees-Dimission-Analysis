'''
生成原始的train_data,无权重，存储在excel中
陈肖
2016.8.19
'''

import os
import xlrd
import xlwt

path=os.getcwd()
raw_datafile="%s\\process_data.xls"%(path)
aftprocess_datafile="%s\\data_excel\\digital_process.xls"%(path)

data=xlrd.open_workbook(raw_datafile)
table=data.sheets()[0]
book=xlwt.Workbook()
sheet=book.add_sheet('process',cell_overwrite_ok=True)
col=table.ncols
line=table.nrows

train_data_number=1000        #用于构建model的数据的数量

#对需要的特征向量进行获取
#1.类标
colcont=table.col_values(28)
label={"离职":-1,"正式员工":1}
for i in range(1,train_data_number+1):
	out=label[colcont[i]]
	sheet.write(i-1,0,out)

#2.处理性别
colcont=table.col_values(1)
feature1={}
for i in range(1,train_data_number+1):
	cont=colcont[i]
	if cont in feature1.keys():
		out=feature1[cont]
	elif not len(feature1.values()):
		out=1
		feature1[cont]=out
	else:
		out=max(feature1.values())+1
		feature1[cont]=out
	sheet.write(i-1,1,out)

#3.处理年龄
colcont=table.col_values(2)
for i in range(1,train_data_number+1):
	cont=colcont[i]
	cont=cont[0:4]
	cont=int(cont)
	out=2016-cont
	sheet.write(i-1,2,out)

#4.招聘渠道
colcont=table.col_values(8)
feature3={}
for i in range(1,train_data_number+1):
	cont=colcont[i]
	if cont in feature3.keys():
		out=feature3[cont]
	elif not len(feature3.values()):
		out=1
		feature3[cont]=out
	else:
		out=max(feature3.values())+1
		feature3[cont]=out
	sheet.write(i-1,3,out)

#5.文凭
colcont=table.col_values(11)
feature4={}
for i in range(1,train_data_number+1):
	cont=colcont[i]
	if cont in feature4.keys():
		out=feature4[cont]
	elif not len(feature4.values()):
		out=1
		feature4[cont]=out
	else:
		out=max(feature4.values())+1
		feature4[cont]=out
	sheet.write(i-1,4,out)

#6.在职时间
colcont=table.col_values(18)
for i in range(1,train_data_number+1):
	cont=colcont[i]
	out=cont
	sheet.write(i-1,5,out)

#7婚姻状况
colcont=table.col_values(19)
feature6={}
for i in range(1,train_data_number+1):
	cont=colcont[i]
	if cont in feature6.keys():
		out=feature6[cont]
	elif not len(feature6.values()):
		out=1
		feature6[cont]=out
	else:
		out=max(feature6.values())+1
		feature6[cont]=out
	sheet.write(i-1,6,out)
#8处理职称
colcont=table.col_values(24)
feature8={}
for i in range(1,train_data_number+1):
	cont=colcont[i]
	if cont in feature8.keys():
		out=feature8[cont]
	elif not len(feature8.values()):
		out=1
		feature8[cont]=out
	else:
		out=max(feature8.values())+1
		feature8[cont]=out
	sheet.write(i-1,7,out)	

book.save(aftprocess_datafile)
