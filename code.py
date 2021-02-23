#!/usr/bin/env python
# coding: utf-8

# In[121]:


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
            output.append({'pid':int(i[0]), 'cpu':int(i[1]), 'at':int(i[2]), 'p':int(i[3])})
        num=num+1
    f.close()
    return op, ts, output, path

def FCFS(dlist):
    x=copy.deepcopy(dlist)
    sort=BubbleSort(x)
    t=sort[0]['at']
    fcfs=[]
    for i in sort:
        fcfs.append({'pid':i['pid'], 'start':t, 'end':t+i['cpu']})
        t=t+i['cpu']
    return fcfs

def CheckZ(lst):
    num=0
    for i in lst:
        if i['cpu']!=0:
            num=num+1
    if num>0:
        return False
    else:
        return True

def RR(dlist, ts):
    x=copy.deepcopy(dlist)
    sort=BubbleSort(x)
    rr=[]
    t=0
    queue=[]
    useip=-1
    while CheckZ(sort)==False:
        ip=0
        for i in sort:
            if t>=i['at'] and i['cpu']!=0 and Loc(queue,  i['pid'])==-1and useip!=ip:
                queue.append({'ip':ip, 'pid':i['pid']})
            ip=ip+1
        if len(queue)==0 and useip!=-1 and CheckZ(sort)==False:
            queue.append({'ip':useip, 'pid':sort[useip]['pid']})
        if len(queue)!=0:
            if sort[Loc(sort,  queue[0]['pid'])]['cpu'] < ts:
                num=sort[Loc(sort,  queue[0]['pid'])]['cpu']
            else:
                num=ts
            rr.append({'pid':queue[0]['pid'], 'start':t, 'end':t+num})
            useip=queue[0]['ip']
            sort[queue[0]['ip']]['cpu']=sort[queue[0]['ip']]['cpu']-1
            queue.remove(queue[0])
        t=t+1
    return rr

def PSJFsort(lst):
    n = len( lst )
    for i in range( 0, n - 1 ):
        for j in range( i + 1, n ):
            if lst[i]['cpu'] > lst[j]['cpu']:
                lst[i], lst[j] =lst[j], lst[i]
            elif lst[i]['cpu'] == lst[j]['cpu'] and (lst[i]['times']!=0 and lst[j]['times']==0):
                lst[i], lst[j] =lst[j], lst[i]
            elif lst[i]['cpu'] == lst[j]['cpu'] and((lst[i]['times']==0 and lst[j]['times']==0)or(lst[i]['times']!=0 and lst[j]['times']!=0)) and (lst[i]['at'] > lst[j]['at']):
                lst[i], lst[j] =lst[j], lst[i]
            elif lst[i]['cpu']== lst[j]['cpu'] and lst[i]['at'] ==lst[j]['at'] and lst[i]['pid'] > lst[j]['pid']:
                lst[i], lst[j] =lst[j], lst[i]
    return lst

def PSJF(dlist):
    sort=[]
    x=copy.deepcopy(dlist)
    for i in x:
        i['times']=0
        sort.append(i)
    sort=PSJFsort(sort)
    psjf=[]
    t=0
    queue=[]
    qlen=0
    useip=-1
    while CheckZ(sort)==False:
        ip=0
        for i in sort:
            if t>=i['at'] and i['cpu']!=0 and Loc(queue,  i['pid'])==-1 and useip!=ip:
                queue.append({'ip':ip, 'pid':i['pid'], 'cpu':i['cpu'], 'times':i['times'], 'at':i['at']})
            ip=ip+1
        if len(queue)!=0:
            if qlen!=len(queue) or (useip!=-1 and sort[useip]['cpu']==0):
                queue=PSJFsort(queue)
                qlen=len(queue)
            useip=queue[0]['ip']
            psjf.append({'pid':queue[0]['pid'],'start':t, 'end':t+1})
            sort[queue[0]['ip']]['times']=sort[queue[0]['ip']]['times']+1
            sort[queue[0]['ip']]['cpu']=sort[queue[0]['ip']]['cpu']-1
            if queue[0]['cpu']==1:
                queue.remove(queue[0])
            else:
                queue[0]['cpu']=queue[0]['cpu']-1

        t=t+1
    return psjf

def Loc(lst, pid):
    num=0
    for i in lst:
        if i['pid']==pid:
            return num
        num=num+1
    return -1
    
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
            queue.remove(queue[0])
        else:
            t=t+1
   
    return nsjf

def PPsort(lst):
    n = len( lst )
    for i in range( 0, n - 1 ):
        for j in range( i + 1, n ):
            if lst[i]['p'] > lst[j]['p']:
                lst[i], lst[j] =lst[j], lst[i]
            elif lst[i]['p'] == lst[j]['p'] and (lst[i]['times']!=0 and lst[j]['times']==0):
                lst[i], lst[j] =lst[j], lst[i]
            elif lst[i]['p'] == lst[j]['p'] and((lst[i]['times']==0 and lst[j]['times']==0)or(lst[i]['times']!=0 and lst[j]['times']!=0)) and (lst[i]['at'] > lst[j]['at']):
                lst[i], lst[j] =lst[j], lst[i]
            elif lst[i]['p']== lst[j]['p'] and lst[i]['at'] ==lst[j]['at'] and lst[i]['pid'] > lst[j]['pid']:
                lst[i], lst[j] =lst[j], lst[i]
    return lst

def PP(dlist):
    sort=[]
    x=copy.deepcopy(dlist)
    for i in x:
        i['times']=0
        sort.append(i)
    sort=PPsort(sort)
    pp=[]
    t=0
    queue=[]
    qlen=0
    useip=-1
    incpu={}
    while CheckZ(sort)==False:
        ip=0
        for i in sort:
            if t>=i['at'] and i['cpu']!=0 and Loc(queue,  i['pid'])==-1 and useip!=ip:
                queue.append({'ip':ip, 'pid':i['pid'], 'cpu':i['cpu'], 'times':i['times'], 'at':i['at'], 'p':i['p']})
            ip=ip+1
        if len(queue)!=0:
            if qlen!=len(queue) or (useip!=-1 and sort[useip]['cpu']==0): #come or done
                queue=PPsort(queue)
                if qlen!=len(queue) and sort[useip]['cpu']!=0:
                    if incpu!={} and queue[0]['p']< incpu['p']:
                        tmp=incpu
                        incpu=queue[0]
                        queue[0]=incpu
                qlen=len(queue)
        
            if incpu=={}:
                incpu=queue[0]
                queue.remove(queue[0])
                qlen=0

            useip=incpu['ip']
            pp.append({'pid':incpu['pid'],'start':t, 'end':t+1})
            sort[incpu['ip']]['times']=sort[incpu['ip']]['times']+1
            sort[incpu['ip']]['cpu']=sort[incpu['ip']]['cpu']-1
            incpu['cpu']=incpu['cpu']-1
            incpu['times']= incpu['times']+1
            
            if incpu['cpu']==0:
                if Loc(queue,  incpu['pid'])!=-1:
                    queue.remove(queue[Loc(queue,  incpu['pid'])])
                incpu={}
        else:
            if incpu!={} and incpu['cpu']!=0 and  CheckZ(sort)==False:
                pp.append({'pid':incpu['pid'],'start':t, 'end':t+incpu['cpu']})
                sort[incpu['ip']]['cpu']=0
                sort[incpu['ip']]['times']=sort[incpu['ip']]['times']+incpu['cpu']
                incpu['cpu']=0
                incpu['times']= incpu['times']+incpu['cpu']

        t=t+1
    return pp

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

def Convrt(chart):
    dic={10:'A', 11:'B', 12:'C', 13:'D', 14:'E', 15:'F', 16:'G', 17:'H', 18:'I', 19:'J', 20:'K', 21:'L', 22:'M', 23:'N', 24:'O', 25:'P',
         26:'Q', 27:'R', 28:'S', 29:'T', 30:'U', 31:'V', 32:'W', 33:'X', 34:'Y', 35:'Z'}
    lst=[]
    t=0
    i=0
    while i < len(chart):
        if t==chart[i]['start']:
            while t < chart[i]['end']:
                if chart[i]['pid']>=10:
                    lst.append(dic[chart[i]['pid']])
                else:
                    lst.append(str(chart[i]['pid']))
                t=t+1
            i=i+1
        else:
            lst.append('-')
            t=t+1
    return lst

def Out(method, chart, dlist):
    Gplot(method, chart)
    print('\n===============\n\nWaiting Time\nID      ',method,'\n===============\n')
    file.writelines('\n==============='+'\n\nWaiting Time\n'+ 'ID      '+method+'\n'+'===============\n')
    info=Ttime(chart)
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
def Gplot(method, chart):
    print('==    ',method,'==')
    file.writelines('==    '+str(method)+'==\n')
    plot=Convrt(chart)
    for i in plot:
        print(i,end='')
    file.writelines(''.join([str(x)  for x in plot]))

if __name__ == '__main__':
    op=0
    ts=0
    dlist=[]
    op, ts, dlist, fname=readfile()
    cpus=[]
    for i in dlist:
        cpus.append({'pid':i['pid'], 'cpu':i['cpu']})
    t=[]
    file=open('output_'+fname,'w')
    if op==1:
        chart=FCFS(dlist)
        Out('FCFS', chart,  cpus)
    elif op==2:
        chart=RR(dlist, ts)
        Out('RR', chart,  cpus)
    elif op==3:
        chart=PSJF(dlist)
        Out('PSJF', chart,  cpus)
    elif op==4:
        chart=NSJF(dlist)
        Out('NSJF', chart,  cpus)
    elif op==5:
        chart=PP(dlist)
        Out('PP', chart,  cpus)
    elif op==6:
        chartlst=[]
        one=FCFS(dlist)
        two=RR(dlist, ts)
        three=PSJF(dlist)
        four=NSJF(dlist)
        five=PP(dlist)
        Gplot('FCFS', one)
        print('\n')
        file.writelines('\n')
        Gplot('RR', two)
        print('\n')
        file.writelines('\n')
        Gplot('PSJF', three)
        print('\n')
        file.writelines('\n')
        Gplot('NSJF', four)
        print('\n')
        file.writelines('\n')
        Gplot('PP', five)

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
#print(t)
#{'pid':0, 'start':0, 'end':0}
#[{'pid':2, 'cpu':5, 'at':1, 'p':1}, {'pid':5, 'cpu':7, 'at':3, 'p':12}, {'pid':3, 'cpu':4, 'at':2, 'p':4}]


# In[ ]:




