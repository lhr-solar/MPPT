%Code to remove text from Array screen output data
% 9-17-19 G. A. Hallock
clc,clear
space = ' ';
newheader = 'L Temp1 Temp2 InV   OutV   InC  InP';
fileID_1 = fopen('Array2_Test2_9_14_19.txt','r');
fileID_2 = fopen('Array2_Test2_9_14_19.dat','w');
[AA,count] = fscanf(fileID_1,'%c',174); %read header
fprintf(fileID_2,'%s \n',newheader); %write new header

for n=1:4583
fprintf(fileID_2,'%i',n); %write line number
fprintf(fileID_2,'%s',space); %write space
A = fscanf(fileID_1,'%c',22);
Temp1 = fscanf(fileID_1,'%c',4);  %read Temp1
fprintf(fileID_2,'%s',Temp1); %write Temp1
fprintf(fileID_2,'%s',space); %write space
B = fscanf(fileID_1,'%c',30);
Temp2 = fscanf(fileID_1,'%c',5); %read Temp2
fprintf(fileID_2,'%s',Temp2); %write Temp2
fprintf(fileID_2,'%s',space); %write space
C = fscanf(fileID_1,'%c',21);
MPPTin = fscanf(fileID_1,'%c',5);  %read MPPT input voltage
fprintf(fileID_2,'%s',MPPTin); %write MPPT input voltage
fprintf(fileID_2,'%s',space); %write space
D = fscanf(fileID_1,'%c',11);
MPPTout = fscanf(fileID_1,'%c',6);  %read MPPT output voltage
fprintf(fileID_2,'%s',MPPTout); %write MPPT output voltage
fprintf(fileID_2,'%s',space); %write space
E = fscanf(fileID_1,'%c',13);
MPPTinC = fscanf(fileID_1,'%c',4);  %read MPPT input current
fprintf(fileID_2,'%s',MPPTinC); %write MPPT input current
fprintf(fileID_2,'%s',space); %write space
F = fscanf(fileID_1,'%c',10);
MPPTinP = fscanf(fileID_1,'%c',5);  %read MPPT input power
fprintf(fileID_2,'%s \n',MPPTinP); %write MPPT input power
line_in=fgets(fileID_1); %read line
line_in=fgets(fileID_1); %read line
line_in=fgets(fileID_1); %read line
end
fclose(fileID_1);
fclose(fileID_2);