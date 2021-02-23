# CPU Scheduling
作業系統程式作業

# 程式目的
實現FCFS、RR、PSJF、NPSJF、Priority五種中央處理器排成演算法

# 功能
1. FCFS:先到先服務排程，依Arrival Time順序做CPU排程，先到的process先佔有CPU，做到CPU Burst
為0為止才換下一個process，最後輸出甘特圖並依process id 由小到大依序輸出Turnaround Time和Waiting Time。
2. NSJF:不可奪取最短工作優先，依CPU Burst大小決定誰先佔CPU，CPU Burst小優先佔CPU，若有CPU Burst較小的process抵達則此process進佇列第一位，
不可搶佔CPU，Arrival Time未到時間不可進佇列和佔CPU，最後輸出甘特圖並依process id 由小到大依序輸出Turnaround Time和Waiting Time。
3. PSJF:可奪取最短工作優先，依CPU Burst大小決定誰先佔CPU，CPU Burst小優先佔CPU，若有CPU Burst較小的process抵達則此process搶佔CPU
自己則進佇列第一位排隊，Arrival Time未到時間不可進佇列和佔CPU，最後輸出甘特圖並依process id 由小到大依序輸出Turnaround Time和
Waiting Time。
4. RR:知更鳥式循環排程，根據Arrival Time做FCFS，process依設定的time slice決定每次佔有CPU多長時間，時間到則換下一個process佔CPU，
自己則去佇列排隊，Arrival Time未到時間不可進佇列和佔CPU，最後輸出甘特圖並依process id 由小到大依序輸出Turnaround Time和Waiting Time。
5. PP:優先等級排程，根據priority大小決定誰先佔CPU，priority小優先佔CPU，若有優先等級較高的process抵達則此process搶佔CPU，自己則去
佇列排隊，Arrival Time未到時間不可進佇列和佔CPU，最後輸出甘特圖並依process id 由小到大依序輸出Turnaround Time和Waiting Time。
6. All:執行上述所有排程法，並在最後輸出所有排程的甘特圖並依process id 由小到大依序輸出所有排程的Turnaround Time和Waiting Time。

# 輸入格式
第一行第一個integer為method,範圍1~6
第一行第二個integer為time slice,範圍不定
第二擺放的資料為
ID CPU Burst Arrival Time Priority
第三行開始每行依序為
[ProcessID] [CPUBurst] [arrival time] [Priority]
如input.txt

# 輸出格式
第一個區段為Gantt chart
第二個區段顯示各個process id 在各個method(可能數個)的Waiting Time
第三個區段顯示各個process id 在各個method(可能數個)的Turn around Time

# 完成時間
2020/06/12
