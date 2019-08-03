#!/usr/bin/env python3

import os 
import sys
import time
import argparse
 
def read_login_rec(filelist):
    '''
    Opens file containing the raw data, 
    Checks for the presence of 15 elements in list, 
    Adds entries from file to variable login_recs.
    '''
    login_recs = []
    f = open(filelist,'r')
    for i in f.readlines():
        if len(i.split()) == 15:
            login_recs.append(i)
    f.close()
    return login_recs

def make_set (list_record,position):
    '''
    Creates a set for each item in list_record,
    Taking into consideration the position.
    '''
    res_list = set()
    for i in list_record:
        res_list.add(i.split()[position])
    return res_list

def format_record(unformat_record):
    '''
    Formats data coming from the variable unformat_record using time module,
    Feeding day, hour, minutes, seconds, and year into the time module.
    Also checks if any given record login and logout days are different. If
    login and logout days are different, duplicate entry.
    '''
    record_list = []
    for i in unformat_record:
        time1 = time.strptime(' '.join(i.split()[3:8]),"%a %b %d %H:%M:%S %Y")
        time2 = time.strptime(' '.join(i.split()[9:14]),"%a %b %d %H:%M:%S %Y")
        
        different_day1 = time.strftime("%j",time1)
        different_day2 = time.strftime("%j",time2)
 
        if different_day1 == different_day2:
            record_list.append(i.split())
        else:
            next_day = time.mktime(time1)

            eod_time = time.ctime(next_day).split()

            old_day = i.split()

            old_day[9] = eod_time[0]
            old_day[10] = eod_time[1]
            old_day[11] = eod_time[2]
            old_day[12] = '23:59:59'
            old_day[13] = eod_time[4]                           
            record_list.append(old_day)

            while different_day1 != different_day2:
                next_day = next_day + 86400 
                new_day = i.split()
                new_time = time.ctime(next_day).split()
                new_day[3] = new_time[0]
                new_day[4] = new_time[1]
                new_day[5] = new_time[2]
                new_day[6] = '00:00:00'
                new_day[7] = new_time[4]
                different_day1 = time.strftime('%j',time.localtime(next_day))

                if different_day1 != different_day2:
                    new_day[9] = new_time[0]
                    new_day[10] = new_time[1]
                    new_day[11] = new_time[2]
                    new_day[12] = '23:59:59'
                    new_day[13] = new_time[4]
                record_list.append(new_day)
    return record_list

def cal_daily_usage(subject,login_recs):
    '''
    Generates daily usage report by adding all the seconds from all days in 
    '''
    total = 0
    daily_usage = {}
    for time_number in login_recs:
        if subject in time_number:
            time_usage = int(time.mktime(time.strptime(' '.join(time_number[9:14]))) - time.mktime(time.strptime(' '.join(time_number[3:8]))))
            time_format = time.strftime('%Y %m %d',time.strptime(' '.join(time_number[9:14])))
            try:
                daily_usage[time_format] += time_usage
            except:
                daily_usage[time_format] = time_usage
            total += time_usage

    return daily_usage,total
    
def cal_weekly_usage(subject,login_recs):
    '''
    Generates weekly usage report by adding all the seconds from all days in week
    '''
    total = 0
    weekly_usage = {}
    for time_number in login_recs:
        if subject in time_number:
            time_usage = int(time.mktime(time.strptime(' '.join(time_number[9:14]))) - time.mktime(time.strptime(' '.join(time_number[3:8]))))
            time_format = time.strftime('%Y %W',time.strptime(' '.join(time_number[9:14])))
            try:
                weekly_usage[time_format] += time_usage
            except:
                weekly_usage[time_format] = time_usage
            total += time_usage
    return weekly_usage,total

def cal_monthly_usage(subject,login_recs):
    '''
    Generates monthly usage report by adding all the seconds from all days in month
    '''
    total = 0
    monthly_usage = {}
    for time_number in login_recs:
        if subject in time_number:
            time_usage = int(time.mktime(time.strptime(' '.join(time_number[9:14]))) - time.mktime(time.strptime(' '.join(time_number[3:8]))))
            time_format = time.strftime('%Y %m',time.strptime(' '.join(time_number[9:14])))
            try:
                monthly_usage[time_format] += time_usage
            except:
                monthly_usage[time_format] = time_usage
            total += time_usage
    return monthly_usage,total

def formatting(usage_number):
    '''

    '''
    ft = []
    records,total = usage_number
    for key in sorted(records.keys(),reverse=True):
        ft.append("{:<11s}{:>11d}".format(str(key),records[key]))
    ft.append("{:<11s}{:>11d}".format("Total",total))
    return ft

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Usage Report based on the last command",epilog="Copyright 2019 - Bruno Guanabara")
    parser.add_argument("-l", "--list", type=str, choices=['user','host'], help="generate user name or remote host IP from the given files")
    parser.add_argument("-r", "--rhost", help="usage report for the given remote host IP")
    parser.add_argument("-t","--type", type=str, choices=['daily','weekly','monthly'], help="type of report: daily, weekly, and monthly")
    parser.add_argument("-u", "--user", help="usage report for the given user name")
    parser.add_argument("-v","--verbose", action="store_true",help="turn on output verbosity")
    parser.add_argument("files",metavar='F', type=str, nargs='+',help="list of files to be processed")
    args=parser.parse_args()
    if args.verbose:
        print('Files to be processed:',args.files)
        print('Type of args for files',type(args.files))
        if args.user:
            print('usage report for user:',args.user)
        if args.rhost:
            print('usage report for remote host:',args.rhost)
        if args.type:
            print('usage report type:',args.type)

    unformatted_login_rec = []
    for file in args.files:
        unformatted_login_rec.extend(read_login_rec(file))

    if args.rhost:
        subject = args.rhost
    elif args.user:
        subject = args.user


    if args.list:
        if args.list == 'user': #if user is selected, set position to 0.
            position = 0
        else: #if rhost (ip) is selected, set position to 2.
            position = 2
        print(str(args.list).title() + " list for", ' '.join(args.files))
        print(len(str(args.list).title() + " list for "+ ' '.join(args.files))*'=')
        print(*sorted(make_set(unformatted_login_rec,position)),sep = "\n")
    
    elif args.type:
        record_list = format_record(unformatted_login_rec)
        print(args.type.title() + " Usage Report for " + subject)
        print(len(args.type.title() + " Usage Report for " + subject)*'=')
        if args.type == 'daily':
            print("{:<14s}{:>14s}".format("Date","Usage in Seconds"))
            print(*formatting(cal_daily_usage(subject,record_list)),sep = "\n")
        elif args.type == 'weekly':
            print("{:<14s}{:>14s}".format("Week #","Usage in Seconds"))
            print(*formatting(cal_weekly_usage(subject,record_list)),sep = "\n")
        else:
            print("{:<14s}{:>14s}".format("Month","Usage in Seconds"))
            print(*formatting(cal_monthly_usage(subject,record_list)),sep = "\n")
