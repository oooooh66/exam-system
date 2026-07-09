-- ============================================
-- 在线考试系统 - 300道模拟题库数据
-- 包含: 单选题(80) / 多选题(60) / 判断题(60) / 填空题(50) / 简答题(50)
-- 难度分布: 简单~40% / 中等~40% / 困难~20%
-- ============================================
-- 前提: 已执行 init_data 创建 admin(id=1) teacher(id=2) student(id=3)
-- ============================================

-- ---------- 分类数据 ----------
INSERT INTO question_categories (id, name, description, is_deleted, created_by_id, created_at, updated_at) VALUES
(1, '计算机基础', '计算机组成原理和基础知识', 2, NOW(), NOW()),
(2, '数据结构', '常用数据结构和基础算法', 2, NOW(), NOW()),
(3, '网络技术', '计算机网络和通信协议', 2, NOW(), NOW()),
(4, '操作系统', '操作系统原理与应用', 2, NOW(), NOW()),
(5, '数据库', '数据库原理与SQL语言', 2, NOW(), NOW()),
(6, '软件工程', '软件开发和项目管理', 2, NOW(), NOW()),
(7, '编程基础', '编程语言基础和编码规范', 2, NOW(), NOW());

-- ==================== 单选题(80题) ====================
INSERT INTO questions (question_type, content, options, correct_answer, analysis, category_id, difficulty, default_score, is_deleted, created_by_id, created_at, updated_at) VALUES
('single_choice', '计算机中，1个字节(Byte)由多少个二进制位(bit)组成？', JSON_ARRAY('A. 2位', 'B. 4位', 'C. 8位', 'D. 16位'), 'C', '字节是计算机存储的基本单位，1Byte=8bit，这是计算机体系结构的基础定义。', 1, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '以下哪种进制是计算机内部采用的？', JSON_ARRAY('A. 十进制', 'B. 八进制', 'C. 十六进制', 'D. 二进制'), 'D', '计算机内部采用二进制，因为电子元件的高低电平天然对应0和1两种状态。', 1, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', 'CPU中负责执行算术和逻辑运算的部件是？', JSON_ARRAY('A. 控制器', 'B. 运算器(ALU)', 'C. 寄存器', 'D. 缓存'), 'B', '运算器(ALU)负责算术运算和逻辑运算；控制器负责指令的取指、译码和执行控制。', 1, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '以下哪种存储器读写速度最快？', JSON_ARRAY('A. 硬盘', 'B. 内存(RAM)', 'C. CPU缓存', 'D. U盘'), 'C', '速度排序: CPU缓存 > 内存 > 硬盘。缓存位于CPU内部，延迟最低。', 1, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '计算机的五大基本部件不包括？', JSON_ARRAY('A. 运算器', 'B. 控制器', 'C. 输入设备', 'D. 网络适配器'), 'D', '冯·诺依曼体系结构五大部件: 运算器、控制器、存储器、输入设备、输出设备。', 1, 'easy', 2.00, 0, 1, NOW(), NOW()),

('single_choice', 'ASCII码中，大写字母A的编码值是？', JSON_ARRAY('A. 48', 'B. 65', 'C. 97', 'D. 32'), 'B', 'ASCII中，A=65，a=97，0=48，空格=32。大小写字母差32。', 1, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '1KB等于多少字节？', JSON_ARRAY('A. 100', 'B. 512', 'C. 1000', 'D. 1024'), 'D', '计算机存储单位是2的幂次: 1KB=1024B, 1MB=1024KB, 1GB=1024MB。', 1, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '下列哪种编程语言的执行方式属于解释执行？', JSON_ARRAY('A. C语言', 'B. C++', 'C. Python', 'D. Go'), 'C', 'Python是解释型语言，逐行翻译执行。C/C++/Go是编译型语言，需先编译为机器码。', 1, 'medium', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '在计算机中，负数的补码是其反码加？', JSON_ARRAY('A. 0', 'B. 1', 'C. 2', 'D. -1'), 'B', '反码+1=补码。这是计算机表示有符号整数的标准方式。', 1, 'medium', 2.00, 0, 1, NOW(), NOW()),
('single_choice', 'CPU的主频单位通常是？', JSON_ARRAY('A. MB', 'B. GHz', 'C. Mbps', 'D. mA'), 'B', 'CPU主频以Hz为单位，现代CPU主频通常在2-5GHz(吉赫兹)范围内。', 1, 'easy', 2.00, 0, 1, NOW(), NOW()),

('single_choice', '算法的五个重要特性不包括？', JSON_ARRAY('A. 有穷性', 'B. 确定性', 'C. 可行性', 'D. 美观性'), 'D', '算法五大特性: 有穷性、确定性、可行性、输入、输出。美观性不是算法必需的。', 2, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '下列哪种数据结构是"先进先出"(FIFO)的？', JSON_ARRAY('A. 栈(Stack)', 'B. 队列(Queue)', 'C. 二叉树', 'D. 图'), 'B', '队列是FIFO(First In First Out)，栈是LIFO(Last In First Out)。', 2, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '在平均情况下，快速排序的时间复杂度是？', JSON_ARRAY('A. O(n)', 'B. O(n²)', 'C. O(n log n)', 'D. O(log n)'), 'C', '快速排序平均时间复杂度O(n log n)，最坏O(n²)。它是基于分治思想的经典排序算法。', 2, 'medium', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '二叉搜索树中，左子树所有节点的值应该？', JSON_ARRAY('A. 大于根节点', 'B. 小于根节点', 'C. 等于根节点', 'D. 任意'), 'B', '二叉搜索树性质: 左子树所有值 < 根节点值 < 右子树所有值。', 2, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '链表比数组的优势主要体现在？', JSON_ARRAY('A. 随机访问速度快', 'B. 插入删除效率高', 'C. 内存占用小', 'D. 排序速度快'), 'B', '链表插入删除只需修改指针O(1)，数组需要移动元素O(n)。但数组支持O(1)随机访问。', 2, 'medium', 2.00, 0, 1, NOW(), NOW()),

('single_choice', '哈希表解决冲突的常用方法不包括？', JSON_ARRAY('A. 链地址法', 'B. 开放地址法', 'C. 再哈希法', 'D. 归并法'), 'D', '哈希冲突解决方法包括链地址法、开放地址法、再哈希法等。归并是排序算法。', 2, 'medium', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '深度优先搜索(DFS)通常使用哪种数据结构辅助实现？', JSON_ARRAY('A. 队列', 'B. 栈', 'C. 优先队列', 'D. 链表'), 'B', 'DFS用栈(递归隐式栈或显式栈)，BFS用队列。这是图遍历的基础。', 2, 'medium', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '对于有n个节点的完全二叉树，其高度为？', JSON_ARRAY('A. n', 'B. n/2', 'C. ⌊log₂n⌋+1', 'D. log₁₀n'), 'C', '完全二叉树高度h满足: 2^(h-1) ≤ n < 2^h，解得h=⌊log₂n⌋+1。', 2, 'hard', 3.00, 0, 1, NOW(), NOW()),
('single_choice', '动态规划的核心思想是？', JSON_ARRAY('A. 把大问题分解为小问题并记录子问题结果', 'B. 每次选局部最优解', 'C. 枚举所有可能解', 'D. 随机搜索'), 'A', '动态规划=最优子结构+重叠子问题+记忆化。与贪心的区别是记录子问题结果避免重复计算。', 2, 'medium', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '栈的典型应用场景是？', JSON_ARRAY('A. 任务调度', 'B. 函数调用', 'C. 消息队列', 'D. 进程管理'), 'B', '函数调用时通过系统栈保存返回地址和局部变量，体现了栈的后进先出特性。', 2, 'easy', 2.00, 0, 1, NOW(), NOW()),

('single_choice', 'OSI七层模型中，从下往上第三层是？', JSON_ARRAY('A. 物理层', 'B. 数据链路层', 'C. 网络层', 'D. 传输层'), 'C', 'OSI七层: 物理层→数据链路层→网络层→传输层→会话层→表示层→应用层。网络层是第3层。', 3, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', 'IP地址192.168.1.1属于哪类地址？', JSON_ARRAY('A. A类', 'B. B类', 'C. C类', 'D. D类'), 'C', 'C类私网地址范围: 192.168.0.0~192.168.255.255。A类: 10.x.x.x, B类: 172.16.x.x~172.31.x.x。', 3, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', 'HTTP协议的默认端口号是？', JSON_ARRAY('A. 21', 'B. 25', 'C. 80', 'D. 443'), 'C', '常用端口: HTTP=80, HTTPS=443, FTP=21, SMTP=25, DNS=53, SSH=22。', 3, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', 'TCP协议的主要特点是？', JSON_ARRAY('A. 无连接、不可靠', 'B. 面向连接、可靠', 'C. 面向连接、不可靠', 'D. 无连接、可靠'), 'B', 'TCP: 面向连接、可靠传输(三次握手、确认重传)。UDP: 无连接、不可靠但效率高。', 3, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', 'DNS服务器的作用是？', JSON_ARRAY('A. 分配IP地址', 'B. 域名解析为IP地址', 'C. 加密数据传输', 'D. 过滤网络包'), 'B', 'DNS(Domain Name System)将域名(如www.baidu.com)解析为IP地址，是互联网的电话簿。', 3, 'easy', 2.00, 0, 1, NOW(), NOW()),

('single_choice', 'TCP三次握手中，客户端发送的第一个报文包含什么标志？', JSON_ARRAY('A. ACK', 'B. FIN', 'C. SYN', 'D. RST'), 'C', '三次握手: ①客户端→SYN→服务器 ②服务器→SYN+ACK→客户端 ③客户端→ACK→服务器。', 3, 'medium', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '子网掩码255.255.255.0对应的CIDR表示是？', JSON_ARRAY('A. /8', 'B. /16', 'C. /24', 'D. /32'), 'C', '255.255.255.0=11111111.11111111.11111111.00000000，共24个连续的1→/24。', 3, 'medium', 2.00, 0, 1, NOW(), NOW()),
('single_choice', 'HTTP状态码404表示？', JSON_ARRAY('A. 服务器错误', 'B. 请求成功', 'C. 资源未找到', 'D. 需要认证'), 'C', '常见状态码: 200=成功，404=未找到，500=服务器错误，403=禁止访问，401=需要认证。', 3, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '以下哪个协议用于发送电子邮件？', JSON_ARRAY('A. HTTP', 'B. FTP', 'C. SMTP', 'D. DHCP'), 'C', 'SMTP(Simple Mail Transfer Protocol)用于发送邮件，POP3/IMAP用于接收邮件。', 3, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', 'Cookie和Session的主要区别是？', JSON_ARRAY('A. Cookie存储在服务器，Session存储在客户端', 'B. Cookie存储在客户端，Session存储在服务器', 'C. 两者都存储在客户端', 'D. 两者都存储在服务器'), 'B', 'Cookie存储在浏览器端，容量约4KB。Session存储在服务器端，客户端只保存SessionID。', 3, 'medium', 2.00, 0, 1, NOW(), NOW()),

('single_choice', '操作系统中，进程和线程的关系是？', JSON_ARRAY('A. 进程包含线程', 'B. 线程包含进程', 'C. 两者没有关系', 'D. 进程和线程是一回事'), 'A', '进程是资源分配的基本单位，线程是CPU调度的基本单位。一个进程可包含多个线程。', 4, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '死锁的四个必要条件不包括？', JSON_ARRAY('A. 互斥条件', 'B. 请求保持', 'C. 不可剥夺', 'D. 优先级调度'), 'D', '死锁四条件: 互斥、请求保持、不可剥夺、循环等待。破坏任一条件可预防死锁。', 4, 'medium', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '虚拟内存技术主要解决什么问题？', JSON_ARRAY('A. CPU速度太慢', 'B. 物理内存不足', 'C. 硬盘空间不足', 'D. 网络带宽不足'), 'B', '虚拟内存使用硬盘空间模拟内存，让程序可以使用比物理内存更大的地址空间。', 4, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', 'Linux系统中，查看当前目录的命令是？', JSON_ARRAY('A. dir', 'B. ls', 'C. pwd', 'D. cd'), 'C', 'pwd(Print Working Directory)显示当前工作目录。ls列出文件，cd切换目录。', 4, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '进程状态不包括以下哪个？', JSON_ARRAY('A. 就绪态', 'B. 运行态', 'C. 阻塞态', 'D. 休眠态'), 'D', '进程三态模型: 就绪(Ready)、运行(Running)、阻塞(Blocked)。部分教材增加创建和终止态。', 4, 'medium', 2.00, 0, 1, NOW(), NOW()),

('single_choice', '数据库事务的ACID特性中，I代表？', JSON_ARRAY('A. 完整性(Integrity)', 'B. 隔离性(Isolation)', 'C. 交互性(Interaction)', 'D. 独立性(Independence)'), 'B', 'ACID: Atomicity原子性、Consistency一致性、Isolation隔离性、Durability持久性。', 5, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', 'SQL中，用于从表中查询数据的关键字是？', JSON_ARRAY('A. INSERT', 'B. UPDATE', 'C. SELECT', 'D. DELETE'), 'C', 'CRUD操作: SELECT(查)、INSERT(增)、UPDATE(改)、DELETE(删)。', 5, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '以下哪条SQL语句可以删除表中的所有数据但保留表结构？', JSON_ARRAY('A. DELETE FROM table', 'B. DROP TABLE table', 'C. TRUNCATE TABLE table', 'D. REMOVE FROM table'), 'C', 'TRUNCATE快速删除所有数据且不可回滚；DELETE可回滚；DROP直接删除整个表。', 5, 'medium', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '数据库三大范式中的第一范式(1NF)要求？', JSON_ARRAY('A. 每个列都是不可分割的基本数据项', 'B. 每个表都应该有主键', 'C. 消除传递依赖', 'D. 消除部分依赖'), 'A', '1NF: 列不可再分(原子性)。2NF: 消除部分函数依赖。3NF: 消除传递函数依赖。', 5, 'medium', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '索引的主要作用是？', JSON_ARRAY('A. 节省存储空间', 'B. 加快数据查询速度', 'C. 加密数据', 'D. 减少数据冗余'), 'B', '索引类似书的目录，可以快速定位数据。但会增加写入开销(INSERT/UPDATE/DELETE需维护索引)。', 5, 'easy', 2.00, 0, 1, NOW(), NOW()),

('single_choice', '聚合开发模型中，以下哪个阶段不属于传统瀑布模型？', JSON_ARRAY('A. 需求分析', 'B. 设计', 'C. 持续集成', 'D. 测试'), 'C', '瀑布模型: 需求→设计→编码→测试→维护。持续集成属于敏捷开发实践。', 6, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '单元测试通常由谁来编写？', JSON_ARRAY('A. 测试人员', 'B. 产品经理', 'C. 开发人员', 'D. 客户'), 'C', '单元测试由开发人员编写，用于验证代码中最小的可测试单元(函数/方法)的正确性。', 6, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', 'Git中，将本地修改提交到远程仓库的命令是？', JSON_ARRAY('A. git commit', 'B. git push', 'C. git add', 'D. git pull'), 'B', 'git add(暂存)→git commit(提交到本地)→git push(推送到远程)。git pull=git fetch+git merge。', 6, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '以下哪个是面向对象编程的三个基本特征？', JSON_ARRAY('A. 封装、继承、多态', 'B. 顺序、选择、循环', 'C. 输入、处理、输出', 'D. 编译、链接、运行'), 'A', '面向对象三大特征: 封装(隐藏内部实现)、继承(复用父类代码)、多态(同一接口不同实现)。', 7, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', 'Python中，列表(list)和元组(tuple)的主要区别是？', JSON_ARRAY('A. 列表有序，元组无序', 'B. 列表可变，元组不可变', 'C. 列表只能存数字，元组只能存字符串', 'D. 没有区别'), 'B', '列表是可变序列(支持增删改)，元组是不可变序列(创建后不能修改)。', 7, 'easy', 2.00, 0, 1, NOW(), NOW()),

('single_choice', '多态的具体表现是？', JSON_ARRAY('A. 一个类只能有一个方法', 'B. 同一个方法在不同类中可以有不同的实现', 'C. 子类必须重写父类的所有方法', 'D. 对象不能被转换为其他类型'), 'B', '多态允许多个类实现同一个接口，各以自己的方式实现，调用方无需关心具体类型。', 7, 'medium', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '异常处理中，finally代码块的作用是？', JSON_ARRAY('A. 仅在无异常时执行', 'B. 无论是否发生异常都会执行', 'C. 仅在发生异常时执行', 'D. 直接跳过不执行'), 'B', 'finally块中的代码无论是否捕获异常都会执行，常用于关闭资源(文件、数据库连接等)。', 7, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '正则表达式\\d+ 匹配的是？', JSON_ARRAY('A. 一个字母', 'B. 一个或多个数字', 'C. 一个空格', 'D. 一个或多个字母'), 'B', '\\d匹配一个数字(0-9)，+表示一个或多个。\\d+匹配连续的数字串。', 7, 'medium', 2.00, 0, 1, NOW(), NOW()),
('single_choice', 'TCP/IP协议栈中，IP协议位于哪一层？', JSON_ARRAY('A. 应用层', 'B. 传输层', 'C. 网络层', 'D. 数据链路层'), 'C', 'TCP/IP四层: 应用层→传输层(TCP/UDP)→网络层(IP)→网络接口层。IP是网络层核心。', 3, 'medium', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '在Java中，ArrayList和LinkedList的主要区别在于？', JSON_ARRAY('A. ArrayList有序，LinkedList无序', 'B. ArrayList基于数组，LinkedList基于链表', 'C. ArrayList只能存字符串', 'D. LinkedList只能存数字'), 'B', 'ArrayList基于动态数组，随机访问快。LinkedList基于双向链表，插入删除快。', 7, 'medium', 2.00, 0, 1, NOW(), NOW()),

('single_choice', 'CPU中断的作用是？', JSON_ARRAY('A. 停止计算机运行', 'B. 暂停当前程序转去处理紧急事件', 'C. 格式化硬盘', 'D. 重启操作系统'), 'B', '中断是CPU对外部事件的响应机制，暂停当前任务去处理更高优先级的紧急事件后再返回。', 4, 'medium', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '数据库中，外键的作用是？', JSON_ARRAY('A. 加密数据', 'B. 建立表之间的关联关系', 'C. 提高查询速度', 'D. 自动备份数据'), 'B', '外键引用另一张表的主键，用于维护表之间的引用完整性。例如: 订单表的user_id引用用户表的id。', 5, 'medium', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '哪种排序算法是稳定的？', JSON_ARRAY('A. 快速排序', 'B. 堆排序', 'C. 归并排序', 'D. 选择排序'), 'C', '稳定排序: 值相等的元素在排序后相对位置不变。归并排序、冒泡排序是稳定的；快排、堆排、选择排不稳定。', 2, 'hard', 3.00, 0, 1, NOW(), NOW()),
('single_choice', 'HTTPS相比HTTP增加了什么？', JSON_ARRAY('A. 压缩传输', 'B. SSL/TLS加密', 'C. 缓存机制', 'D. 断点续传'), 'B', 'HTTPS=HTTP+SSL/TLS。通过SSL/TLS协议对数据进行加密传输，保证通信安全。', 3, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', 'GCC编译器将C代码转换为可执行文件的正确顺序是？', JSON_ARRAY('A. 预处理→编译→汇编→链接', 'B. 汇编→预处理→编译→链接', 'C. 编译→链接→预处理→汇编', 'D. 链接→编译→汇编→预处理'), 'A', '编译四阶段: 预处理(.i)→编译(.s)→汇编(.o)→链接(可执行文件)。', 7, 'medium', 2.00, 0, 1, NOW(), NOW()),

('single_choice', '以下哪种IPC方式速度最快？', JSON_ARRAY('A. 管道', 'B. 消息队列', 'C. 共享内存', 'D. 套接字'), 'C', '共享内存直接映射同一块物理内存到不同进程的地址空间，无需数据拷贝，速度最快。', 4, 'hard', 3.00, 0, 1, NOW(), NOW()),
('single_choice', 'KMP字符串匹配算法的核心是？', JSON_ARRAY('A. 暴力匹配', 'B. 利用next数组避免回溯', 'C. 哈希比较', 'D. 分治匹配'), 'B', 'KMP通过预处理模式串生成next(部分匹配表)，在匹配失败时利用已匹配信息减少回溯。', 2, 'hard', 3.00, 0, 1, NOW(), NOW()),
('single_choice', 'MySQL中，MyISAM和InnoDB引擎的主要区别是？', JSON_ARRAY('A. MyISAM支持事务，InnoDB不支持', 'B. MyISAM不支持事务，InnoDB支持事务', 'C. 两者完全一样', 'D. InnoDB不能使用索引'), 'B', 'InnoDB支持事务、行级锁、外键；MyISAM不支持事务、表级锁。InnoDB是MySQL默认引擎。', 5, 'medium', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '设计模式中，单例模式的主要目的是？', JSON_ARRAY('A. 创建一个类只有一个实例', 'B. 创建类的多个实例', 'C. 隐藏类的实现细节', 'D. 动态创建对象'), 'A', '单例模式确保一个类只有一个实例，并提供全局访问点。如数据库连接池、配置管理器。', 7, 'medium', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '二叉树的先序遍历顺序是？', JSON_ARRAY('A. 左→根→右', 'B. 根→左→右', 'C. 左→右→根', 'D. 根→右→左'), 'B', '先序(根左右)、中序(左根右)、后序(左右根)、层序(从上到下逐层)。', 2, 'easy', 2.00, 0, 1, NOW(), NOW()),

('single_choice', 'VLAN的主要作用是？', JSON_ARRAY('A. 提高网速', 'B. 逻辑上划分广播域', 'C. 加密数据', 'D. 分配IP地址'), 'B', 'VLAN(虚拟局域网)在交换机上逻辑划分网络，隔离广播域，提高网络安全性。', 3, 'hard', 3.00, 0, 1, NOW(), NOW()),
('single_choice', '页面置换算法中，OPT(最佳置换算法)属于？', JSON_ARRAY('A. 实际可用算法', 'B. 理论最优算法，实际无法实现', 'C. 最简单的置换算法', 'D. 随机置换算法'), 'B', 'OPT理论上置换最远将来才访问的页面，缺页率最低。但因无法预知未来访问模式而无法实现，只用作比较基准。', 4, 'hard', 3.00, 0, 1, NOW(), NOW()),
('single_choice', 'MVC设计模式中，M代表？', JSON_ARRAY('A. Method(方法)', 'B. Module(模块)', 'C. Model(模型)', 'D. Main(主程序)'), 'C', 'MVC: Model(模型-数据和业务), View(视图-展示), Controller(控制器-逻辑调度)。', 6, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '冒泡排序在最好情况下的时间复杂度是？', JSON_ARRAY('A. O(n)', 'B. O(n²)', 'C. O(n log n)', 'D. O(1)'), 'A', '最好情况(数据已有序): 一趟比较无交换即结束，O(n)。最坏/平均: O(n²)。', 2, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '软件测试中，黑盒测试关注的���？', JSON_ARRAY('A. 代码内部结构', 'B. 程序的输入输出功能', 'C. 内存使用情况', 'D. 代码覆盖率'), 'B', '黑盒测试只关注输入和输出是否符合预期，不需要了解内部代码。白盒测试关注内部逻辑。', 6, 'medium', 2.00, 0, 1, NOW(), NOW()),
('single_choice', 'DDos攻击的主要目的是？', JSON_ARRAY('A. 窃取数据', 'B. 使服务不可用', 'C. 窃听通信', 'D. 篡改数据'), 'B', 'DDoS(分布式拒绝服务攻击)通过大量请求耗尽服务器资源，使正常用户无法访问。', 3, 'medium', 2.00, 0, 1, NOW(), NOW()),

('single_choice', '以下哪种算法不属于机器学习领域？', JSON_ARRAY('A. 决策树', 'B. 快��排序', 'C. 神经网络', 'D. SVM(支持向量机)'), 'B', '快速排序是经典排序算法，属于数据结构与算法基础。决策树、神经网络、SVM都是机器学习算法。', 2, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '线程池的核心优势是？', JSON_ARRAY('A. 可以无限制创建线程', 'B. 重用线程避免频繁创建销毁开销', 'C. 让线程永远不退出', 'D. 线程之间可以不用同步'), 'B', '线程池维护一组工作线程，任务完成后线程不销毁而是等待新任务，减少线程创建/销毁的系统开销。', 4, 'medium', 2.00, 0, 1, NOW(), NOW()),
('single_choice', 'SQL注入攻击的防范措施不包括？', JSON_ARRAY('A. 参数化查询', 'B. ORM框架', 'C. 输入校验', 'D. 使用GET请求'), 'D', 'SQL注入防范: 参数化查询/预编译、ORM框架自动转义、输入校验过滤。GET/POST与SQL注入无关。', 5, 'medium', 2.00, 0, 1, NOW(), NOW()),
('single_choice', 'Git的分支操作中，创建并切换到新分支的命令是？', JSON_ARRAY('A. git branch new', 'B. git checkout -b new', 'C. git switch new', 'D. git merge new'), 'B', 'git checkout -b <分支名> = git branch <分支名> + git checkout <分支名>。新版本也支持git switch -c。', 7, 'easy', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '冯·诺依曼体系结构中，指令和数据如何存储？', JSON_ARRAY('A. 分开存储在不同存储器', 'B. 统一存储在同一个存储器中', 'C. 指令存在硬盘，数据存在内存', 'D. 指令存在CPU，数据存在内存'), 'B', '冯·诺依曼结构的核心是"存储程序"，指令和数据统一放在内存中，按地址访问。', 1, 'medium', 2.00, 0, 1, NOW(), NOW()),

('single_choice', '关于接口(Interface)，描述正确的是？', JSON_ARRAY('A. 接口中可以包含已实现的方法', 'B. 一个类只能实现一个接口', 'C. 接口只定义方法签名，不包含实现', 'D. 接口不能被继承'), 'C', '传统接口定义行为契约、只声明方法签名。Java8+支持default方法，但核心思想仍是契约定义。', 7, 'medium', 2.00, 0, 1, NOW(), NOW()),
('single_choice', '数据库连接池的最小连接数一般设置为？', JSON_ARRAY('A. 0', 'B. 与CPU核心数相当', 'C. 与最大连接数相同', 'D. 1000'), 'B', '最小空闲连接数通常设为CPU核心数的1-2倍，平衡响应速度与资源占用。', 5, 'hard', 3.00, 0, 1, NOW(), NOW()),
('single_choice', 'DNS解析中，A记录的作用是？', JSON_ARRAY('A. 域名→IPv4地址', 'B. 域名→IPv6地址', 'C. 域名→邮件服务器', 'D. 域名→别名'), 'A', 'DNS记录类型: A(IPv4地址)、AAAA(IPv6地址)、MX(邮件服务器)、CNAME(别名)、NS(域名服务器)。', 3, 'hard', 3.00, 0, 1, NOW(), NOW()),
('single_choice', '分页存储管理中，逻辑地址到物理地址的转换由谁完成？', JSON_ARRAY('A. CPU', 'B. 内存管理单元(MMU)', 'C. 硬盘控制器', 'D. 网卡'), 'B', 'MMU(Memory Management Unit)负责虚拟地址→物理地址的转换，通过页表实现地址映射。', 4, 'hard', 3.00, 0, 1, NOW(), NOW()),
('single_choice', '哪种设计模式最适合实现"一对多"的依赖关系？', JSON_ARRAY('A. 单例模式', 'B. 观察者模式', 'C. 工厂模式', 'D. 策略模式'), 'B', '观察者模式定义一对多依赖，当一个对象(Subject)状态变化时，所有依赖它的对象(Observer)自动收到通知。', 6, 'medium', 2.00, 0, 1, NOW(), NOW()),
('single_choice', 'B-树常用于什么场景？', JSON_ARRAY('A. 字符串匹配', 'B. 数据库索引和文件系统', 'C. 图像处理', 'D. 网络路由'), 'B', 'B-树是多路平衡搜索树，节点可包含多个键，减少磁盘I/O次数，广泛用于数据库索引和文件系统。', 2, 'hard', 3.00, 0, 1, NOW(), NOW());

-- ==================== 多选题(60题) ====================
INSERT INTO questions (question_type, content, options, correct_answer, analysis, category_id, difficulty, default_score, is_deleted, created_by_id, created_at, updated_at) VALUES
('multiple_choice', '以下哪些属于计算机的输入设备？', JSON_ARRAY('A. 键盘', 'B. 鼠标', 'C. 显示器', 'D. 扫描仪'), JSON_ARRAY('A', 'B', 'D'), '键盘、鼠标、扫描仪都是将外部信息输入计算机的设备。显示器是输出设备。', 1, 'easy', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '以下哪些属于计算机的输出设备？', JSON_ARRAY('A. 显示器', 'B. 打印机', 'C. 键盘', 'D. 音箱'), JSON_ARRAY('A', 'B', 'D'), '显示器、打印机、音箱都是将计算机处理结果输出的设备。键盘是输入设备。', 1, 'easy', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '以下哪些是冯·诺依曼体系结构的组成部分？', JSON_ARRAY('A. 运算器', 'B. 控制器', 'C. 存储器', 'D. 图形处理器'), JSON_ARRAY('A', 'B', 'C'), '冯·诺依曼结构: 运算器、控制器、存储器、输入设备、输出设备。GPU不是基本部件。', 1, 'medium', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '以下哪些是常见的编程语言？', JSON_ARRAY('A. Python', 'B. Java', 'C. HTML', 'D. C++'), JSON_ARRAY('A', 'B', 'D'), 'Python、Java、C++是编程语言。HTML是标记语言，不是编程语言。', 1, 'easy', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '以下关于进制的说法正确的有？', JSON_ARRAY('A. 二进制只有0和1', 'B. 十六进制用0-9和A-F表示', 'C. 八进制用0-7表示', 'D. 十进制有0-9十个数字'), JSON_ARRAY('A', 'B', 'C', 'D'), '以上都是正确说法。二进制2种、八进制8种、十进制10种、十六进制16种符号。', 1, 'easy', 3.00, 0, 1, NOW(), NOW()),

('multiple_choice', '以下哪些数据结构是线性的？', JSON_ARRAY('A. 数组', 'B. 链表', 'C. 栈', 'D. 二叉树'), JSON_ARRAY('A', 'B', 'C'), '线性结构: 元素之间存在一对一关系。数组/链表/栈/队列都是线性结构。二叉树是非线性结构。', 2, 'easy', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '以下哪些排序算法的时间复杂度是O(n²)？', JSON_ARRAY('A. 冒泡排序', 'B. 选择排序', 'C. 插入排序', 'D. 快速排序(平均)'), JSON_ARRAY('A', 'B', 'C'), '冒泡、选择、插入排序平均和最坏都是O(n²)。快速排序平均O(n log n)。', 2, 'medium', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '以下哪些属于哈希表的冲突解决方法？', JSON_ARRAY('A. 链地址法(拉链法)', 'B. 开放地址法', 'C. 再哈希法', 'D. 建立公共溢出区'), JSON_ARRAY('A', 'B', 'C', 'D'), '四种都是常见哈希冲突解决方案。链地址法最常用(Java HashMap)。', 2, 'medium', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '关于二叉树，以下说法正确的有？', JSON_ARRAY('A. 满二叉树每层节点数都达到最大', 'B. 完全二叉树节点按层序编号与满二叉树对应', 'C. 二叉搜索树左子树值小于根', 'D. 平衡二叉树高度为O(log n)'), JSON_ARRAY('A', 'B', 'C', 'D'), '四种说法都是正确的。这些是二叉树体系中的基本概念和性质。', 2, 'medium', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '以下哪些算法使用了分治思想？', JSON_ARRAY('A. 归并排序', 'B. 快速排序', 'C. 二分查找', 'D. 冒泡排序'), JSON_ARRAY('A', 'B', 'C'), '分治法: 将大问题分解为小问题解决后合并。归并、快排、二分查找都是分治。冒泡是蛮力法。', 2, 'hard', 3.00, 0, 1, NOW(), NOW()),

('multiple_choice', '以下哪些属于TCP协议的特性？', JSON_ARRAY('A. 面向连接', 'B. 可靠传输', 'C. 流量控制', 'D. 无连接'), JSON_ARRAY('A', 'B', 'C'), 'TCP特性: 面向连接(三次握手)、可靠(确认重传)、流量控制(滑动窗口)、拥塞控制。无连接是UDP的特性。', 3, 'easy', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '以下哪些是合法的IPv4私网地址段？', JSON_ARRAY('A. 10.0.0.0/8', 'B. 172.16.0.0/12', 'C. 192.168.0.0/16', 'D. 8.8.8.0/24'), JSON_ARRAY('A', 'B', 'C'), 'RFC1918定义的私网地址: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16。8.8.8.8是Google公共DNS，公网地址。', 3, 'medium', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '以下哪些协议属于应用层协议？', JSON_ARRAY('A. HTTP', 'B. FTP', 'C. DNS', 'D. TCP'), JSON_ARRAY('A', 'B', 'C'), 'HTTP/FTP/DNS都是应用层协议。TCP是传输层协议，为应用层提供可靠传输服务。', 3, 'easy', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '关于HTTP与HTTPS的区别，正确的有？', JSON_ARRAY('A. HTTP明文传输，HTTPS加密传输', 'B. HTTP端口80，HTTPS端口443', 'C. HTTPS需要SSL证书', 'D. HTTPS比HTTP更快'), JSON_ARRAY('A', 'B', 'C'), 'HTTPS加密会增加握手开销，所以比HTTP慢(虽有优化)。其他三项正确。', 3, 'medium', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '以下哪些是常见的DDoS攻击类型？', JSON_ARRAY('A. SYN Flood', 'B. UDP Flood', 'C. HTTP Flood', 'D. SQL Injection'), JSON_ARRAY('A', 'B', 'C'), 'SYN/UDP/HTTP Flood都是通过耗尽资源实现拒绝服务。SQL注入是代码注入攻击，不属于DDoS。', 3, 'hard', 3.00, 0, 1, NOW(), NOW()),

('multiple_choice', '以下哪些属于进程间通信(IPC)方式？', JSON_ARRAY('A. 管道', 'B. 共享内存', 'C. 消息队列', 'D. 信号量'), JSON_ARRAY('A', 'B', 'C', 'D'), '四种都是IPC方式。管道、共享内存、消息队列用于数据传递，信号量用于进程同步和互斥。', 4, 'medium', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '以下哪些是Linux系统的特点？', JSON_ARRAY('A. 开源免费', 'B. 多用户多任务', 'C. 支持多种硬件平台', 'D. 需要付费使用'), JSON_ARRAY('A', 'B', 'C'), 'Linux是开源免费系统(GPL协议)，支持多用户多任务，可运行在多种CPU架构上。', 4, 'easy', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '死锁的预防措施包括？', JSON_ARRAY('A. 破坏互斥条件', 'B. 破坏请求保持条件', 'C. 破坏不可剥夺条件', 'D. 破坏循环等待条件'), JSON_ARRAY('A', 'B', 'C', 'D'), '破坏死锁四个必要条件中的任意一个都可以预防死锁。实践中常用破坏循环等待(资源有序分配)。', 4, 'medium', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '进程调度算法包括？', JSON_ARRAY('A. 先来先服务(FCFS)', 'B. 最短作业优先(SJF)', 'C. 时间片轮转(RR)', 'D. 优先级调度'), JSON_ARRAY('A', 'B', 'C', 'D'), '四种都是常见进程调度算法，各有优缺点。现代操作系统常结合多种策略。', 4, 'easy', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '以下哪些属于操作系统的主要功能？', JSON_ARRAY('A. 进程管理', 'B. 内存管理', 'C. 文件管理', 'D. 设备管理'), JSON_ARRAY('A', 'B', 'C', 'D'), '操作系统五大功能: 进程管理、内存管理、文件管理、设备管理、用户接口。全部正确。', 4, 'easy', 3.00, 0, 1, NOW(), NOW()),

('multiple_choice', 'SQL中，以下哪些是DML(数据操作语言)语句？', JSON_ARRAY('A. SELECT', 'B. INSERT', 'C. UPDATE', 'D. CREATE'), JSON_ARRAY('A', 'B', 'C'), 'DML: SELECT/INSERT/UPDATE/DELETE操作数据。DDL: CREATE/ALTER/DROP操作表结构。', 5, 'easy', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '数据库事务的ACID特性包括？', JSON_ARRAY('A. 原子性(Atomicity)', 'B. 一致性(Consistency)', 'C. 隔离性(Isolation)', 'D. 持久性(Durability)'), JSON_ARRAY('A', 'B', 'C', 'D'), 'ACID是事务的四个基本特性。原子性: 全做或全不做；一致性: 前后状态一致；隔离性: 并发不干扰；持久性: 提交后永久保存。', 5, 'easy', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '以下哪种索引类型在MySQL中支持？', JSON_ARRAY('A. B+树索引', 'B. 哈希索引', 'C. 全文索引', 'D. 空间索引(R-Tree)'), JSON_ARRAY('A', 'B', 'C', 'D'), 'MySQL支持多种索引: B+树(默认, InnoDB/MyISAM)、哈希(Memory引擎)、全文(MyISAM/InnoDB5.6+)、空间索引。', 5, 'hard', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '关于数据库范式，以下正确的是？', JSON_ARRAY('A. 1NF要求字段原子性', 'B. 2NF消除了部分函数依赖', 'C. 3NF消除了传递函数依赖', 'D. 范式越高越好'), JSON_ARRAY('A', 'B', 'C'), '范式越高数据冗余越少但查询性能可能下降(需多表JOIN)。实际开发常在3NF和反范式间平衡。', 5, 'medium', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '以下哪些操作会使用索引？', JSON_ARRAY('A. WHERE子句中的条件列', 'B. ORDER BY排序列', 'C. GROUP BY分组列', 'D. JOIN连接列'), JSON_ARRAY('A', 'B', 'C', 'D'), '索引在WHERE条件过滤、排序、分组、表连接时都可能被使用，能大幅提升性能。', 5, 'medium', 3.00, 0, 1, NOW(), NOW()),

('multiple_choice', '以下哪些是软件开发的生命周期阶段？', JSON_ARRAY('A. 需求分析', 'B. 系统设计', 'C. 编码实现', 'D. 运维部署'), JSON_ARRAY('A', 'B', 'C', 'D'), '完整的软件生命周期包括以上所有阶段，形成需求→设计→编码→测试→部署→运维的闭环。', 6, 'easy', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '以下哪些属于敏捷开发中的实践？', JSON_ARRAY('A. 每日站会', 'B. 迭代开发', 'C. 结对编程', 'D. 详细的文档驱动'), JSON_ARRAY('A', 'B', 'C'), '敏捷注重快速迭代、面对面沟通、可工作软件。详细的文档驱动是瀑布模型的特点。', 6, 'medium', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', 'Git中以下哪些是正确的操作？', JSON_ARRAY('A. git clone 克隆仓库', 'B. git add 暂存文件', 'C. git commit 提交到本地仓库', 'D. git push 推送到远程仓库'), JSON_ARRAY('A', 'B', 'C', 'D'), '四个都是Git的常用基本操作，构成了日常工作的标准流程。', 6, 'easy', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '软件测试类型包括？', JSON_ARRAY('A. 单元测试', 'B. 集成测试', 'C. 系统测试', 'D. 验收测试'), JSON_ARRAY('A', 'B', 'C', 'D'), '测试按阶段分为单元→集成→系统→验收测试，是从局部到整体的逐步验证过程。', 6, 'medium', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '以下哪些代码管理平台基于Git？', JSON_ARRAY('A. GitHub', 'B. GitLab', 'C. Gitee', 'D. SVN'), JSON_ARRAY('A', 'B', 'C'), 'GitHub/GitLab/Gitee都是基于Git的代码托管平台。SVN是集中式版本控制，与Git不同。', 6, 'easy', 3.00, 0, 1, NOW(), NOW()),

('multiple_choice', '面向对象编程中，以下哪些是合法的访问修饰符？', JSON_ARRAY('A. public', 'B. private', 'C. protected', 'D. internal'), JSON_ARRAY('A', 'B', 'C'), 'public/private/protected是Java/C++中最常见的三种访问控制。internal是C#特有。', 7, 'easy', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', 'Python中，以下哪些是合法的数据类型？', JSON_ARRAY('A. int', 'B. str', 'C. list', 'D. dict'), JSON_ARRAY('A', 'B', 'C', 'D'), '四种都是Python内置数据类型: 整数、字符串、列表、字典。', 7, 'easy', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '关于接口和抽象类的区别，正确的有？', JSON_ARRAY('A. 接口可以多实现，抽象类只能单继承', 'B. 接口方法默认是抽象的', 'C. 抽象类可以有构造方法', 'D. 接口可以包含成员变量'), JSON_ARRAY('A', 'B', 'C'), '接口中的变量默认是public static final(常量)，不是普通成员变量。其他三项正确。', 7, 'medium', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '设计模式的类型包括？', JSON_ARRAY('A. 创建型模式', 'B. 结构型模式', 'C. 行为型模式', 'D. 功能型模式'), JSON_ARRAY('A', 'B', 'C'), 'GoF设计模式分为三类: 创建型(工厂、单例等)、结构型(代理、装饰等)、行为型(观察者、策略等)。', 7, 'hard', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '以下哪些是Python中常用的第三方库？', JSON_ARRAY('A. NumPy(数值计算)', 'B. Pandas(数据分析)', 'C. Django(Web框架)', 'D. Selenium(自动化测试)'), JSON_ARRAY('A', 'B', 'C', 'D'), '四个都是广泛使用的Python库，分别覆盖科学计算、数据分析、Web开发和自动化测试领域。', 7, 'easy', 3.00, 0, 1, NOW(), NOW()),

('multiple_choice', '关于TCP和UDP的区别，正确的有？', JSON_ARRAY('A. TCP是面向连接的', 'B. UDP传输效率更高', 'C. TCP保证数据顺序', 'D. UDP没有流量控制'), JSON_ARRAY('A', 'B', 'C', 'D'), 'TCP面向连接、可靠、有序、有流量控制。UDP无连接、不可靠、无序、无流量控制，但效率高。', 3, 'medium', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '以下哪些属于RESTful API的设计原则？', JSON_ARRAY('A. 使用HTTP方法表达操作', 'B. 资源用URL标识', 'C. 无状态通信', 'D. 用XML作为唯一数据格式'), JSON_ARRAY('A', 'B', 'C'), 'RESTful原则: 资源URL化、HTTP方法语义化(GET/POST/PUT/DELETE)、无状态。JSON和XML都可作为数据格式。', 3, 'medium', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '以下哪些是数据库索引可能带来的负面影响？', JSON_ARRAY('A. 占用额外磁盘空间', 'B. 降低INSERT速度', 'C. 降低UPDATE速度', 'D. 可能让查询变慢'), JSON_ARRAY('A', 'B', 'C', 'D'), '索引是双刃剑: 占用空间、影响写性能，不当使用(如小表建索引)甚至会让查询更慢。', 5, 'medium', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '关于HashMap，以下说法正确的有？', JSON_ARRAY('A. 基于哈希表实现', 'B. 允许null键和null值', 'C. 线程安全', 'D. 默认初始容量为16'), JSON_ARRAY('A', 'B', 'D'), 'HashMap非线程安全(需要ConcurrentHashMap)，其他三项正确。Java中HashMap初始容量16，负载因子0.75。', 2, 'medium', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '关于封装的好处，正确的有？', JSON_ARRAY('A. 隐藏内部实现细节', 'B. 提高代码安全性', 'C. 便于修改内部实现而不影响外部', 'D. 使代码不能运行'), JSON_ARRAY('A', 'B', 'C'), '封装通过private+getter/setter保护数据，修改内部不影响外部调用方，但不会阻止代码运行。', 7, 'medium', 3.00, 0, 1, NOW(), NOW()),

('multiple_choice', '以下哪些是栈的实际应用场景？', JSON_ARRAY('A. 括号匹配检查', 'B. 表达式求值', 'C. 函数递归调用', 'D. 浏览器前进后退'), JSON_ARRAY('A', 'B', 'C', 'D'), '栈的应用: 括号匹配、后缀表达式计算、函数调用栈、撤销/回退功能。', 2, 'medium', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '以下哪些是图的遍历算法？', JSON_ARRAY('A. 深度优先搜索(DFS)', 'B. 广度优先搜索(BFS)', 'C. Dijkstra算法', 'D. 冒泡排序'), JSON_ARRAY('A', 'B'), 'DFS和BFS是图的基本遍历算法。Dijkstra是最短路径算法，冒泡是排序算法。', 2, 'easy', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '哪些因素会影响数据库查询性能？', JSON_ARRAY('A. 是否使用索引', 'B. SQL语句的写法', 'C. 数据量大小', 'D. 硬件配置'), JSON_ARRAY('A', 'B', 'C', 'D'), '查询性能是多因素综合作用的结果，索引设计、SQL优化、数据规模、硬件配置都影响性能。', 5, 'easy', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '关于HTTP请求方法，以下正确的是？', JSON_ARRAY('A. GET请求参数在URL中', 'B. POST请求参数在请求体中', 'C. PUT用于更新资源', 'D. DELETE用于删除资源'), JSON_ARRAY('A', 'B', 'C', 'D'), 'RESTful规范中四种方法各司其职:GET(读)、POST(增)、PUT(改)、DELETE(删)。', 3, 'easy', 3.00, 0, 1, NOW(), NOW()),
('multiple_choice', '以下哪些是软件设计时应遵循的原则？', JSON_ARRAY('A. 单一职责原则', 'B. 开闭原则', 'C. 里氏替换原则', 'D. 接口隔离原则'), JSON_ARRAY('A', 'B', 'C', 'D'), 'SOLID五大原则: 单一职责、开闭、里氏替换、接口隔离、依赖倒置。以上四个都是。', 6, 'medium', 3.00, 0, 1, NOW(), NOW());

-- ==================== 判断题(60题) ====================
INSERT INTO questions (question_type, content, options, correct_answer, analysis, category_id, difficulty, default_score, is_deleted, created_by_id, created_at, updated_at) VALUES
('true_false', '计算机只能识别二进制代码。', JSON_ARRAY(), '对', '计算机硬件基于高低电平，只能直接识别和处理二进制0和1。', 1, 'easy', 2.00, 0, 1, NOW(), NOW()),
('true_false', '1GB等于1000MB。', JSON_ARRAY(), '错', '计算机存储单位是1024进制，1GB=1024MB。部分硬盘厂商用1000进制。', 1, 'easy', 2.00, 0, 1, NOW(), NOW()),
('true_false', 'CPU的主频越高，性能一定越好。', JSON_ARRAY(), '错', 'CPU性能取决于架构、核心数、缓存、指令集等多种因素，不能只看主频。', 1, 'medium', 2.00, 0, 1, NOW(), NOW()),
('true_false', '固态硬盘(SSD)的读写速度通常比机械硬盘(HDD)快。', JSON_ARRAY(), '对', 'SSD没有机械部件，随机读写速度远超HDD。HDD有物理磁头移动延迟。', 1, 'easy', 2.00, 0, 1, NOW(), NOW()),
('true_false', 'RAM中的���据在断电后会丢失。', JSON_ARRAY(), '对', 'RAM是易失性存储器，断电后数据消失。ROM是非易失性的，断电后数据保留。', 1, 'easy', 2.00, 0, 1, NOW(), NOW()),

('true_false', 'ROM是只读存储器，数据断电后不会丢失。', JSON_ARRAY(), '对', 'ROM(Read-Only Memory)是非易失性存储器，常用于存放BIOS等固件程序。', 1, 'easy', 2.00, 0, 1, NOW(), NOW()),
('true_false', '计算机中的所有数据最终都以十进制形式存储。', JSON_ARRAY(), '错', '所有数据最终以二进制(0和1)形式存储。十进制只是人类可读的表示方式。', 1, 'easy', 2.00, 0, 1, NOW(), NOW()),
('true_false', '显卡(GPU)只能用于图形渲染。', JSON_ARRAY(), '错', '现代GPU也广泛用于通用计算(GPGPU)，如深度学习训练、科学计算等。', 1, 'medium', 2.00, 0, 1, NOW(), NOW()),
('true_false', '操作系统是系统软件。', JSON_ARRAY(), '对', '系统软件包括操作系统、编译器等。应用软件如Word、浏览器等运行在系统软件之上。', 1, 'easy', 2.00, 0, 1, NOW(), NOW()),
('true_false', 'Python是一种编译型语言。', JSON_ARRAY(), '错', 'Python是解释型语言(也有JIT编译如PyPy)。C/C++/Go/Rust是编译型语言。', 1, 'easy', 2.00, 0, 1, NOW(), NOW()),

('true_false', '栈是先进先出(FIFO)的数据结构。', JSON_ARRAY(), '错', '栈是后进先出(LIFO)。队列才是先进先出(FIFO)。这是考试常考点。', 2, 'easy', 2.00, 0, 1, NOW(), NOW()),
('true_false', '链表支持随机访问，时间复杂度为O(1)。', JSON_ARRAY(), '错', '链表不支持随机访问，需要从头遍历，访问第k个节点需要O(k)时间。数组才支持O(1)随机访问。', 2, 'easy', 2.00, 0, 1, NOW(), NOW()),
('true_false', '哈希表的查找效率在最坏情况下可能是O(n)。', JSON_ARRAY(), '对', '最坏情况(所有key哈希到同一位置)退化为链表，查找O(n)。平均情况O(1)。', 2, 'medium', 2.00, 0, 1, NOW(), NOW()),
('true_false', '二叉搜索树的中序遍历结果是递增有序的。', JSON_ARRAY(), '对', '二叉搜索树性质: 左<根<右，中序遍历(左→根→右)输出递增序列。', 2, 'medium', 2.00, 0, 1, NOW(), NOW()),
('true_false', '递归函数一定比非递归版本执行速度快。', JSON_ARRAY(), '错', '递归有函数调用开销(栈帧)，通常比非递归慢。但代码更简洁，更容易理解和维护。', 2, 'medium', 2.00, 0, 1, NOW(), NOW()),

('true_false', '动态规划适用于有重叠子问题的问题。', JSON_ARRAY(), '对', '动态规划核心是识别重叠子问题并用记忆化避免重复计算，如斐波那契、背包问题。', 2, 'medium', 2.00, 0, 1, NOW(), NOW()),
('true_false', '平衡二叉树的查找时间复杂度为O(log n)。', JSON_ARRAY(), '对', '平衡二叉树(AVL/红黑树)通过旋转保持树的高度为O(log n)，保证查找效率。', 2, 'medium', 2.00, 0, 1, NOW(), NOW()),
('true_false', '所有递归算法都可以转换为非递归实现。', JSON_ARRAY(), '对', '递归本质上可用栈模拟。所有递归算法都可以用显式栈+循环转换为非递归实现。', 2, 'hard', 3.00, 0, 1, NOW(), NOW()),
('true_false', '图的邻接矩阵存储方式比邻接表更节省空间。', JSON_ARRAY(), '错', '邻接矩阵O(n²)空间，适合稠密图。邻接表O(n+e)空间，适合稀疏图。大多数实际图为稀疏图。', 2, 'medium', 2.00, 0, 1, NOW(), NOW()),
('true_false', '冒泡排序是稳定的排序算法。', JSON_ARRAY(), '对', '冒泡排序相邻比较交换，相等元素不交换位置，是稳定排序。', 2, 'easy', 2.00, 0, 1, NOW(), NOW()),

('true_false', 'TCP协议比UDP协议更可靠。', JSON_ARRAY(), '对', 'TCP提供确认重传、顺序控制、流量控制等可靠性机制。UDP不提供这些保证。', 3, 'easy', 2.00, 0, 1, NOW(), NOW()),
('true_false', 'IP地址由MAC地址转换而来。', JSON_ARRAY(), '错', 'IP地址(网络层)和MAC地址(数据链路层)是不同的地址体系。ARP协议将IP→MAC映射，但非转换关系。', 3, 'medium', 2.00, 0, 1, NOW(), NOW()),
('true_false', 'DNS使用UDP协议的53端口。', JSON_ARRAY(), '对', 'DNS默认使用UDP 53端口(也支持TCP 53)，因为DNS查询数据量小，UDP高效。', 3, 'medium', 2.00, 0, 1, NOW(), NOW()),
('true_false', '路由器工作在OSI模型的第三层(网络层)。', JSON_ARRAY(), '对', '路由器根据IP地址转发数据包，属于网络层。交换机通常工作在数据链路层(第二层)。', 3, 'easy', 2.00, 0, 1, NOW(), NOW()),
('true_false', '防火墙可以完全防止所有网络攻击。', JSON_ARRAY(), '错', '防火墙是网络安全的一层防护，但不能防止所有攻击(如内部威胁、零日漏洞、社会工程攻击)。', 3, 'medium', 2.00, 0, 1, NOW(), NOW()),

('true_false', 'NAT(网络地址转换)可以将私网IP转换为公网IP。', JSON_ARRAY(), '对', 'NAT将内部私网IP映射为公网IP访问互联网，同时解决IPv4地址不足问题。', 3, 'medium', 2.00, 0, 1, NOW(), NOW()),
('true_false', 'WebSocket协议是全双工的。', JSON_ARRAY(), '对', 'WebSocket建立连接后，客户端和服务器可同时发送数据(全双工)。HTTP是半双工(请求-响应)。', 3, 'hard', 3.00, 0, 1, NOW(), NOW()),
('true_false', 'MAC地址是唯一的，全球不会重复。', JSON_ARRAY(), '对', 'MAC地址由IEEE分配，理论上全球唯一。但实际上可被软件修改，存在伪造可能。', 3, 'easy', 2.00, 0, 1, NOW(), NOW()),
('true_false', 'WiFi使用的是无线电波通信。', JSON_ARRAY(), '对', 'WiFi(IEEE 802.11)使用2.4GHz或5GHz无线电波进行无线局域网通信。', 3, 'easy', 2.00, 0, 1, NOW(), NOW()),
('true_false', 'HTTPS比HTTP更安全但传输速度也更快。', JSON_ARRAY(), '错', 'HTTPS安全但握手阶段需要SSL/TLS加解密，比HTTP稍慢。HTTP/2和TLS 1.3已大幅优化。', 3, 'medium', 2.00, 0, 1, NOW(), NOW()),

('true_false', '一个进程可以包含多个线程。', JSON_ARRAY(), '对', '进程是资源容器，线程是执行单元。一个进程至少有一个主线程，可创建多个工作线程。', 4, 'easy', 2.00, 0, 1, NOW(), NOW()),
('true_false', '虚拟内存让程序可以使用比物理内存更大的地址空间。', JSON_ARRAY(), '对', '虚拟内存技术将硬盘空间映射到地址空间，程序可用的地址空间可超过物理内存大小。', 4, 'easy', 2.00, 0, 1, NOW(), NOW()),
('true_false', 'Linux系统中，root用户拥有最高权限。', JSON_ARRAY(), '对', 'root是Linux系统的超级管理员账户，拥有系统所有权限，可执行任何操作。', 4, 'easy', 2.00, 0, 1, NOW(), NOW()),
('true_false', '死锁一旦发生，只能重启系统来解决。', JSON_ARRAY(), '错', '可���过终止死锁中的进程或剥夺资源来解除死锁。银行家算法可避免死锁。', 4, 'medium', 2.00, 0, 1, NOW(), NOW()),
('true_false', '时间片轮转调度算法对所有进程是公平的。', JSON_ARRAY(), '对', 'RR给每个就绪进程分配相等的时间片轮流执行，保证各进程获得公平的CPU时间。', 4, 'easy', 2.00, 0, 1, NOW(), NOW()),

('true_false', '数据库的索引一定能提升查询性能。', JSON_ARRAY(), '错', '小表建索引反而可能降低性能(索引维护开销大于全表扫描)。不恰当的索引也可能不被优化器使用。', 5, 'medium', 2.00, 0, 1, NOW(), NOW()),
('true_false', 'TRUNCATE TABLE操作可以回滚。', JSON_ARRAY(), '错', 'TRUNCATE是DDL操作，大多数数据库(MyISAM)不能回滚。InnoDB在事务中可回滚。', 5, 'medium', 2.00, 0, 1, NOW(), NOW()),
('true_false', 'WHERE子句中LIKE "%xxx"可以使用索引。', JSON_ARRAY(), '错', '以%开头的模糊查询无法使用B+树索引(前缀匹配失效)。LIKE"xxx%"可以使用索引。', 5, 'medium', 2.00, 0, 1, NOW(), NOW()),
('true_false', '数据库的JOIN操作一定比子查询快。', JSON_ARRAY(), '错', '性能取决于数据量、索引、具体写法。优化器可能将子查询转换为JOIN。需要具体分析。', 5, 'hard', 3.00, 0, 1, NOW(), NOW()),
('true_false', 'MySQL的InnoDB引擎支持行级锁。', JSON_ARRAY(), '对', 'InnoDB支持行级锁(和表级锁)，对同一表中不同行的并发操作不互相阻塞。MyISAM只支持表级锁。', 5, 'easy', 2.00, 0, 1, NOW(), NOW()),

('true_false', '版本控制工具Git是分布式版本控制系统。', JSON_ARRAY(), '对', 'Git是分布式VCS，每个开发者电脑上都有完整的仓库副本，可离线工作。SVN是集中式的。', 6, 'easy', 2.00, 0, 1, NOW(), NOW()),
('true_false', '单元测试应该由专业的测试人员来编写。', JSON_ARRAY(), '错', '单元测试通常由开发人员编写，验证代码最小单元的正确性。测试人员负责集成/系统测试。', 6, 'easy', 2.00, 0, 1, NOW(), NOW()),
('true_false', '敏捷开发不需要任何文档。', JSON_ARRAY(), '错', '敏捷宣言说"工作的软件高于详尽的文档"，但并非不需要文档，只需要必要的文档。', 6, 'medium', 2.00, 0, 1, NOW(), NOW()),
('true_false', '程序出现bug是无法避免的。', JSON_ARRAY(), '对', '完美无bug的软件理论上不可能(停止问题等)。目标是尽可能减少bug、尽早发现并修复。', 6, 'medium', 2.00, 0, 1, NOW(), NOW()),
('true_false', '代码review(审查)的主要目的是找bug。', JSON_ARRAY(), '错', '代码审查目的多方面: 知识分享、代码规范、设计评审，发现bug只是其中之一。', 6, 'medium', 2.00, 0, 1, NOW(), NOW()),

('true_false', '面向对象编程中，子类可以访问父类的private成员。', JSON_ARRAY(), '错', 'private成员只有本类内部可以访问，子类也不能直接访问。protected成员子类可以访问。', 7, 'easy', 2.00, 0, 1, NOW(), NOW()),
('true_false', 'Python中的变量使用前不需要声明类型。', JSON_ARRAY(), '对', 'Python是动态类型语言，变量类型在运行时自动推导，不需要显式声明。', 7, 'easy', 2.00, 0, 1, NOW(), NOW()),
('true_false', '多态可以提高代码的扩展性和可维护性。', JSON_ARRAY(), '对', '多态让新功能通过添加新类来实现(开闭原则)，不需要修改已有代码，提高扩展性。', 7, 'medium', 2.00, 0, 1, NOW(), NOW()),
('true_false', '抽象类不能被实例化。', JSON_ARRAY(), '对', '抽象类包含未实现的抽象方法，不能被直接实例化，必须通过子类实现抽象方法后实例化子类。', 7, 'easy', 2.00, 0, 1, NOW(), NOW()),
('true_false', '构造函数可以有返回值。', JSON_ARRAY(), '错', '构造函数没有返回值类型(连void都没有)，作用是初始化对象，返回的是新创建的对象引用。', 7, 'easy', 2.00, 0, 1, NOW(), NOW());

-- ==================== 填空题(50题) ====================
INSERT INTO questions (question_type, content, options, correct_answer, analysis, category_id, difficulty, default_score, is_deleted, created_by_id, created_at, updated_at) VALUES
('fill_blank', '计算机中，CPU的中文全称是______。', JSON_ARRAY(), '中央处理器', 'CPU=Central Processing Unit=中央处理器，是计算机的运算和控制核心。', 1, 'easy', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', '8个二进制位组成1个______。', JSON_ARRAY(), '字节', '1Byte=8bit，字节是计算机存储和数据处理的基本单位。', 1, 'easy', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', '冯·诺依曼体系结构中，计算机由运算器、控制器、______、输入设备和输出设备五部分组成。', JSON_ARRAY(), '存储器', '五大部件缺一不可，存储程序是冯·诺依曼结构的核心思想。', 1, 'medium', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', '在微型计算机中，RAM的中文名称是______。', JSON_ARRAY(), '随机存取存储器', 'RAM=Random Access Memory，可随机读写，断电数据丢失。', 1, 'easy', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', '十六进制数FF对应的十进制数是______。', JSON_ARRAY(), '255', 'FF(16)=15×16+15=255。十六进��中F=15。', 1, 'medium', 3.00, 0, 1, NOW(), NOW()),

('fill_blank', '队列的特点是______先出。', JSON_ARRAY(), '先进', '队列是先进先出(FIFO)的线性数据结构。', 2, 'easy', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', '深度优先搜索的英文缩写是______。', JSON_ARRAY(), 'DFS', 'DFS=Depth First Search，从起始节点沿一条路径深入到底再回溯。', 2, 'easy', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', '有n个节点的完全二叉树的深度是______(用n表示)。', JSON_ARRAY(), '⌊log₂n⌋+1', '由2^(h-1)≤n<2^h推导而来。', 2, 'hard', 4.00, 0, 1, NOW(), NOW()),
('fill_blank', '在链表中，每个节点包含数据域和______域。', JSON_ARRAY(), '指针', '链表节点=数据域(存储数据)+指针域(指向下一个节点)。双向链表有两个指针域。', 2, 'easy', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', '堆排序使用的数据结构是______。', JSON_ARRAY(), '堆', '堆排序利用最大堆/最小堆的性质，建堆O(n)，每次取堆顶调整O(log n)。', 2, 'medium', 3.00, 0, 1, NOW(), NOW()),

('fill_blank', '在TCP/IP协议栈中，传输层两个主要协议是______和______。', JSON_ARRAY(), 'TCP和UDP', 'TCP提供可靠传输，UDP提供高效无连接传输。', 3, 'easy', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', 'HTTP协议默认使用______端口。', JSON_ARRAY(), '80', 'HTTP=80，HTTPS=443，FTP=21，SSH=22。', 3, 'easy', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', '将域名转换为IP地址的系统称为______。', JSON_ARRAY(), 'DNS', 'DNS(Domain Name System)是互联网的基础服务之一。', 3, 'easy', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', 'IPv4地址由______位二进制数构成。', JSON_ARRAY(), '32', 'IPv4地址32位(4字节)，IPv6地址128位(16字节)。', 3, 'easy', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', 'TCP建立连接需要______次握手。', JSON_ARRAY(), '三', '三次握手: SYN→SYN+ACK→ACK，建立可靠的双向通道。', 3, 'easy', 3.00, 0, 1, NOW(), NOW()),

('fill_blank', '操作系统的基本特征包括并发、______、虚拟和异步。', JSON_ARRAY(), '共享', '操作系统的四个基本特征: 并发、共享、虚拟、异步。', 4, 'medium', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', 'Linux中，显示当前工作目录的命令是______。', JSON_ARRAY(), 'pwd', 'pwd=Print Working Directory，显示当前所在的目录路径。', 4, 'easy', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', 'Linux中，修改文件权限的命令是______。', JSON_ARRAY(), 'chmod', 'chmod(Change Mode)用于修改文件/目录的读(r)、写(w)、执行(x)权限。', 4, 'medium', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', '进程的三个基本状态是就绪态、运行态和______。', JSON_ARRAY(), '阻塞态', '三态模型: Ready、Running、Blocked。进程在这三个状态间转换。', 4, 'easy', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', '临界区(Critical Section)指的是访问______资源的代码段。', JSON_ARRAY(), '共享', '临界区是访问共享资源的代码区域，需要互斥访问，保证数据一致性。', 4, 'medium', 3.00, 0, 1, NOW(), NOW()),

('fill_blank', 'SQL中，创建数据库表的语句以______关键字开头。', JSON_ARRAY(), 'CREATE TABLE', 'DDL语句: CREATE TABLE 表名 (列名 类型 约束,...)。', 5, 'easy', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', '数据库事务具有四个特性，简称______。', JSON_ARRAY(), 'ACID', 'Atomicity原子性、Consistency一致性、Isolation隔离性、Durability持久性。', 5, 'easy', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', '在MySQL中，默认的存储引擎是______。', JSON_ARRAY(), 'InnoDB', 'MySQL 5.5起默认引擎为InnoDB，支持事务、行级锁、外键约束。', 5, 'medium', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', 'SQL的SELECT语句中，消除重复行的关键字是______。', JSON_ARRAY(), 'DISTINCT', 'SELECT DISTINCT 列名 FROM 表名。类似地，COUNT(DISTINCT 列名)计算不重复值数量。', 5, 'easy', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', '数据库设计中，E-R图的E代表______。', JSON_ARRAY(), '实体', 'E-R图(Entity-Relationship Diagram): 实体(矩形)、属性(椭圆)、联系(菱形)。', 5, 'easy', 3.00, 0, 1, NOW(), NOW()),

('fill_blank', '软件工程中，SDLC的全称是______。', JSON_ARRAY(), '软件开发生命周期', 'SDLC=Software Development Life Cycle，涵盖需求、设计、编码、测试、部署、维护。', 6, 'medium', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', '版本控制系统中，VCS的全称是______。', JSON_ARRAY(), '版本控制系统', 'VCS=Version Control System，用于跟踪和管理代码变更历史。', 6, 'easy', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', 'Git中，将工作区修改添加到暂存区的命令是______。', JSON_ARRAY(), 'git add', 'git add → git commit → git push 是Git的基本工作流。', 6, 'easy', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', 'OCP(开闭原则)的含义是对______开放，对______关闭。', JSON_ARRAY(), '扩展、修改', '开闭原则: 软件实体应对扩展开放(可以添加新功能)，对修改关闭(不修改已有代码)。', 6, 'medium', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', '软件测试的目的是发现程序中的______。', JSON_ARRAY(), '错误', '测试是为了发现bug而执行程序的过程，证明程序有错而非证明程序正确。', 6, 'easy', 3.00, 0, 1, NOW(), NOW()),

('fill_blank', 'Java中，所有类的基类是______。', JSON_ARRAY(), 'Object', 'Java中所有类默认继承java.lang.Object类，提供toString()、equals()等基本方法。', 7, 'easy', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', '面向对象编程中，将数据和操作数据的方法绑定在一起称为______。', JSON_ARRAY(), '封装', '封装(Encapsulation)隐藏了类的内部实现细节，通过公开的接口与外界交互。', 7, 'easy', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', 'Python中，使用______关键字定义函数。', JSON_ARRAY(), 'def', 'Python定义函数语法: def 函数名(参数列表): 函数体。', 7, 'easy', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', '接口中所有方法默认都是______的(abstract/public)。', JSON_ARRAY(), 'public abstract', 'Java接口中方法默认public abstract，变量默认public static final。', 7, 'medium', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', '设计模式中的单例模式确保一个类只有______个实例。', JSON_ARRAY(), '一', '单例模式通过私有构造函数和静态方法控制实例创建，全局只有一个实例。', 7, 'easy', 3.00, 0, 1, NOW(), NOW()),

('fill_blank', '二分查找要求数据必须是______的。', JSON_ARRAY(), '有序', '二分查找前提是数据有序(O(log n))。无序数据只能用线性查找(O(n))。', 2, 'easy', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', '广度优先搜索的英文缩写是______。', JSON_ARRAY(), 'BFS', 'BFS=Breadth First Search，逐层遍历，用队列实现。', 2, 'easy', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', '归并排序的时间复杂度是______。', JSON_ARRAY(), 'O(n log n)', '归并排序总是O(n log n)，稳定排序，需要O(n)额外空间。', 2, 'medium', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', '处理哈希冲突的链地址法，其本质是使用______结构存储同义词。', JSON_ARRAY(), '链表', '链地址法(拉链法): 每个桶存放一个链表，相同哈希值的元素放在同一链表。Java的HashMap用此方法。', 2, 'medium', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', 'TCP三次握手中，第二次握手服务器回复的报文标志位是______。', JSON_ARRAY(), 'SYN+ACK', '服务端同时设置SYN和ACK标志，既确认客户端的SYN，又发出自己的SYN。', 3, 'medium', 3.00, 0, 1, NOW(), NOW()),

('fill_blank', '子网掩码255.255.255.192对应的CIDR前缀长度为______。', JSON_ARRAY(), '/26', '255.255.255.192=11111111.11111111.11111111.11000000，共26个1。', 3, 'hard', 4.00, 0, 1, NOW(), NOW()),
('fill_blank', '互斥锁(mutex)保证同一时间只有______个线程访问共享资源。', JSON_ARRAY(), '一', '互斥锁用于多线程同步，保证临界区互斥访问，防止数据竞争。', 4, 'medium', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', 'SQL中，用于分组的子句是______。', JSON_ARRAY(), 'GROUP BY', 'GROUP BY配合聚合函数(COUNT/SUM/AVG等)进行分组统计。HAVING用于过滤分组后结果。', 5, 'easy', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', 'MySQL中，查看表结构的命令是______。', JSON_ARRAY(), 'DESC 表名', 'DESC=DESCRIBE，显示表的字段名、类型、是否为空、键等信息。', 5, 'easy', 3.00, 0, 1, NOW(), NOW()),
('fill_blank', '软件工程的三要素是方法、______和过程。', JSON_ARRAY(), '工具', '软件工程=方法(技术)+工具(开发环境)+过程(管理流程)。', 6, 'medium', 3.00, 0, 1, NOW(), NOW());

-- ==================== 简答题(50题) ====================
INSERT INTO questions (question_type, content, options, correct_answer, analysis, category_id, difficulty, default_score, is_deleted, created_by_id, created_at, updated_at) VALUES
('short_answer', '请简述计算机的五大基本部件及其功能。', JSON_ARRAY(), '运算器(算术逻辑运算)、控制器(指令控制和调度)、存储器(存储数据和程序)、输入设备(接收外部信息)、输出设备(输出处理结果)。', '冯·诺依曼体系结构的核心组成。', 1, 'easy', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '请解释RAM和ROM的区别。', JSON_ARRAY(), 'RAM(随机存取存储器)可读可写，断电后数据丢失，用于内存。ROM(只读存储器)只能读不能随意写，断电数据保留，用于存储固件和BIOS。', '两者都是主存储器，关键区别是易失性和读写特性。', 1, 'easy', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '请解释什么是二进制以及为什么计算机使用二进制。', JSON_ARRAY(), '二进制是用0和1表示的数字系统，逢二进一。计算机使用二进制因为电子元件的高低电平自然对应0和1两种状态，实现简单可靠，抗干扰能力强。', '二进制是计算机的数学基础。', 1, 'easy', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '请解释CPU缓存的作用和多级缓存结构。', JSON_ARRAY(), 'CPU缓存是位于CPU和主存之间的高速存储，用于缓解CPU和内存速度不匹配。现代CPU通常有L1(最小最快)、L2、L3(最大最慢)三级缓存，命中缓存可以大幅减少等待内存的时间。', '缓存层次: 速度降、容量升。', 1, 'medium', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '简述固态硬盘(SSD)相比机械硬盘(HDD)的优缺点。', JSON_ARRAY(), '优点: 无机械部件、读写快(尤其随机读写)、静音、功耗低、抗震。缺点: 单位价格高、写入寿命有限(擦写次数)、长时间不通电可能丢数据。', '随着技术进步，SSD性价比不断提高。', 1, 'medium', 5.00, 0, 1, NOW(), NOW()),

('short_answer', '请解释栈和队列的区别，并各举一个实际应用场景。', JSON_ARRAY(), '栈是后进先出(LIFO)，应用: 函数调用栈、浏览器的后退功能。队列是先进先出(FIFO)，应用: 任务调度、消息队列、打印机任务队列。', 'LIFO vs FIFO是最基本的线性结构区别。', 2, 'easy', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '请分析数组和链表的优缺点及适用场景。', JSON_ARRAY(), '数组: O(1)随机访问，空间连续，但插入删除O(n)，容量固定。适用随机访问多的场景。链表: 插入删除O(1)，动态扩容，但随机访问O(n)，额外指针开销。适用频繁增删的场景。', '选择数据结构需要根据实际操作的频率来决定。', 2, 'easy', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '什么是哈希表？请解释其基本原理和冲突解决方法。', JSON_ARRAY(), '哈希表通过哈希函数将键映射到数组下标。发生冲突(不同key映射到同一位置)时，用链地址法(同一位置构建链表)或开放地址法(找下一个空位)解决。平均查找O(1)。', '哈希表是空间换时间的典型应用。', 2, 'medium', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '请解释二叉搜索树的定义、性质和基本操作。', JSON_ARRAY(), '定义: 左子树值<根值<右子树值，且左右子树也是BST。操作: 查找(比较大小定位)、插入(找到叶子位置)、删除(分无子/单子/双子三种情况)。中序遍历得到有序序列。', 'BST是理解更复杂树结构的基础。', 2, 'medium', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '请简述快速排序的基本思想和时间复杂度分析。', JSON_ARRAY(), '基本思想: 选择一个基准(pivot)，将数组分为小于基准和大于基准两部分，递归排序子数组。平均O(n log n)，最坏(已有序且选边元素为基准)O(n²)。可通过随机选基准优化。', '快排是实际应用最广泛的排序算法。', 2, 'hard', 6.00, 0, 1, NOW(), NOW()),

('short_answer', '请解释TCP和UDP协议的主要区别及各自的适用场景。', JSON_ARRAY(), 'TCP: 面向连接、可靠(确认重传)、有序、流量控制，适用网页浏览、文件传输、邮件。UDP: 无连接、不可靠、无序、无流量控制但效率高，适用视频直播、在线游戏、DNS查询等对实时性要求高的场景。', '选TCP还是UDP取决于可靠性和实时性的权衡。', 3, 'easy', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '请描述TCP三次握手的过程。', JSON_ARRAY(), '第一次: 客户端发送SYN=1, seq=x。第二次: 服务器回复SYN=1, ACK=1, seq=y, ack=x+1。第三次: 客户端发送ACK=1, seq=x+1, ack=y+1。双方确认收发能力后连接建立。', '三次握手确保双方都能收发数据。', 3, 'medium', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '请解释DNS的工作原理。', JSON_ARRAY(), '用户在浏览器输入域名→操作系统查本地DNS缓存→向DNS服务器查询→DNS服务器逐级查询(根→顶级域→权威DNS)→返回IP地址→浏览器用IP地址连接目标服务器。', 'DNS把人类友好的域名翻译为机器可用的IP。', 3, 'easy', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '请解释HTTP和HTTPS的区别。', JSON_ARRAY(), 'HTTP: 明文传输，端口80，无加密。HTTPS=HTTP+SSL/TLS: 加密传输，端口443，需要SSL证书，提供数据加密、身份认证、数据完整性保护。', 'HTTPS已成标配，Chrome等浏览器标记HTTP为不安全。', 3, 'easy', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '请解释什么是CDN及其作用。', JSON_ARRAY(), 'CDN(内容分发网络)将内容缓存到全球各地的边缘节点。用户请求时由最近的节点响应，减少延迟、提高访问速度、减轻源站压力、增强抗DDoS能力。', 'CDN是互联网基础设施的重要组成部分。', 3, 'medium', 5.00, 0, 1, NOW(), NOW()),

('short_answer', '请解释进程和线程的区别。', JSON_ARRAY(), '进程是资源分配的基本单位(独立内存空间)，线程是CPU调度的基本单位(共享进程内存)。进程间通信复杂(IPC)、开销大；线程间共享内存、通信简单但需考虑同步。切换线程比切换进程开销小。', '进程和线程是多任务操作系统的核心概念。', 4, 'easy', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '什么是死锁？请说明死锁的四个必要条件和预防方法。', JSON_ARRAY(), '死锁: 多个进程因争夺资源而相互等待，无法继续执行。四条件: 互斥、请求保持、不可剥夺、循环等待。预防: 破坏任一条件，如资源有序分配破坏循环等待，或一次性分配所需所有资源。', '死锁是多进程编程必须处理的经典问题。', 4, 'medium', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '请解释虚拟内存的工作原理。', JSON_ARRAY(), '操作系统将硬盘空间映射到内存地址空间，当程序访问不在物理内存中的页面时触发缺页中断，将所需页面从硬盘换入内存(同时可能换出不常用页面)。程序可见的地址空间可远大于实际物理内存。', '虚拟内存是现代操作系统的关键特性。', 4, 'medium', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '请解释互斥锁(Mutex)和信号量(Semaphore)的区别。', JSON_ARRAY(), '互斥锁: 只有锁定和非锁定两种状态，同一时间只有一个线程能持有。信号量: 有一个整型计数器，允许多个线程同时访问(计数器>0可进入)。互斥锁可看作初始值为1的二元信号量。', '两者都是常用的线程同步原语。', 4, 'medium', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '简述操作系统的主要功能。', JSON_ARRAY(), '五大功能: 1.进程管理(创建/调度/终止进程)；2.内存管理(分配/回收/虚拟内存)；3.文件管理(文件系统/目录/权限)；4.设备管理(驱动程序/I/O控制)；5.用户接口(命令行/图形界面/API)。', '操作系统是硬件和应用程序之间的桥梁。', 4, 'easy', 5.00, 0, 1, NOW(), NOW()),

('short_answer', '请解释数据库事务的ACID特性。', JSON_ARRAY(), '原子性(A): 事务中的操作要么全部成功要么全部回滚。一致性(C): 事务前后数据库保持一致状态。隔离性(I): 并发事务之间互不干扰，如同串行执行。持久性(D): 提交的事务结果永久保存不丢失。', 'ACID是数据库保证数据可靠性的核心机制。', 5, 'easy', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '请解释数据库索引的作用和原理。', JSON_ARRAY(), '索引类似书的目录，通过B+树等数据结构快速定位数据行。原理: 对索引列建立有序结构，查询时通过二分查找定位，避免全表扫描。代价: 占用额外空间，增删改需维护索引。', '索引是最常用的数据库性能优化手段。', 5, 'easy', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '请解释SQL注入攻击的原理和防范方法。', JSON_ARRAY(), '攻击者通过拼接恶意SQL片段到用户输入中，修改原SQL语义，如 admin OR 1=1 绕过登录。防范: 1.参数化查询/预编译语句 2.ORM框架(自动转义) 3.输入校验和过滤 4.最小权限原则 5.错误信息不暴露数据库细节。', 'SQL注入是OWASP十大安全威胁之一。', 5, 'medium', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '请解释INNER JOIN和LEFT JOIN的区别。', JSON_ARRAY(), 'INNER JOIN: 返回两表匹配的行(取交集)。LEFT JOIN: 返回左表所有行，右表没有匹配的填NULL。RIGHT JOIN: 返回右表所有行。FULL JOIN: 返回两表所有行。', 'JOIN类型选择取决于业务需要保留哪边的数据。', 5, 'easy', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '请解释数据库三范式的概念。', JSON_ARRAY(), '1NF: 每列不可再分(原子性)。2NF: 满足1NF且非主键列完全依赖于主键(消除部分依赖)。3NF: 满足2NF且非主键列不依赖于其他非主键列(消除传递依赖)。范式越高冗余越少但查询可能越复杂。', '数据库设计通常做到3NF即可满足大部分需求。', 5, 'medium', 5.00, 0, 1, NOW(), NOW()),

('short_answer', '请简述敏捷开发和传统瀑布模型的区别。', JSON_ARRAY(), '瀑布: 顺序执行(需求→设计→编码→测试→维护)，文档驱动，变更成本高。敏捷: 迭代增量(短周期冲刺)，持续交付可工作软件，拥抱变化，注重沟通和反馈。', '敏捷不是不要文档和计划，而是更灵活地响应变化。', 6, 'easy', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '请解释Git的工作流程(工作区→暂存区→本地仓库→远程仓库)。', JSON_ARRAY(), '1.git add: 工作区修改→暂存区。2.git commit: 暂存区→本地仓库。3.git push: 本地仓库→远程仓库。4.git pull: 远程仓库→本地仓库+工作区。', '理解Git的三个区域是正确使用Git的基础。', 6, 'easy', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '什么是单元测试？为什么要写单元测试？', JSON_ARRAY(), '单元测试是测试代码中最小单元(通常是函数/方法)的正确性。优势: 1.及早发现bug 2.放心重构代码 3.文档作用(测试即规格) 4.回归测试自动化 5.提高代码质量(可测试的代码通常设计更好)。', '测试驱动开发(TDD)是先写测试再写代码。', 6, 'medium', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '请解释什么是持续集成(CI)和持续部署(CD)。', JSON_ARRAY(), 'CI(持续集成): 代码提交后自动构建+测试，快速发现集成问题。CD(持续部署/交付): CI通过后自动部署到测试/生产环境。工具: Jenkins/GitHub Actions/GitLab CI。', 'CI/CD是现代DevOps实践的核心。', 6, 'medium', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '请解释SOLID原则，至少说明其中三个。', JSON_ARRAY(), 'S单一职责: 一个类只负责一件事。O开闭: 对扩展开放，对修改关闭。L里氏替换: 子类可以替换父类。I接口隔离: 不应强迫实现不需要的接口。D依赖倒置: 依赖抽象而非具体实现。', 'SOLID是面向对象设计的五大基本原则。', 6, 'hard', 6.00, 0, 1, NOW(), NOW()),

('short_answer', '请解释面向对象编程的三大特征: 封装、继承、多态。', JSON_ARRAY(), '封装: 隐藏内部实现，通过公开接口交互(private+getter/setter)。继承: 子类复用父类的属性和方法(extends)。多态: 同一接口不同实现，如不同子类重写同一方法表现不同行为。', '三大特征是OOP区别于过程式编程的核心。', 7, 'easy', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '请解释接口(Interface)和抽象类(Abstract Class)的区别。', JSON_ARRAY(), '接口: 只定义方法签名(无实现)，可多实现(const implements A,B)，不能有构造方法。抽象类: 可以有实现方法，只能单继承(extends)，可以有构造方法。接口定义"能做什么"，抽象类定义"是什么"。', 'Java8+接口可以有default方法，但仍不能有实例字段。', 7, 'medium', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '什么是异常处理？请解释try-catch-finally的执行流程。', JSON_ARRAY(), '异常处理是捕获和处理程序运行时错误(如除以零、文件不存在)的机制。流程: 执行try块→若有异常匹配catch块→执行对应catch(如无匹配向上抛出)→无论有无异常都执行finally块(常用于关闭资源)。', 'finally在return之前执行(除System.exit())。', 7, 'easy', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '请解释什么是设计模式以及为什么需要设计模式。', JSON_ARRAY(), '设计模式是软件开发中经过验证的可复用解决方案模板。好处: 1.复用成熟方案，降低出错 2.提供通用词汇，便于团队沟通 3.提高代码可维护性和扩展性 4.体现面向对象设计原则。', 'GoF的23种设计模式是最经典的参考。', 7, 'medium', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '请解释强类型语言和弱类型语言的区别，并举例。', JSON_ARRAY(), '强类型(类型安全): 变量类型固定，不能隐式转换不兼容类型，在编译时检查。如Java、C++、Rust。弱类型: 变量类型可被自动转换，在运行时确定。如JavaScript、PHP。Python是强类型但动态的(变量可以改变类型但操作时检查)。', '类型系统是编程语言设计的重要维度。', 7, 'medium', 5.00, 0, 1, NOW(), NOW()),

('short_answer', '请说明数组排序中稳定排序和不稳定排序的区��，并各举两个例子。', JSON_ARRAY(), '稳定排序: 相等元素的相对位置在排序后不变。例: 冒泡排序、归并排序、插入排序。不稳定排序: 相等元素的相对位置可能改变。例: 快速排序、堆排序、选择排序。', '当按多个关键字排序时，稳定性很重要。', 2, 'medium', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '请简述TCP流量控制和拥塞控制的基本思想。', JSON_ARRAY(), '流量控制: 通过滑动窗口让发送方根据接收方的处理能力调整发送速率(防止接收方溢出)。拥塞控制: 通过慢启动、拥塞避免、快重传、快恢复等算法，根据网络状况调整发送速率(防止网络过载)。', '流量控制是端到端的，拥塞控制是全局的。', 3, 'hard', 6.00, 0, 1, NOW(), NOW()),
('short_answer', '请解释HTTPS的SSL/TLS握手过程。', JSON_ARRAY(), '1.客户端发送支持的加密算法列表+随机数。2.服务端选择算法+发送证书+随机数。3.客户端验证证书，生成预主密钥用公钥加密发送。4.双方用三个随机数生成会话密钥。5.后续通信用会话密钥对称加密。', '混合使用非对称加密(握手阶段)和对称加密(数据传输)。', 3, 'hard', 6.00, 0, 1, NOW(), NOW()),
('short_answer', '请说明数据库连接池的工作原理和配置参数。', JSON_ARRAY(), '连接池预先创建一组数据库连接并维护。请求时从池中获取连接(不需创建)，用完归还(不需关闭)。配置: 最小连接数(保证响应速度)、最大连接数(防止连接过多)、超时时间、空闲回收。', '连接池大幅减少了频繁创建/销毁连接的开销。', 5, 'medium', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '请解释什么是缓存穿透、缓存击穿和缓存雪崩，以及各自的解决方案。', JSON_ARRAY(), '缓存穿透: 查不存在的数据，绕过缓存直达DB→解决方法: 布隆过滤器/缓存空值。缓存击穿: 热点key过期瞬间大量请求→解决方法: 互斥锁/永不过期。缓存雪崩: 大量key同时过期→解决方法: 随机过期时间/多级缓存/限流。', '这三个问题是缓存架构中的经典难题。', 5, 'hard', 6.00, 0, 1, NOW(), NOW()),

('short_answer', '请简述进程调度中抢占式和非抢占式的区别。', JSON_ARRAY(), '非抢占式: 进程获得CPU后一直运行直到主动让出(完成/阻塞)，简单但响应差(批处理)。抢占式: 操作系统可以在时间片用完或高优先级进程就绪时强制切换CPU，响应及时(现代OS)。', '所有现代通用操作系统都使用抢占式调度。', 4, 'medium', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '请解释软件工程中的"技术债"概念。', JSON_ARRAY(), '技术债指为了快速交付而采取的捷径(如跳过重构、不写测试)在长期会导致代码质量下降、维护成本上升。如同金融债务，需要定期"偿还"(重构、补充测试)否则会产生"利息"(越来越难改)。', '适度技术债是战略选择，但需有偿还计划。', 6, 'medium', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '请解释RESTful API的设计原则，并说明什么是"无状态"。', JSON_ARRAY(), 'RESTful原则: 1.资源用URL标识 2.使用HTTP方法语义(GET/POST/PUT/DELETE) 3.无状态(每个请求包含所有需要的信息，服务器不保存客户端状态) 4.统一接口 5.响应可缓存。无状态让服务易于水平扩展。', '无状态是REST最核心的原则。', 6, 'medium', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '请简述抽象类和接口在Java中的具体区别和选择场景。', JSON_ARRAY(), '抽象类可以有构造方法、成员变量、已实现方法、只能单继承；接口只能有常量和抽象方法(Java8+可有default/static方法)、可多实现。选择: is-a关系用抽象类(如Animal→Dog)，can-do能力用接口(如Runnable、Comparable)。', '组合优于继承，优先考虑接口。', 7, 'medium', 5.00, 0, 1, NOW(), NOW()),
('short_answer', '请简述软件设计中的"高内聚、低耦合"原则。', JSON_ARRAY(), '高内聚: 模块内部功能紧密相关，职责单一明确。低耦合: 模块之间依赖关系弱，一个模块的变化不影响或少影响其他模块。实现方法: 接口隔离、依赖注入、事件驱动等。好处: 易维护、可测试、可复用。', '这是评价软件设计质量的核心标准。', 7, 'medium', 5.00, 0, 1, NOW(), NOW());

-- ============================================
-- 完成! 导入成功后可用以下命令验证:
-- SELECT question_type, COUNT(*) FROM questions GROUP BY question_type;
-- ============================================
