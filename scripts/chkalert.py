#!/usr/bin/python
file_dir="/data/forilen/Kikyou/logs"
print("hello world")
file_object=open(file_dir+"/status.log")
for line in file_object :
	# print(line[1])
	a=line.split("\t")
	for item in a :
		print(item)
	# print(a[0])
