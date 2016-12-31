'''
对原始的文本数据进行转化，将对应数字转化成类别
陈肖
2016.8.10
'''
import xlrd

data=xlrd.open_workbook('C:\\Users\\chenxiao\\Desktop\\南天-工作\\员工离职概率\\process_data.xls')
table=data.sheets()[0]
line=table.nrows
label={};feature1={};feature3={};feature4={};feature6={};feature7={};feature8={}
feature9={};feature10={};feature11={};feature12={}

for i in range(1001,line):
	tmpstr="%s%d%s" %('C:\\Users\\chenxiao\\Desktop\\南天-工作\\员工离职概率\\testdata\\test_data',i-1000,'.txt')
	file=open(tmpstr,'w')
	list_raw=table.row_values(i)
	tmp=[]
	
	#处理类标，是否离职
	cont=list_raw[22];
	if cont in label.keys():
		out=label[cont]
	elif not len(label.values()):
		out=1
		label[cont]=out
	else:
		out=max(label.values())+1
		label[cont]=out
	tmp.append(out)
	
	#处理性别
	cont=list_raw[1]
	if cont in feature1.keys():
		out=feature1[cont]
	elif not len(feature1.values()):
		out=1
		feature1[cont]=out
	else:
		out=max(feature1.values())+1
		feature1[cont]=out
	tmp.append(out)
	
	#处理年龄
	cont=list_raw[2]
	cont=cont[0:4]
	cont=int(cont)
	out=2016-cont
	tmp.append(out)
	
	#处理招聘类型
	cont=list_raw[8]
	if cont in feature3.keys():
		out=feature3[cont]
	elif not len(feature3.values()):
		out=1
		feature3[cont]=out
	else:
		out=max(feature3.values())+1
		feature3[cont]=out
	tmp.append(out)
	
	#处理文凭
	cont=list_raw[11]
	if cont in feature4.keys():
		out=feature4[cont]
	elif not len(feature4.values()):
		out=1
		feature4[cont]=out
	else:
		out=max(feature4.values())+1
		feature4[cont]=out
	tmp.append(out)
	
	#处理在职年龄
	cont=list_raw[18]
	out=cont
	tmp.append(out)
	
	#婚姻状况
	cont=list_raw[19]
	if cont in feature6.keys():
		out=feature6[cont]
	elif not len(feature6.values()):
		out=1
		feature6[cont]=out
	else:
		out=max(feature6.values())+1
		feature6[cont]=out
	tmp.append(out)
	'''
	#健康状况
	cont=list_raw[20]
	if cont in feature7.keys():
		out=feature7[cont]
	elif not len(feature7.values()):
		out=1
		feature7[cont]=out
	else:
		out=max(feature7.values())+1
		feature7[cont]=out
	tmp.append(out)
	'''
	#职称
	cont=list_raw[24]
	if cont in feature8.keys():
		out=feature8[cont]
	elif not len(feature8.values()):
		out=1
		feature8[cont]=out
	else:
		out=max(feature8.values())+1
		feature8[cont]=out
	tmp.append(out)			
	'''
	#岗位分类
	cont=list_raw[23]
	if cont in feature9.keys():
		out=feature9[cont]
	elif not len(feature9.values()):
		out=1
		feature9[cont]=out
	else:
		out=max(feature9.values())+1
		feature9[cont]=out
	tmp.append(out)		
		
	#政治面貌
	cont=list_raw[25]
	if cont in feature12.keys():
		out=feature12[cont]
	elif not len(feature12.values()):
		out=1
		feature12[cont]=out
	else:
		out=max(feature12.values())+1
		feature12[cont]=out
	tmp.append(out)		
	'''			
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
	
