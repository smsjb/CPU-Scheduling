#!/usr/bin/env python
# coding: utf-8

# In[17]:


import copy
    
def BubbleSort(lst):
    sorting=copy.deepcopy(lst)

    n = len( sorting )
    for i in range( 0, n - 1 ):
        for j in range( i + 1, n ):
            if sorting[i]['at'] > sorting[j]['at']:
                sorting[i], sorting[j] =sorting[j], sorting[i]
            elif sorting[i]['at'] == sorting[j]['at'] and sorting[i]['pid'] > sorting[j]['pid']:
                sorting[i], sorting[j] =sorting[j], sorting[i]
    return sorting

def readfile():
    print('filename: ', end='')
    path = input()
    obj=[]
    op=0
    ts=0
    num=0
    output=[]
    with open(path) as f:
        for line in f.readlines():
            obj.append(line)
    num=0
    for i in obj:
        i=i.split()
        if num==0:
            op=int(i[0])
            ts=int(i[1])
        elif num>1:
            output.append({'pid':int(i[0]), 'cpu':int(i[1]), 'at':int(i[2]), 'p':int(i[3]), 'done':'F'})
        num=num+1
    f.close()
    return op, ts, output, path

def FCFS(dlist):
    x=copy.deepcopy(dlist)
    gchart=[]
    sort=BubbleSort(x)
    t=0
    fcfs=[]
    for i in sort:
        if t<i['at']:
            for j in range(t, i['at']):
                gchart.append(-1)
            t=i['at']
        fcfs.append({'pid':i['pid'], 'start':t, 'end':t+i['cpu']})
        for j in range(i['cpu']):
            gchart.append(i['pid'])
        t=t+i['cpu']

    return fcfs, gchart

def CheckZ(lst):
    num=0
    for i in lst:
        if i['cpu']!=0:
            num=num+1
    if num>0:
        return False
    else:
        return True

def Loc(lst, pid):
    num=0
    for i in lst:
        if i['pid']==pid:
            return num
        num=num+1
    return -1

def RR(dlist, ts):
    x=copy.deepcopy(dlist)
    sort=BubbleSort(x)
    rr=[]
    t=0
    queue=[]
    usepid=-1
    start_arr=[]
    tmp=-1
    gchart=[]
    while CheckZ(sort)==False: #check all done
        # add process to queue
        for i in sort:
            if t>=i['at'] and i['cpu']!=0 and Loc(queue,  i['pid'])==-1 and usepid!=i['pid']:
                queue.append({'pid':i['pid']})
        
        if len(queue)==0 and usepid!=-1 and sort[Loc(sort,  usepid)]['cpu']!=0:
            queue.append({'pid':usepid})

        if len(queue)!=0:
            usepid=queue[0]['pid']
            if Loc(start_arr,  usepid)==-1:
                rr.append({'pid':usepid, 'start':t, 'end':0}) #紀錄初始佔cpu時間
                start_arr.append({'pid':usepid, 'start':t})
            sortip=Loc(sort,  usepid)
            if sortip!=-1:
                tmp=ts
                if ts>sort[sortip]['cpu']:
                    tmp= sort[sortip]['cpu']

                sort[sortip]['cpu']-=tmp
                for i in range(tmp):
                    gchart.append(usepid)
                if sort[sortip]['cpu']==0:
                    rr[Loc(start_arr,  usepid)]['end']=t+tmp
            queue.remove(queue[0])
        elif usepid==-1 or (usepid!=-1 and sort[Loc(sort,  usepid)]['cpu']==0): gchart.append(-1)
        if tmp!=-1: t+=tmp
        else: t+=1
    return rr,gchart

def PSJFsort(lst):
    n = len( lst )
    for i in range( 0, n - 1 ):
        for j in range( i + 1, n ):
            if lst[i]['cpu'] > lst[j]['cpu']:
                lst[i], lst[j] =lst[j], lst[i]
            elif lst[i]['cpu'] == lst[j]['cpu'] and (lst[i]['done']!='F' and lst[j]['done']=='F'):
                lst[i], lst[j] =lst[j], lst[i]
            elif lst[i]['cpu'] == lst[j]['cpu'] and((lst[i]['done']=='F' and lst[j]['done']=='F')or(lst[i]['done']!='F' and lst[j]['done']!='F')) and (lst[i]['at'] > lst[j]['at']):
                lst[i], lst[j] =lst[j], lst[i]
            elif lst[i]['cpu']== lst[j]['cpu'] and lst[i]['at'] ==lst[j]['at'] and lst[i]['pid'] > lst[j]['pid']:
                lst[i], lst[j] =lst[j], lst[i]
    return lst

def PSJF(dlist):
    psjf=[]
    queue=[]
    sort=[]
    x=copy.deepcopy(dlist)
    sort=PPsort(x)

    t=0
    usepid=-1
    start_arr=[]
    gchart=[]
    while CheckZ(sort)==False:
        for i in sort:
            if t>=i['at'] and i['cpu']!=0 and Loc(queue,  i['pid'])==-1 and usepid!=i['pid']:
                queue.append(i)
        
        if len(queue)==0 and usepid!=-1 and sort[Loc(sort,  usepid)]['cpu']!=0:
            queue.append(sort[Loc(sort,  usepid)])

        if len(queue)!=0:
            PSJFsort(queue)
            if usepid!=-1 and sort[Loc(sort,  usepid)]['cpu']!=0:
                sortip=Loc(sort,  usepid)
                tmp=[sort[sortip],queue[0]]
                PSJFsort(tmp)
                usepid=tmp[0]['pid']
            else: usepid=queue[0]['pid']

            #print(usepid)
            #print(tmp)

            if Loc(start_arr,  usepid)==-1:
                psjf.append({'pid':usepid, 'start':t, 'end':0}) #紀錄初始佔cpu時間
                start_arr.append({'pid':usepid, 'start':t})
            sortip=Loc(sort,  usepid)
            if sortip!=-1:

                sort[sortip]['cpu']-=1
                sort[sortip]['done']='T'
                #sort[sortip]['times']+=tmp
                #print('tmp: ',tmp)
                gchart.append(usepid)
                if sort[sortip]['cpu']==0:
                    psjf[Loc(start_arr,  usepid)]['end']=t+1
            queue.remove(queue[0])
        elif usepid==-1 or (usepid!=-1 and sort[Loc(sort,  usepid)]['cpu']==0):
            gchart.append(-1)
        t+=1
    return psjf, gchart


    
def NSJFsort(unsrt):
    lst=[]
    for i in unsrt:
        lst.append(i)
    n = len( lst )
    for i in range( 0, n - 1 ):
        for j in range( i + 1, n ):
            if lst[i]['cpu'] > lst[j]['cpu']:
                lst[i], lst[j] =lst[j], lst[i]
            elif lst[i]['cpu'] == lst[j]['cpu'] and (lst[i]['at'] > lst[j]['at']):
                lst[i], lst[j] =lst[j], lst[i]
            elif lst[i]['cpu']== lst[j]['cpu'] and lst[i]['at'] ==lst[j]['at'] and lst[i]['pid'] > lst[j]['pid']:
                lst[i], lst[j] =lst[j], lst[i]
    return lst

def NSJF(dlist):
    x=copy.deepcopy(dlist)
    sort = NSJFsort(x)
    t=0
    nsjf=[]
    queue=[]
    gchart=[]
    while CheckZ(sort)==False:
        ip=0
        for i in sort:
            if t>=i['at'] and i['cpu']!=0 and Loc(queue,  i['pid'])==-1:
                 queue.append({'ip':ip, 'pid':i['pid'], 'cpu':i['cpu'],'at':i['at']})
            ip=ip+1

        if len(queue)!=0:
            queue=NSJFsort(queue)
            nsjf.append({'pid':queue[0]['pid'],'start':t, 'end':t+queue[0]['cpu']})
            sort[queue[0]['ip']]['cpu']=0
            t=t+queue[0]['cpu']
            for i in range(queue[0]['cpu']):
                gchart.append(queue[0]['pid'])
            queue.remove(queue[0])
        else:
            gchart.append(-1)
            t=t+1
   
    return nsjf, gchart

def PPsort(lst):
    n = len( lst )
    for i in range( 0, n - 1 ):
        for j in range( i + 1, n ):
            if lst[i]['p'] > lst[j]['p']:
                lst[i], lst[j] =lst[j], lst[i]
            elif lst[i]['p'] == lst[j]['p'] and (lst[i]['done']!='F' and lst[j]['done']=='F'):
                lst[i], lst[j] =lst[j], lst[i]
            elif lst[i]['p'] == lst[j]['p'] and((lst[i]['done']=='F' and lst[j]['done']=='F')or(lst[i]['done']!='F' and lst[j]['done']!='F')) and (lst[i]['at'] > lst[j]['at']):
                lst[i], lst[j] =lst[j], lst[i]
            elif lst[i]['p']== lst[j]['p'] and lst[i]['at'] ==lst[j]['at'] and lst[i]['pid'] > lst[j]['pid']:
                lst[i], lst[j] =lst[j], lst[i]
    return lst

def PP(dlist):
    sort=[]
    x=copy.deepcopy(dlist)
    sort=PPsort(x)

    pp=[]
    t=0
    queue=[]
    usepid=-1
    start_arr=[]
    gchart=[]
    while CheckZ(sort)==False:
        for i in sort:
            if t>=i['at'] and i['cpu']!=0 and Loc(queue,  i['pid'])==-1 and usepid!=i['pid']:
                queue.append(i)
        
        if len(queue)==0 and usepid!=-1 and sort[Loc(sort,  usepid)]['cpu']!=0:
            queue.append(sort[Loc(sort,  usepid)])

        if len(queue)!=0:
            PPsort(queue)
            #print(queue)
 
            if usepid!=-1 and sort[Loc(sort,  usepid)]['cpu']!=0:
                sortip=Loc(sort,  usepid)
                if sort[sortip]['p']>queue[0]['p']:usepid=queue[0]['pid']
            else: usepid=queue[0]['pid']

            #print('af: ',usepid, 'at: ',sort[Loc(sort,  usepid)]['at'], 'now: ',t)

            #print(usepid)
            #print(tmp)
            gchart.append(usepid)
            if Loc(start_arr,  usepid)==-1:
                pp.append({'pid':usepid, 'start':t, 'end':0}) #紀錄初始佔cpu時間
                start_arr.append({'pid':usepid, 'start':t})
            sortip=Loc(sort,  usepid)
            if sortip!=-1:

                sort[sortip]['cpu']-=1
                sort[sortip]['done']='T'
                #sort[sortip]['times']+=tmp
                #print('tmp: ',tmp)
                if sort[sortip]['cpu']==0:
                    pp[Loc(start_arr,  usepid)]['end']=t+1
            queue.remove(queue[0])
        elif usepid==-1 or (usepid!=-1 and sort[Loc(sort,  usepid)]['cpu']==0): gchart.append(-1)
        t+=1

    return pp, gchart

def Ttime(chart):
    output=[]
    lst=[]
    for i in chart:
        if Loc(output, i['pid'])==-1:
            output.append(i)
        else:
            output[Loc(output, i['pid'])]['end']=i['end']
    for j in output:
        lst.append({'pid':j['pid'], 't':j['end']-dlist[Loc(dlist, j['pid'])]['at']})
    n = len(lst)
    for i in range( 0, n - 1 ):
        for j in range( i + 1, n ):
            if lst[i]['pid'] > lst[j]['pid']:
                lst[i], lst[j] =lst[j], lst[i]
    return lst

def Convrt(gchart):
    dic={10:'A', 11:'B', 12:'C', 13:'D', 14:'E', 15:'F', 16:'G', 17:'H', 18:'I', 19:'J', 20:'K', 21:'L', 22:'M', 23:'N', 24:'O', 25:'P',
         26:'Q', 27:'R', 28:'S', 29:'T', 30:'U', 31:'V', 32:'W', 33:'X', 34:'Y', 35:'Z'}
    lst=[]
    t=0
    i=0
    for i in gchart:
        if i>=10:
            lst.append(dic[i])
        elif i==-1: lst.append('-')
        else: lst.append(i)
    return lst

def Out(method, chart, dlist, gchart):
    info=Ttime(chart)
    Gplot(method,gchart)
    print('\n===============\n\nWaiting Time\nID      ',method,'\n===============\n')
    file.writelines('\n==============='+'\n\nWaiting Time\n'+ 'ID      '+method+'\n'+'===============\n')
    for i in info:
        print(i['pid'], '\t', i['t']- cpus[Loc(dlist, i['pid'])]['cpu'])
        
    file.writelines(''.join([str(x['pid'])+'\t'+str(x['t']- cpus[Loc(dlist,x['pid'])]['cpu'])+'\n' for x in info]))
    print('\n===============\n\nTurnaround Time\nID      ',method,'\n===============\n')
    file.writelines('\n==============='+'\n\nTurnaround Time\n'+ 'ID      '+method+'\n'+'===============\n')
    for i in info:
        print(i['pid'], '\t', i['t'])
    file.writelines(''.join([str(x['pid'])+'\t'+str(x['t'])+'\n' for x in info]))
    print('===============')
    file.writelines('===============')
def Gplot(method,gchart):
    print('==    ',method,'==')
    file.writelines('==    '+str(method)+'==\n')
    plot=Convrt(gchart)
    for i in plot:
        print(i,end='')
    file.writelines(''.join([str(x)  for x in plot]))

if __name__ == '__main__':
    op=0
    ts=0
    dlist=[]
    op, ts, dlist, fname=readfile()
    cpus=[]
    gchart=[]
    for i in dlist:
        cpus.append({'pid':i['pid'], 'cpu':i['cpu']})
    t=[]
    file=open('output_'+fname,'w')
    if op==1:
        chart, gchart=FCFS(dlist)
        Out('FCFS', chart,  cpus, gchart)
    elif op==2:
        chart, gchart=RR(dlist, ts)
        Out('RR', chart,  cpus, gchart)
        #Gplot('RR', chart)
    elif op==3:
        chart, gchart=PSJF(dlist)
        Out('PSJF', chart,  cpus, gchart)
    elif op==4:
        chart, gchart=NSJF(dlist)
        Out('Non-PSJF', chart,  cpus, gchart)
    elif op==5:
        chart, gchart=PP(dlist)
        Out('Priority', chart,  cpus, gchart)
    elif op==6:
        chartlst=[]
        one, gchart=FCFS(dlist)
        Gplot('FCFS', gchart)
        print('\n')
        file.writelines('\n')
        two, gchart=RR(dlist, ts)
        Gplot('RR', gchart)
        print('\n')
        file.writelines('\n')
        three, gchart=PSJF(dlist)
        Gplot('PSJF', gchart)
        print('\n')
        file.writelines('\n')
        four, gchart=NSJF(dlist)
        Gplot('Non-PSJF', gchart)
        print('\n')
        file.writelines('\n')
        five, gchart=PP(dlist)
        Gplot('Priority', gchart)

        print('\n===========================================================\n\nWaiting Time\nID      ','FCFS    RR      PSJF    NPSJF   Priority','\n===========================================================\n')  
        file.writelines('\n==========================================================='+'\n\nWaiting Time\n'+ 'ID      '+' FCFS    RR      PSJF    NPSJF   Priority'+'\n'+'===========================================================\n')
        ip=0
        f=Ttime(one)
        r=Ttime(two)
        p=Ttime(three)
        n=Ttime(four)
        pp=Ttime(five)

        ip=0    

        while ip < len(cpus):
            tmp=str(f[ip]['pid'])+'\t'+str(f[ip]['t']- cpus[Loc(cpus, f[ip]['pid'])]['cpu'])+'\t'+str(r[ip]['t']- cpus[Loc(cpus, r[ip]['pid'])]['cpu'])
            tmp=tmp+'\t'+str(p[ip]['t']- cpus[Loc(cpus, p[ip]['pid'])]['cpu'])+'\t'+str(n[ip]['t']- cpus[Loc(cpus, n[ip]['pid'])]['cpu'])
            tmp=tmp+'\t'+str(pp[ip]['t']- cpus[Loc(cpus, pp[ip]['pid'])]['cpu'])+'\n'
            file.writelines(tmp)
            print(tmp)
            ip=ip+1        
        print('\n===========================================================\n\nTurnaround Time\nID      ',' FCFS    RR      PSJF    NPSJF   Priority','\n===========================================================\n')
        file.writelines('\n==========================================================='+'\n\nTurnaround Time\n'+ 'ID      '+' FCFS    RR      PSJF    NPSJF   Priority'+'\n'+'===========================================================\n')

        ip=0
        while ip < len(cpus):
            tmp=str(f[ip]['pid'])+'\t'+str(f[ip]['t'])+'\t'+str(r[ip]['t'])+'\t'+str(p[ip]['t'])+'\t'+str(n[ip]['t'])+'\t'+str(pp[ip]['t'])+'\n'
            file.writelines(tmp)
            print(tmp)
            ip=ip+1

        print('===========================================================')
        file.writelines('===========================================================')

        

    file.close()





