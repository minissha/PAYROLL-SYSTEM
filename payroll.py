import mysql.connector as msq
import datetime
from tabulate import tabulate

db=input("Enter name of your database: ")
print()
mydb=msq.connect(host='localhost',user='root',passwd='12345')
mycursor=mydb.cursor()

sql="CREATE DATABASE if not exists %s"% (db,)
mycursor.execute(sql)
print("Database created successfully..")
print()

mycursor=mydb.cursor()
mycursor.execute("use "+db)
TableName=input("Enter the name of the table to be created: ")
print()

query="create table if not exists " + TableName+ "\
(Empno int primary key,\
Name varchar(15) not null,\
job varchar(15),\
BasicSalary int,\
DA float,\
HRA float,\
GrossSalary float,\
Tax float,\
Netsalary float)"
print("Table " +TableName+ " created successfully...")
mycursor.execute(query)

while True:
    print('\n\n\n')
    print("*"*95)
    print('\t\t\t\t\t\t\t\t\tMAIN MENU')
    print("*"*95)
    print('\t\t\t\t1. Adding employee records')
    print('\t\t\t\t2. For Displaying Record of All the Employees')
    print('\t\t\t\t3. For Displaying Record of a particular Employee')
    print('\t\t\t\t4. For deleting Records of all the Employees')
    print('\t\t\t\t5. For deleting a Record of a particular employee')
    print('\t\t\t\t6. For modification in a record')
    print('\t\t\t\t7. For displaying payroll')
    print('\t\t\t\t8. For displaying Salary Slip for all the Employees')
    print('\t\t\t\t9. For displaying Salary slip for a particular Employee')
    print('\t\t\t\t10.For exit')
    choice=int(input('Enter your choice: '))
    print()
    if choice==1:
        try:
            print('Enter Employee information...')
            mempno=int(input('Enter employee no: '))
            mname=input('Enter employee name: ')
            mjob=input('Enter employee job: ')
            mbasic=float(input('Enter basic salary: '))
            if mjob.upper()=='OFFICER':
                mda=mbasic*0.5
                mhra=mbasic*0.35
                mtax=mbasic*0.2
            elif mjob.upper()=='MANAGER':
                mda=mbasic*0.45
                mhra=mbasic*0.30
                mtax=mbasic*0.15
            else:
                mda=mbasic*0.40
                mhra=mbasic*0.25
                mtax=mbasic*0.1
            mgross=mbasic+mda+mhra
            mnet=mgross-mtax
            rec=(mempno,mname,mjob,mbasic,mda,mhra,mgross,mtax,mnet)
            query="insert into "+TableName+" values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            mycursor.execute(query,rec)
            
            mydb.commit()
            print("record added successfully...")
        except Exception as e:
            print("Something went wrong",e)
        
            
    elif choice==2:
        try:
            query='select * from '+TableName
            mycursor.execute(query)
            myrecords=mycursor.fetchall()
            print(tabulate(myrecords,headers=['Empno','Name','Job','Basic salary','DA','HRA','Gross Salary','Tax','Net Salary'])) 
        except:
            print("SOMETHING WENT WRONG")
            
    elif choice==3:
        try:
            en=input('enter employee no to be displayed...')
            query="select * from "+TableName+" where empno=" +en
            mycursor.execute(query)
            myrecord=mycursor.fetchone()
            print("\n\nRecord of Employee No: "+en)
            print(myrecord)
            c=mycursor.rowcount
            if c==-1:
                print("nothing to display")
        except:
            print('SOMETHING WENT WRONG')
            
            
    elif choice==4:
        try:
            ch=input("do you want to delete all the records (Y/N)---")
            if ch.upper()=="Y":
                 mycursor.execute('delete from '+TableName)
                 mydb.commit()
                 print("all the records are deleted...")
        except:
            print("SOMETHING WENT WRONG")
            
            
    elif choice==5:
        try:
            en=input('enter employee no. of the record to be deleted..')
            query='delete from '+TableName+' where empno='+en
            mycursor.execute(query)
            mydb.commit()
            c=mycursor.rowcount
            if c>0:
                print("DELETION DONE")
            else:
                print("employee no ",en," not found ")
        except:
            print("SOMETHING WENT WRONG")
            
    
    elif choice==6:
        try:
            en=input("enter employee number, of whom the record to be modified...")
            query="select * from " +TableName+ " where empno="+en
            mycursor.execute(query)
            myrecord=mycursor.fetchone()
            c=mycursor.rowcount
            if c==-1:
                print('empno '+en+' does not exist')
            else:
                mname=myrecord[1]
                mjob=myrecord[2]
                mbasic=myrecord[3]
                print('empno  :',myrecord[0])
                print('name   :',myrecord[1])
                print('job    :',myrecord[2])
                print('basic  :',myrecord[3])
                print('da     :',myrecord[4])
                print('hra    :',myrecord[5])
                print('gross  :',myrecord[6])
                print('tax    :',myrecord[7])
                print('net    :',myrecord[8])
                print('-----------------------')
                print('Type value below to modify  or just press enter for no change')
                x=input('enter name ')
                if len(x)>0:
                    mname=x
                x=input('enter job ')
                if len(x)>0:
                    myjob=x
                x=input('enter basic salary ')
                if len(x)>0:
                    mbasic=float(x)
                query='update '+TableName+' set name='+"'" +mname+"'"+','+' job='+"'"+mjob+"'"+','+'basicsalary='\
                    +str(mbasic)+' where empno='+en
                print(query)
                mycursor.execute(query)
                mydb.commit()
                print('record modified')
                
        except:
            print('SOMETHING WENT WRONG')
            
            
    elif choice==7:
        try:
            query='select * from '+TableName
            mycursor.execute(query)
            myrecords=mycursor.fetchall()
            print("\n\n\n")
            print(95*'*')
            print('EMPLOYEE PAYROLL'.center(90))
            print(95*'*')
            now=datetime.datetime.now()
            print("current date and time:",end=' ')
            print(now.strftime("%Y-%m-%d %H:%M:%S"))
            print()
            print(95*'-')
            print('%-5s %-15s %-10s %-8s  %-8s  %-8s  %-9s  %-8s  %-9s'\
                  %('Empno','Name','Job','Basic','DA','HRA','Gross','Tax','Net'))
            print(95*'-')
            for rec in myrecords:
                print('%4d %-15s %-10s %8.2f %8.2f  %8.2f  %9.2f  %8.2f  %9.2f'%rec)
            print(95*'-')
        except:
            print("SOMETHING WENT WRONG")
            
            
    elif choice==8:
        try:
            query='select * from '+TableName
            mycursor.execute(query)
            now=datetime.datetime.now()
            print("\n\n\n")
            print('-'*95)
            print('\t\t\t\tSalary slip')
            print('-'*95)
            print("current date and time:",end='')
            print(now.strftime("%Y-%m-%d %H:%M:%S"))
            myrecords=mycursor.fetchall()
            for rec in myrecords:
                print('%4d %-15s %-10s %8.2f %8.2f  %8.2f  %9.2f  %8.2f  %9.2f'%rec)
        except:
            print("SOMETHING WENT WRONG")
            
            
    elif choice==9:
       try:
           en=input("enter employee number whose pay slip you want to retrieve: ")
           query="select * from " +TableName+" where empno=" +en
           mycursor.execute(query)
           now = datetime.datetime.now()
           print("\n\n\n\t\t\t\tSALARY SLIP ")
           print("current date and time:",end=' ')
           print(now.strftime("%Y-%m-%d %H:%M:%S"))
           print(tabulate(mycursor, headers=['Empno','Name','Job','Basic salary','DA','HRA','Gross Salary','Tax','Net Salary'])) 
           
           
       except Exception as e:
           print("SOMETHING WENT WRONG",e)
            
    
    elif choice==10:
        break
    else:
        print("wrong choice...........")

 
