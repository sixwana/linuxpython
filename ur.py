#!/usr/bin/env python3

import os 
import sys
import time
import argparse

def get_login_rec():
    ''' 
    get_login_rec function will read from the command to get the data from the system
	using last command and return the valid data to an unformatted list
	'''
    cmd = "last -Fiw"
    p = os.popen(cmd)  
    result = p.readlines()
    p.close() 
    login_recs = []
    for item in result:
        if len(item.split()) == 15: 
            login_recs.append(item)
    return login_recs
 
def read_login_rec(filelist):
    '''
    read_login_rec accepts one argument which is the log file name that will be given, it reads the file and return
    an unformatted list
    '''
    f = open(filelist,'r')
    login_recs = f.readlines()
    f.close()
    return login_recs

def get_list (list_record,position):
    '''
    get_list function accepts 2 agurments that are formatted list record and the position of the column in the record. If position is 0,
    it will take the first column in the list which is username. 
    All item will be put in the set in order to make every values are unique and not duplicated. After collecting all the values,
    Returning a list of usarnames or ip's
    '''
    res_list = set()
    for item in list_record:
        res_list.add(item.split()[position])
    return res_list

def normalized_rec(unformat_record):
    '''
    normalized_rec accepts one argument which can be parsed from get_login_record function or read_login_rec function. It reads a list of
    unformatted records and convert all the records which have a different day of login and logout time, to the same day. Then return
    a new list of records.
    '''
    record_list = []
    for item in unformat_record:
        time1 = time.strptime(' '.join(item.split()[3:8]),"%a %b %d %H:%M:%S %Y") 
        time2 = time.strptime(' '.join(item.split()[9:14]),"%a %b %d %H:%M:%S %Y")
        
        doy1 = time.strftime("%j",time1) 
        doy2 = time.strftime("%j",time2)
 
        if doy1 == doy2: 
            record_list.append(item.split()) 
        else: 
            novo_day = time.mktime(time1) 
            
            eod_time = time.ctime(novo_day).split() 
            velho_day = item.split()

            velho_day[9] = eod_time[0]
            velho_day[10] = eod_time[1]
            velho_day[11] = eod_time[2]
            velho_day[12] = '23:59:59'
            velho_day[13] = eod_time[4]                           
            record_list.append(velho_day)
            while doy1 != doy2:
                                
                novo_day = novo_day + 86400 
                new_day = item.split()
                new_time = time.ctime(novo_day).split() 
                new_day[3] = new_time[0]
                new_day[4] = new_time[1]
                new_day[5] = new_time[2]
                new_day[6] = '00:00:00'
                new_day[7] = new_time[4]
                doy1 = time.strftime('%j',time.localtime(novo_day))

                if doy1 != doy2: 
                    new_day[9] = new_time[0]
                    new_day[10] = new_time[1]
                    new_day[11] = new_time[2]
                    new_day[12] = '23:59:59'
                    new_day[13] = new_time[4]
                record_list.append(new_day)
    return record_list

def cal_daily_usage(subject,login_recs):
    ''' 
    cal_daily_usage accepts 2 arguments. First argument can be username or ip address. Second argument is the list of formatted records
    which get from function normalized_rec. 
    Will all the records in the same day then sum the all. 
    It will return a dictionary with the key is the date and the value is total time for each date, and the Total time of all the dates
    '''
    total = 0
    daily_usage = {}
    for item in login_recs:
        if subject in item:
            time_usage = int(time.mktime(time.strptime(' '.join(item[9:14]))) - time.mktime(time.strptime(' '.join(item[3:8]))))
            time_format = time.strftime('%Y %m %d',time.strptime(' '.join(item[9:14])))
            try:
                daily_usage[time_format] += time_usage
            except:
                daily_usage[time_format] = time_usage
            total += time_usage

    return daily_usage,total
    
def cal_weekly_usage(subject,login_recs):
    ''' 
    cal_daily_usage accepts 2 arguments. First argument can be username or ip address. Argument in second place is a list of formatted records
    which get from function normalized_rec. It collects all the records in the same weekday of the year then sum all the total time. It will return 
    a dictionary with the key is the date and the value is total time for each date, and the Total time of all the dates
    '''
    total = 0
    weekly_usage = {}
    for item in login_recs:
        if subject in item:
            time_usage = int(time.mktime(time.strptime(' '.join(item[9:14]))) - time.mktime(time.strptime(' '.join(item[3:8]))))
            time_format = time.strftime('%Y %W',time.strptime(' '.join(item[9:14])))
            try:
                weekly_usage[time_format] += time_usage
            except:
                weekly_usage[time_format] = time_usage
            total += time_usage
    return weekly_usage,total

def cal_monthly_usage(subject,login_recs):
    ''' 
    cal_daily_usage accepts 2 arguments. First argument can be username or ip address. Second argument is the list of formatted records
    which get from function normalized_rec. It collects all the records in the same month then sum all the total time. It will return 
    a dictionary with the key is the date and the value is total time for each date, and the Total time of all the dates
    '''
    total = 0
    monthly_usage = {}
    for item in login_recs:
        if subject in item:
            time_usage = int(time.mktime(time.strptime(' '.join(item[9:14]))) - time.mktime(time.strptime(' '.join(item[3:8]))))
            time_format = time.strftime('%Y %m',time.strptime(' '.join(item[9:14])))
            try:
                monthly_usage[time_format] += time_usage
            except:
                monthly_usage[time_format] = time_usage
            total += time_usage
    return monthly_usage,total

def mathMath(calculation):
    '''
    mathMath function accepts one argument which is the result of the daily,weekly,monthly function. It gets dictionary and the total time
    It sorts the key in the dictionary in reverse with text allignment and save it to the list.
    '''
    ft = []
    records,total = calculation
    for key in sorted(records.keys(),reverse=True):
        ft.append("{:<11s}{:>11d}".format(str(key),records[key]))
    ft.append("{:<11s}{:>11d}".format("Total",total))
    return ft

def gen_text(): 
    '''
    gen_text function will generate log file for different command running situations
    '''
    text = []
    text.append("Files to be processed: "+ str(args.filename))
    text.append("Type of args for files "+ str(type(args.filename)))

    if args.list: 
        text.append("processing usage report for the following:")
        text.append("reading login/logout record files "+ str(args.filename))
        text.append("Generating list for "+ str(args.list))
    else:
        if args.user: 
            text.append("usage report for user: "+ str(subject))
        else:
            text.append("usage report for remote host: "+ str(subject))    
        text.append("usage report type: " + str(args.type))
        text.append("processing usage report for the following:")
        text.append("reading login/logout record files "+ str(args.filename))
    return text

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Usage Report based on the last command",
     epilog = "Copyright 2019 - Lucas Costa")

    parser.add_argument('filename',metavar = 'F', nargs='+',help='list of files to be processed')
    parser.add_argument('-l', '--list', choices = ['user','host']
        ,help='generate user name or remote host IP from the given files')
    parser.add_argument('-r', '--rhost', help='usage report for the given remote host IP')
    parser.add_argument('-t', '--type', choices = ['daily','weekly','monthly']
        ,help='type of report: daily, weekly, and monthly')
    parser.add_argument('-u', '--user' ,help='usage report for the given user name')
    parser.add_argument('-v', '--verbose',action="store_true",help='tune on output verbosity')
    args = parser.parse_args()
	
    unformatted_login_rec = []
    if "last" in args.filename:
        unformatted_login_rec.extend(get_login_rec())
    else:
        for file in args.filename:
            unformatted_login_rec.extend(read_login_rec(file))

    if args.rhost:
        subject = args.rhost
    elif args.user:
        subject = args.user

    if args.verbose:
        print(*gen_text(),sep="\n")

    if args.list:
        if args.list == 'user':
            position = 0
        else:
            position = 2
        print(str(args.list).title() + " list for", ' '.join(args.filename))
        print(len(str(args.list).title() + " list for "+ ' '.join(args.filename))*'=')
        print(*sorted(get_list(unformatted_login_rec,position)),sep = "\n")
    
    elif args.type:
        record_list = normalized_rec(unformatted_login_rec)
        print(args.type.title() + " Usage Report for " + subject)
        print(len(args.type.title() + " Usage Report for " + subject)*'=')
        if args.type == 'daily':
            print("{:<14s}{:>14s}".format("Date","Usage in Seconds"))
            print(*mathMath(cal_daily_usage(subject,record_list)),sep = "\n")
        elif args.type == 'weekly':
            print("{:<14s}{:>14s}".format("Week #","Usage in Seconds"))
            print(*mathMath(cal_weekly_usage(subject,record_list)),sep = "\n")
        else:
            print("{:<14s}{:>14s}".format("Month","Usage in Seconds"))
            print(*mathMath(cal_monthly_usage(subject,record_list)),sep = "\n")
