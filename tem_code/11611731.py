import numpy as np
import random

COLOR_BLACK=-1
COLOR_WHITE=1
COLOR_NONE=0
random.seed(0)



#don't change the class name
class AI(object):
#chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
#You are white or black
        global COLOR_BLACK
        global COLOR_WHITE
        self.color = color
        if self.color==COLOR_BLACK:
            COLOR_BLACK = -1
            COLOR_WHITE = 1
        else:
            COLOR_BLACK=1
            COLOR_WHITE =-1


 #the max time you should use, your algorithm's run time must not exceed the timelimit.
        self.time_out = time_out
 # You need add your decision into your candidate_list. System will get the end ofyour candidate_list as your decision .
        self.candidate_list = []


 # The input is current chessboard.
    def go(self, chessboard):

        valueboard=np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)



 # Clear candidate_list
        self.candidate_list.clear()
 #==================================================================
 #Write your algorithm here
 #Here is the simplest sample:Random decision





        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1])) #以上2行获取空的位置


        #pos_idx = random.randint((len(idx) - 1), (len(idx) - 1)/2)


        pos_idx = random.randint(0, len(idx) - 1)
        new_pos = idx[pos_idx]
        self.candidate_list.append(new_pos)#最最最开始随便空位置下一个
        print("随")
        print(self.candidate_list[0][0], self.candidate_list[0][1])


        o=(self.chessboard_size//2,self.chessboard_size//2)

        if chessboard[o[0]][o[1]]==0:

            valueboard[o[0]][o[1]]+=0.1

            self.candidate_list.pop()
            self.candidate_list.append(o)









 #==============Find new pos========================================


        idx2 = np.where(chessboard == COLOR_WHITE)#得到敌人的点
        idx2 = list(zip(idx2[0], idx2[1]))

        idx3 = np.where(chessboard == COLOR_BLACK)#得到自己的点
        idx3 = list(zip(idx3[0], idx3[1]))
        print("白")
        print(idx2)
        print("空")
        print(idx)
        for i in idx2:#扫描敌人棋子

            x=i[0]
            y=i[1]



            #一个子也堵 1分  应该包装起来 但我懒得写

            a = (x + 1, y)
            b = (x - 1, y)
            d = (x,y+1)
            e = (x,y-1)#怕弄混 不用c和i这两个字母

            f=(x-1,y-1)

            g=(x+1,y-1)
            h=(x+1,y+1)
            j=(x-1,y+1)


            if sizeok(a[0],a[0],self.chessboard_size) and chessboard[a[0]][a[1]]==0:
                valueboard[a[0]][a[1]] += 1



                bijiao(a,self.candidate_list,valueboard)
                c = self.candidate_list[0]
                if valueboard[a[0]][a[1]] > valueboard[c[0]][c[1]]:
                    self.candidate_list.pop()
                    self.candidate_list.append(a)

            if sizeok(b[0], b[1], self.chessboard_size) and chessboard[b[0]][b[1]] == 0:
                valueboard[b[0]][b[1]] += 1
                c = self.candidate_list[0]
                if valueboard[b[0]][b[1]] > valueboard[c[0]][c[1]]:
                    self.candidate_list.pop()
                    self.candidate_list.append(b)

            if sizeok(d[0], d[1], self.chessboard_size) and chessboard[d[0]][d[1]] == 0:
                valueboard[d[0]][d[1]] += 1
                c = self.candidate_list[0]
                if valueboard[d[0]][d[1]] > valueboard[c[0]][c[1]]:
                    self.candidate_list.pop()
                    self.candidate_list.append(d)


            if sizeok(e[0], e[1], self.chessboard_size) and chessboard[e[0]][e[1]] == 0:
                valueboard[e[0]][e[1]] += 1
                c = self.candidate_list[0]
                if valueboard[e[0]][e[1]] > valueboard[c[0]][c[1]]:
                    self.candidate_list.pop()
                    self.candidate_list.append(e)

                if sizeok(f[0], f[0], self.chessboard_size) and chessboard[f[0]][f[1]] == 0:
                    valueboard[f[0]][f[1]] += 1
                    c = self.candidate_list[0]
                    if valueboard[f[0]][f[1]] > valueboard[c[0]][c[1]]:
                        self.candidate_list.pop()
                        self.candidate_list.append(f)

                if sizeok(g[0], g[1], self.chessboard_size) and chessboard[g[0]][g[1]] == 0:
                    valueboard[g[0]][g[1]] += 1
                    c = self.candidate_list[0]
                    if valueboard[g[0]][g[1]] > valueboard[c[0]][c[1]]:
                        self.candidate_list.pop()
                        self.candidate_list.append(g)

                if sizeok(h[0], h[1], self.chessboard_size) and chessboard[h[0]][h[1]] == 0:
                    valueboard[h[0]][h[1]] += 1
                    c = self.candidate_list[0]
                    if valueboard[h[0]][h[1]] > valueboard[c[0]][c[1]]:
                        self.candidate_list.pop()
                        self.candidate_list.append(h)


                if sizeok(j[0], j[1], self.chessboard_size) and chessboard[j[0]][j[1]] == 0:
                    valueboard[j[0]][j[1]] += 1
                    c = self.candidate_list[0]
                    if valueboard[j[0]][j[1]] > valueboard[c[0]][c[1]]:
                        self.candidate_list.pop()
                        self.candidate_list.append(j)







                if sizeok(x - 1, y - 1, self.chessboard_size) and chessboard[x - 1][y - 1] == COLOR_WHITE:  # 左下是白
                    if sizeok(x + 1, y + 1, self.chessboard_size) and chessboard[x + 1][y + 1] == COLOR_WHITE:  # 右上是白
                        a = (x - 2, y - 2)
                        b = (x + 2, y + 2)
                        if sizeok(a[0], a[1], self.chessboard_size) and chessboard[a[0]][a[1]] == 0:
                            valueboard[a[0]][a[1]] += 30
                            c = self.candidate_list[0]
                            if valueboard[a[0]][a[1]] > valueboard[c[0]][c[1]]:
                                self.candidate_list.pop()
                                self.candidate_list.append(a)
                                print("list变了9")
                        if sizeok(b[0], b[1], self.chessboard_size) and chessboard[b[0]][b[1]] == 0:
                            valueboard[b[0]][b[1]] += 30
                            c = self.candidate_list[0]
                            if valueboard[b[0]][b[1]] > valueboard[c[0]][c[1]]:
                                self.candidate_list.pop()
                                self.candidate_list.append(b)
                                print("list变了10")



            #   /型单二 10分
            print("走到这了1")
            if x + 1 >= 0 and y + 1 >= 0 and x+1<=self.chessboard_size-1 and y+1<= self.chessboard_size-1\
                    and chessboard[x + 1][y + 1] == COLOR_WHITE:#右上是敌人
                a = (x + 2, y + 2)
                b = (x - 1, y - 1)
                if a[0] >= 0 and a[1] >= 0 and a[0]<=self.chessboard_size-1 \
                        and a[1]<=self.chessboard_size-1 and chessboard[a[0]][a[1]] == 0:
                    valueboard[a[0]][a[1]] += 10
                    c= self.candidate_list[0]
                    if valueboard[a[0]][a[1]]>valueboard[c[0]][c[1]]:
                        self.candidate_list.pop()
                        self.candidate_list.append(a)
                        print("list变了1")

                if b[0] >= 0 and b[1] >= 0 and b[0] <= self.chessboard_size-1 \
                        and b[1] <= self.chessboard_size-1 and chessboard[b[0]][b[1]] == 0:
                    valueboard[b[0]][b[1]] += 10
                    c = self.candidate_list[0]
                    if valueboard[b[0]][b[1]] > valueboard[c[0]][c[1]]:
                        self.candidate_list.pop()
                        self.candidate_list.append(b)
                        print("list变了2")
            #   \型单二 10分
            print("走到这了2")
            if x - 1 >= 0 and y + 1 >= 0 and x-1 <=self.chessboard_size-1 and y+1 <=self.chessboard_size-1 \
                    and chessboard[x - 1][y + 1] == COLOR_WHITE:#左上是敌人
                a = (x - 2, y + 2)
                b = (x + 1, y - 1)
                if a[0] >= 0 and a[1] >= 0 and a[0] <= self.chessboard_size-1 \
                        and a[1] <= self.chessboard_size-1 and chessboard[a[0]][a[1]] == 0:
                    valueboard[a[0]][a[1]] += 10
                    c = self.candidate_list[0]
                    if valueboard[a[0]][a[1]] > valueboard[c[0]][c[1]]:
                        self.candidate_list.pop()
                        self.candidate_list.append(a)
                        print("list变了3")
                if b[0] >= 0 and b[1] >= 0 and b[0] <= self.chessboard_size-1 \
                        and b[1] <= self.chessboard_size-1 and chessboard[b[0]][b[1]] == 0:
                    valueboard[b[0]][b[1]] += 10
                    c = self.candidate_list[0]
                    if valueboard[b[0]][b[1]] > valueboard[c[0]][c[1]]:
                        self.candidate_list.pop()
                        self.candidate_list.append(b)
                        print("list变了4")

            #   |型单二 10分
            print("走到这了3")
            if x  >= 0 and y + 1 >= 0 and x<=self.chessboard_size-1 and y+1<=self.chessboard_size-1 \
                    and chessboard[x ][y + 1] == COLOR_WHITE:#上是敌人
                a = (x , y + 2)
                b = (x , y - 1)
                if a[0] >= 0 and a[1] >= 0 and a[0] <= self.chessboard_size-1 \
                        and a[1] <= self.chessboard_size-1 and chessboard[a[0]][a[1]] == 0:
                    valueboard[a[0]][a[1]] += 10
                    c = self.candidate_list[0]
                    if valueboard[a[0]][a[1]] > valueboard[c[0]][c[1]]:
                        self.candidate_list.pop()
                        self.candidate_list.append(a)
                        print("list变了5")
                if b[0] >= 0 and b[1] >= 0 and b[0] <= self.chessboard_size-1 \
                        and b[1] <= self.chessboard_size-1 and chessboard[b[0]][b[1]] == 0:
                    valueboard[b[0]][b[1]] += 10
                    c = self.candidate_list[0]
                    if valueboard[b[0]][b[1]] > valueboard[c[0]][c[1]]:
                        self.candidate_list.pop()
                        self.candidate_list.append(b)
                        print("list变了6")

            #   一型单二 10分
            print("走到这了4")
            if x-1 >= 0 and y >= 0 and chessboard[x-1][y] == COLOR_WHITE:#左是敌人
                a = (x - 2, y)
                b = (x + 1, y)
                if a[0] >= 0 and a[1] >= 0 and a[0] <= self.chessboard_size-1 \
                        and a[1] <= self.chessboard_size-1 and chessboard[a[0]][a[1]] == 0:
                    valueboard[a[0]][a[1]] += 10
                    c = self.candidate_list[0]
                    if valueboard[a[0]][a[1]] > valueboard[c[0]][c[1]]:
                        self.candidate_list.pop()
                        self.candidate_list.append(a)
                        print("list变了7")
                if b[0] >= 0 and b[1] >= 0 and b[0] <= self.chessboard_size-1 \
                        and b[1] <= self.chessboard_size-1 and chessboard[b[0]][b[1]] == 0:
                    valueboard[b[0]][b[1]] += 10
                    c = self.candidate_list[0]
                    if valueboard[b[0]][b[1]] > valueboard[c[0]][c[1]]:
                        self.candidate_list.pop()
                        self.candidate_list.append(b)
                        print("list变了8")

            print("扫描完2个了")

            #   /型单三 30分
            if sizeok(x-1,y-1,self.chessboard_size) and chessboard[x - 1][y - 1] == COLOR_WHITE:  # 左下是白
                if sizeok(x+1,y+1,self.chessboard_size) and chessboard[x + 1][y +1] == COLOR_WHITE:  # 右上是白
                    a = (x - 2, y-2)
                    b = (x + 2, y+2)
                    if sizeok(a[0],a[1],self.chessboard_size)and chessboard[a[0]][a[1]] == 0:
                        if sizeok(b[0],b[1],self.chessboard_size)and chessboard[b[0]][b[1]]==COLOR_BLACK:#眠三
                            valueboard[a[0]][a[1]] +=11
                        elif sizeok(b[0],b[1],self.chessboard_size)and chessboard[b[0]][b[1]]==0 : #不眠的三
                            valueboard[a[0]][a[1]] +=30
                        c = self.candidate_list[0]
                        if valueboard[a[0]][a[1]] > valueboard[c[0]][c[1]]:
                            self.candidate_list.pop()
                            self.candidate_list.append(a)
                            print("list变了9")
                    if sizeok(b[0],b[1],self.chessboard_size) and chessboard[b[0]][b[1]] == 0:
                        if sizeok(a[0],a[1],self.chessboard_size)and chessboard[a[0]][a[1]]==COLOR_BLACK:#眠三
                            valueboard[b[0]][b[1]] +=11
                        elif sizeok(a[0],a[1],self.chessboard_size)and chessboard[a[0]][a[1]]==0 : #不眠的三
                            valueboard[b[0]][b[1]] +=30
                        c = self.candidate_list[0]
                        if valueboard[b[0]][b[1]] > valueboard[c[0]][c[1]]:
                            self.candidate_list.pop()
                            self.candidate_list.append(b)
                            print("list变了10")
            #   \型单三 30分
            if sizeok(x-1,y+1,self.chessboard_size) and chessboard[x - 1][y + 1] == COLOR_WHITE:  # 左上是白
                if sizeok(x+1,y-1,self.chessboard_size) and chessboard[x + 1][y -1] == COLOR_WHITE:  # 右下是白
                    a = (x - 2, y+2)
                    b = (x + 2, y-2)
                    if sizeok(a[0],a[1],self.chessboard_size)and chessboard[a[0]][a[1]] == 0:

                        if sizeok(b[0],b[1],self.chessboard_size)and chessboard[b[0]][b[1]]==COLOR_BLACK:#眠三
                            valueboard[a[0]][a[1]] +=11
                        elif sizeok(b[0],b[1],self.chessboard_size)and chessboard[b[0]][b[1]]==0 : #不眠的三
                            valueboard[a[0]][a[1]] +=30

                        c = self.candidate_list[0]
                        if valueboard[a[0]][a[1]] > valueboard[c[0]][c[1]]:
                            self.candidate_list.pop()
                            self.candidate_list.append(a)
                            print("list变了11")
                    if sizeok(b[0],b[1],self.chessboard_size) and chessboard[b[0]][b[1]] == 0:
                        if sizeok(a[0],a[1],self.chessboard_size)and chessboard[a[0]][a[1]]==COLOR_BLACK:#眠三
                            valueboard[b[0]][b[1]] +=11
                        elif sizeok(a[0],a[1],self.chessboard_size)and chessboard[a[0]][a[1]]==0 : #不眠的三
                            valueboard[b[0]][b[1]] +=30

                        c = self.candidate_list[0]
                        if valueboard[b[0]][b[1]] > valueboard[c[0]][c[1]]:
                            self.candidate_list.pop()
                            self.candidate_list.append(b)
                            print("list变了12")
            #   |型单三 30分
            if sizeok(x,y-1,self.chessboard_size) and chessboard[x][y - 1] == COLOR_WHITE:  # 下是白
                if sizeok(x,y+1,self.chessboard_size) and chessboard[x][y +1] == COLOR_WHITE:  # 上是白
                    a = (x , y-2)
                    b = (x , y+2)
                    if sizeok(a[0],a[1],self.chessboard_size)and chessboard[a[0]][a[1]] == 0:
                        if sizeok(b[0],b[1],self.chessboard_size)and chessboard[b[0]][b[1]]==COLOR_BLACK:#眠三
                            valueboard[a[0]][a[1]] +=11
                        elif sizeok(b[0],b[1],self.chessboard_size)and chessboard[b[0]][b[1]]==0 : #不眠的三
                            valueboard[a[0]][a[1]] +=30




                        c = self.candidate_list[0]
                        if valueboard[a[0]][a[1]] > valueboard[c[0]][c[1]]:
                            self.candidate_list.pop()
                            self.candidate_list.append(a)
                            print("list变了13")
                    if sizeok(b[0],b[1],self.chessboard_size) and chessboard[b[0]][b[1]] == 0:
                        if sizeok(b[0],b[1]+1,self.chessboard_size) and chessboard[b[0]][b[1]+1]==COLOR_WHITE:#一种跳五
                            valueboard[b[0]][b[1]] += 200
                        c = self.candidate_list[0]
                        if valueboard[b[0]][b[1]] > valueboard[c[0]][c[1]]:
                            self.candidate_list.pop()
                            self.candidate_list.append(b)
                            print("终于他妈的有了")
                        if sizeok(a[0],a[1],self.chessboard_size)and chessboard[a[0]][a[1]]==COLOR_BLACK:#眠三
                            valueboard[b[0]][b[1]] +=11
                        elif sizeok(a[0],a[1],self.chessboard_size)and chessboard[a[0]][a[1]]==0 : #不眠的三
                            valueboard[b[0]][b[1]] +=30

                        c = self.candidate_list[0]
                        if valueboard[b[0]][b[1]] > valueboard[c[0]][c[1]]:
                            self.candidate_list.pop()
                            self.candidate_list.append(b)
                            print("list变了14")


            #   一型单三 30分
            if sizeok(x-1,y,self.chessboard_size) and chessboard[x - 1][y ] == COLOR_WHITE:  # 左是白
                if sizeok(x+1,y,self.chessboard_size) and chessboard[x + 1][y] == COLOR_WHITE:  # 右是白
                    a = (x - 2, y)
                    b = (x + 2, y)
                    if sizeok(a[0],a[1],self.chessboard_size)and chessboard[a[0]][a[1]] == 0:

                        if sizeok(b[0],b[1],self.chessboard_size)and chessboard[b[0]][b[1]]==COLOR_BLACK:#眠三
                            valueboard[a[0]][a[1]] +=11
                        elif sizeok(b[0],b[1],self.chessboard_size)and chessboard[b[0]][b[1]]==0 : #不眠的三
                            valueboard[a[0]][a[1]] +=30

                        c = self.candidate_list[0]
                        if valueboard[a[0]][a[1]] > valueboard[c[0]][c[1]]:
                            self.candidate_list.pop()
                            self.candidate_list.append(a)
                            print("list变了15")
                    if sizeok(b[0],b[1],self.chessboard_size) and chessboard[b[0]][b[1]] == 0:
                        if sizeok(b[0]+1,b[1],self.chessboard_size) and chessboard[b[0]+1][b[1]]==COLOR_WHITE:#一种跳五
                            valueboard[b[0]][b[1]] += 200
                        c = self.candidate_list[0]
                        if valueboard[b[0]][b[1]] > valueboard[c[0]][c[1]]:
                            self.candidate_list.pop()
                            self.candidate_list.append(b)



                        if sizeok(a[0],a[1],self.chessboard_size)and chessboard[a[0]][a[1]]==COLOR_BLACK:#眠三
                            valueboard[b[0]][b[1]] +=11
                        elif sizeok(a[0],a[1],self.chessboard_size)and chessboard[a[0]][a[1]]==0 : #不眠的三
                            valueboard[b[0]][b[1]] +=30

                        c = self.candidate_list[0]
                        if valueboard[b[0]][b[1]] > valueboard[c[0]][c[1]]:
                            self.candidate_list.pop()
                            self.candidate_list.append(b)
                            print("list变了16")

            print("单三验证完毕")

            #   /型单四 90分
            if sizeok(x-1,y-1,self.chessboard_size) and chessboard[x - 1][y - 1] == COLOR_WHITE:  # 左下是白
                if sizeok(x+1,y+1,self.chessboard_size) and chessboard[x + 1][y +1] == COLOR_WHITE:  # 右上是白
                    if sizeok(x+2,y+2,self.chessboard_size) and chessboard[x + 2][y +2] == COLOR_WHITE:
                        a = (x - 2, y-2)
                        b = (x + 3, y+3)
                        if sizeok(a[0],a[1],self.chessboard_size)and chessboard[a[0]][a[1]] == 0:
                            valueboard[a[0]][a[1]] +=90
                            c = self.candidate_list[0]
                            if valueboard[a[0]][a[1]] > valueboard[c[0]][c[1]]:
                                self.candidate_list.pop()
                                self.candidate_list.append(a)
                                print("list变了17")
                        if sizeok(b[0],b[1],self.chessboard_size) and chessboard[b[0]][b[1]] == 0:
                            valueboard[b[0]][b[1]] += 90
                            c = self.candidate_list[0]
                            if valueboard[b[0]][b[1]] > valueboard[c[0]][c[1]]:
                                self.candidate_list.pop()
                                self.candidate_list.append(b)
                                print("list变了18")
            #   \型单四 90分
            if sizeok(x+1,y-1,self.chessboard_size) and chessboard[x + 1][y - 1] == COLOR_WHITE:  #
                if sizeok(x-1,y+1,self.chessboard_size) and chessboard[x - 1][y +1] == COLOR_WHITE:  #
                    if sizeok(x-2,y+2,self.chessboard_size) and chessboard[x - 2][y +2] == COLOR_WHITE:
                        a = (x - 3, y+3)
                        b = (x + 2, y-2)
                        if sizeok(a[0],a[1],self.chessboard_size)and chessboard[a[0]][a[1]] == 0:
                            valueboard[a[0]][a[1]] +=90
                            c = self.candidate_list[0]
                            if valueboard[a[0]][a[1]] > valueboard[c[0]][c[1]]:
                                self.candidate_list.pop()
                                self.candidate_list.append(a)
                                print("list变了19")
                        if sizeok(b[0],b[1],self.chessboard_size) and chessboard[b[0]][b[1]] == 0:
                            valueboard[b[0]][b[1]] += 90
                            c = self.candidate_list[0]
                            if valueboard[b[0]][b[1]] > valueboard[c[0]][c[1]]:
                                self.candidate_list.pop()
                                self.candidate_list.append(b)
                                print("list变了20")

            #   |型单四 90分
            if sizeok(x,y-1,self.chessboard_size) and chessboard[x ][y - 1] == COLOR_WHITE:  #
                if sizeok(x,y+1,self.chessboard_size) and chessboard[x][y +1] == COLOR_WHITE:  #
                    if sizeok(x,y+2,self.chessboard_size) and chessboard[x][y +2] == COLOR_WHITE:
                        a = (x , y-2)
                        b = (x , y+3)
                        if sizeok(a[0],a[1],self.chessboard_size)and chessboard[a[0]][a[1]] == 0:
                            valueboard[a[0]][a[1]] +=90
                            c = self.candidate_list[0]
                            if valueboard[a[0]][a[1]] > valueboard[c[0]][c[1]]:
                                self.candidate_list.pop()
                                self.candidate_list.append(a)
                                print("list变了21")
                        if sizeok(b[0],b[1],self.chessboard_size) and chessboard[b[0]][b[1]] == 0:
                            valueboard[b[0]][b[1]] += 90
                            c = self.candidate_list[0]
                            if valueboard[b[0]][b[1]] > valueboard[c[0]][c[1]]:
                                self.candidate_list.pop()
                                self.candidate_list.append(b)
                                print("list变了22")
            #   一型单四 90分
            if sizeok(x-1,y,self.chessboard_size) and chessboard[x - 1][y ] == COLOR_WHITE:  #
                if sizeok(x+1,y,self.chessboard_size) and chessboard[x + 1][y] == COLOR_WHITE:  #
                    if sizeok(x+2,y,self.chessboard_size) and chessboard[x + 2][y ] == COLOR_WHITE:
                        a = (x - 2, y)
                        b = (x + 3, y)
                        if sizeok(a[0],a[1],self.chessboard_size)and chessboard[a[0]][a[1]] == 0:
                            valueboard[a[0]][a[1]] +=90
                            c = self.candidate_list[0]
                            if valueboard[a[0]][a[1]] > valueboard[c[0]][c[1]]:
                                self.candidate_list.pop()
                                self.candidate_list.append(a)
                                print("list变了23")
                        if sizeok(b[0],b[1],self.chessboard_size) and chessboard[b[0]][b[1]] == 0:
                            valueboard[b[0]][b[1]] += 90
                            c = self.candidate_list[0]
                            if valueboard[b[0]][b[1]] > valueboard[c[0]][c[1]]:
                                self.candidate_list.pop()
                                self.candidate_list.append(b)
                                print("list变了24")



            print("扫描完单4了")
            print("扫描完敌人了")
        for i in idx3:#扫描自己棋子

            x = i[0]
            y = i[1]
            #   自己/型单四 1000分
            if sizeok(x-1,y-1,self.chessboard_size) and chessboard[x - 1][y - 1] == COLOR_BLACK:  # 左下是白
                if sizeok(x+1,y+1,self.chessboard_size) and chessboard[x + 1][y +1] == COLOR_BLACK:  # 右上是白
                    if sizeok(x+2,y+2,self.chessboard_size) and chessboard[x + 2][y +2] == COLOR_BLACK:
                        a = (x - 2, y-2)
                        b = (x + 3, y+3)
                        if sizeok(a[0],a[1],self.chessboard_size)and chessboard[a[0]][a[1]] == 0:
                            valueboard[a[0]][a[1]] +=1000
                            c = self.candidate_list[0]
                            if valueboard[a[0]][a[1]] > valueboard[c[0]][c[1]]:
                                self.candidate_list.pop()
                                self.candidate_list.append(a)
                                print("list变了25")
                        if sizeok(b[0],b[1],self.chessboard_size) and chessboard[b[0]][b[1]] == 0:
                            valueboard[b[0]][b[1]] += 1000
                            c = self.candidate_list[0]
                            if valueboard[b[0]][b[1]] > valueboard[c[0]][c[1]]:
                                self.candidate_list.pop()
                                self.candidate_list.append(b)
                                print("list变了26")
            #   自己\型单四 1000分
            if sizeok(x+1,y-1,self.chessboard_size) and chessboard[x + 1][y - 1] == COLOR_BLACK:  #
                if sizeok(x-1,y+1,self.chessboard_size) and chessboard[x - 1][y +1] == COLOR_BLACK:  #
                    if sizeok(x-2,y+2,self.chessboard_size) and chessboard[x - 2][y +2] == COLOR_BLACK:
                        a = (x - 3, y+3)
                        b = (x + 2, y-2)
                        if sizeok(a[0],a[1],self.chessboard_size)and chessboard[a[0]][a[1]] == 0:
                            valueboard[a[0]][a[1]] +=1000
                            c = self.candidate_list[0]
                            if valueboard[a[0]][a[1]] > valueboard[c[0]][c[1]]:
                                self.candidate_list.pop()
                                self.candidate_list.append(a)
                                print("list变了27")
                        if sizeok(b[0],b[1],self.chessboard_size) and chessboard[b[0]][b[1]] == 0:
                            valueboard[b[0]][b[1]] += 1000
                            c = self.candidate_list[0]
                            if valueboard[b[0]][b[1]] > valueboard[c[0]][c[1]]:
                                self.candidate_list.pop()
                                self.candidate_list.append(b)
                                print("list变了28")

            #   自己|型单四 1000分
            if sizeok(x,y-1,self.chessboard_size) and chessboard[x ][y - 1] == COLOR_BLACK:  #
                if sizeok(x,y+1,self.chessboard_size) and chessboard[x][y +1] == COLOR_BLACK:  #
                    if sizeok(x,y+2,self.chessboard_size) and chessboard[x][y +2] == COLOR_BLACK:
                        a = (x , y-2)
                        b = (x , y+3)
                        if sizeok(a[0],a[1],self.chessboard_size)and chessboard[a[0]][a[1]] == 0:
                            valueboard[a[0]][a[1]] +=1000
                            c = self.candidate_list[0]
                            if valueboard[a[0]][a[1]] > valueboard[c[0]][c[1]]:
                                self.candidate_list.pop()
                                self.candidate_list.append(a)
                                print("list变了29")
                        if sizeok(b[0],b[1],self.chessboard_size) and chessboard[b[0]][b[1]] == 0:
                            valueboard[b[0]][b[1]] += 1000
                            c = self.candidate_list[0]
                            if valueboard[b[0]][b[1]] > valueboard[c[0]][c[1]]:
                                self.candidate_list.pop()
                                self.candidate_list.append(b)
                                print("list变了30")
            #   自己一型单四 1000分
            if sizeok(x-1,y,self.chessboard_size) and chessboard[x - 1][y ] == COLOR_BLACK:  #
                if sizeok(x+1,y,self.chessboard_size) and chessboard[x + 1][y] == COLOR_BLACK:  #
                    if sizeok(x+2,y,self.chessboard_size) and chessboard[x + 2][y ] == COLOR_BLACK:
                        a = (x - 2, y)
                        b = (x + 3, y)
                        if sizeok(a[0],a[1],self.chessboard_size)and chessboard[a[0]][a[1]] == 0:
                            valueboard[a[0]][a[1]] +=1000
                            c = self.candidate_list[0]
                            if valueboard[a[0]][a[1]] > valueboard[c[0]][c[1]]:
                                self.candidate_list.pop()
                                self.candidate_list.append(a)
                                print("list变了31")
                        if sizeok(b[0],b[1],self.chessboard_size) and chessboard[b[0]][b[1]] == 0:
                            valueboard[b[0]][b[1]] += 1000
                            c = self.candidate_list[0]
                            if valueboard[b[0]][b[1]] > valueboard[c[0]][c[1]]:
                                self.candidate_list.pop()
                                self.candidate_list.append(b)
                                print("list变了32")


            #   /型单三 50分
            if sizeok(x-1,y-1,self.chessboard_size) and chessboard[x - 1][y - 1] == COLOR_BLACK:  # 左下是白
                if sizeok(x+1,y+1,self.chessboard_size) and chessboard[x + 1][y +1] == COLOR_BLACK:  # 右上是白
                    a = (x - 2, y-2)
                    b = (x + 2, y+2)
                    if sizeok(a[0],a[1],self.chessboard_size)and chessboard[a[0]][a[1]] == 0:
                        valueboard[a[0]][a[1]] +=50
                        c = self.candidate_list[0]
                        if valueboard[a[0]][a[1]] > valueboard[c[0]][c[1]]:
                            self.candidate_list.pop()
                            self.candidate_list.append(a)
                            print("list变了9")
                    if sizeok(b[0],b[1],self.chessboard_size) and chessboard[b[0]][b[1]] == 0:
                        valueboard[b[0]][b[1]] += 50
                        c = self.candidate_list[0]
                        if valueboard[b[0]][b[1]] > valueboard[c[0]][c[1]]:
                            self.candidate_list.pop()
                            self.candidate_list.append(b)
                            print("list变了10")
            #   \型单三 30分
            if sizeok(x-1,y+1,self.chessboard_size) and chessboard[x - 1][y + 1] == COLOR_BLACK:  # 左上是白
                if sizeok(x+1,y-1,self.chessboard_size) and chessboard[x + 1][y -1] == COLOR_BLACK:  # 右下是白
                    a = (x - 2, y+2)
                    b = (x + 2, y-2)
                    if sizeok(a[0],a[1],self.chessboard_size)and chessboard[a[0]][a[1]] == 0:
                        valueboard[a[0]][a[1]] +=50
                        c = self.candidate_list[0]
                        if valueboard[a[0]][a[1]] > valueboard[c[0]][c[1]]:
                            self.candidate_list.pop()
                            self.candidate_list.append(a)
                            print("list变了11")
                    if sizeok(b[0],b[1],self.chessboard_size) and chessboard[b[0]][b[1]] == 0:
                        valueboard[b[0]][b[1]] += 50
                        c = self.candidate_list[0]
                        if valueboard[b[0]][b[1]] > valueboard[c[0]][c[1]]:
                            self.candidate_list.pop()
                            self.candidate_list.append(b)
                            print("list变了12")
            #   |型单三 30分
            if sizeok(x,y-1,self.chessboard_size) and chessboard[x][y - 1] == COLOR_BLACK:  # 下是白
                if sizeok(x,y+1,self.chessboard_size) and chessboard[x][y +1] == COLOR_BLACK:  # 上是白
                    a = (x , y-2)
                    b = (x , y+2)
                    if sizeok(a[0],a[1],self.chessboard_size)and chessboard[a[0]][a[1]] == 0:
                        valueboard[a[0]][a[1]] +=50
                        c = self.candidate_list[0]
                        if valueboard[a[0]][a[1]] > valueboard[c[0]][c[1]]:
                            self.candidate_list.pop()
                            self.candidate_list.append(a)
                            print("list变了13")
                    if sizeok(b[0],b[1],self.chessboard_size) and chessboard[b[0]][b[1]] == 0:
                        valueboard[b[0]][b[1]] += 50
                        c = self.candidate_list[0]
                        if valueboard[b[0]][b[1]] > valueboard[c[0]][c[1]]:
                            self.candidate_list.pop()
                            self.candidate_list.append(b)
                            print("list变了14")


            #   一型单三 30分
            if sizeok(x-1,y,self.chessboard_size) and chessboard[x - 1][y ] == COLOR_BLACK:  # 左是白
                if sizeok(x+1,y,self.chessboard_size) and chessboard[x + 1][y] == COLOR_BLACK:  # 右是白
                    a = (x - 2, y)
                    b = (x + 2, y)
                    if sizeok(a[0],a[1],self.chessboard_size)and chessboard[a[0]][a[1]] == 0:
                        valueboard[a[0]][a[1]] +=50
                        c = self.candidate_list[0]
                        if valueboard[a[0]][a[1]] > valueboard[c[0]][c[1]]:
                            self.candidate_list.pop()
                            self.candidate_list.append(a)
                            print("list变了15")
                    if sizeok(b[0],b[1],self.chessboard_size) and chessboard[b[0]][b[1]] == 0:
                        valueboard[b[0]][b[1]] += 50
                        c = self.candidate_list[0]
                        if valueboard[b[0]][b[1]] > valueboard[c[0]][c[1]]:
                            self.candidate_list.pop()
                            self.candidate_list.append(b)
                            print("list变了16")


                                
                                
            #   自己/型单二 12分
            
            if x + 1 >= 0 and y + 1 >= 0 and x+1<=self.chessboard_size-1 and y+1<= self.chessboard_size-1\
                    and chessboard[x + 1][y + 1] == COLOR_BLACK:#右上是自己
                a = (x + 2, y + 2)
                b = (x - 1, y - 1)
                if a[0] >= 0 and a[1] >= 0 and a[0]<=self.chessboard_size-1 \
                        and a[1]<=self.chessboard_size-1 and chessboard[a[0]][a[1]] == 0:
                    valueboard[a[0]][a[1]] += 12
                    c= self.candidate_list[0]
                    if valueboard[a[0]][a[1]]>valueboard[c[0]][c[1]]:
                        self.candidate_list.pop()
                        self.candidate_list.append(a)
                        print("list变了33")

                if b[0] >= 0 and b[1] >= 0 and b[0] <= self.chessboard_size-1 \
                        and b[1] <= self.chessboard_size-1 and chessboard[b[0]][b[1]] == 0:
                    valueboard[b[0]][b[1]] += 12
                    c = self.candidate_list[0]
                    if valueboard[b[0]][b[1]] > valueboard[c[0]][c[1]]:
                        self.candidate_list.pop()
                        self.candidate_list.append(b)
                        print("list变了34")
            #   自己\型单二 12分
            
            if x - 1 >= 0 and y + 1 >= 0 and x-1 <=self.chessboard_size-1 and y+1 <=self.chessboard_size-1 \
                    and chessboard[x - 1][y + 1] == COLOR_BLACK:#左上是自己
                a = (x - 2, y + 2)
                b = (x + 1, y - 1)
                if a[0] >= 0 and a[1] >= 0 and a[0] <= self.chessboard_size-1 \
                        and a[1] <= self.chessboard_size-1 and chessboard[a[0]][a[1]] == 0:
                    valueboard[a[0]][a[1]] += 12
                    c = self.candidate_list[0]
                    if valueboard[a[0]][a[1]] > valueboard[c[0]][c[1]]:
                        self.candidate_list.pop()
                        self.candidate_list.append(a)
                        print("list变了35")
                if b[0] >= 0 and b[1] >= 0 and b[0] <= self.chessboard_size-1 \
                        and b[1] <= self.chessboard_size-1 and chessboard[b[0]][b[1]] == 0:
                    valueboard[b[0]][b[1]] += 12
                    c = self.candidate_list[0]
                    if valueboard[b[0]][b[1]] > valueboard[c[0]][c[1]]:
                        self.candidate_list.pop()
                        self.candidate_list.append(b)
                        print("list变了36")

            #   自己|型单二 12分
            print("走到这了3")
            if x  >= 0 and y + 1 >= 0 and x<=self.chessboard_size-1 and y+1<=self.chessboard_size-1 \
                    and chessboard[x ][y + 1] == COLOR_BLACK:#上是自己
                a = (x , y + 2)
                b = (x , y - 1)
                if a[0] >= 0 and a[1] >= 0 and a[0] <= self.chessboard_size-1 \
                        and a[1] <= self.chessboard_size-1 and chessboard[a[0]][a[1]] == 0:
                    valueboard[a[0]][a[1]] += 12
                    c = self.candidate_list[0]
                    if valueboard[a[0]][a[1]] > valueboard[c[0]][c[1]]:
                        self.candidate_list.pop()
                        self.candidate_list.append(a)
                        print("list变了37")
                if b[0] >= 0 and b[1] >= 0 and b[0] <= self.chessboard_size-1 \
                        and b[1] <= self.chessboard_size-1 and chessboard[b[0]][b[1]] == 0:
                    valueboard[b[0]][b[1]] += 12
                    c = self.candidate_list[0]
                    if valueboard[b[0]][b[1]] > valueboard[c[0]][c[1]]:
                        self.candidate_list.pop()
                        self.candidate_list.append(b)
                        print("list变了38")

            #   自己一型单二 12分
            print("走到这了4")
            if x-1 >= 0 and y >= 0 and chessboard[x-1][y] == COLOR_BLACK:#左是自己
                a = (x - 2, y)
                b = (x + 1, y)
                if a[0] >= 0 and a[1] >= 0 and a[0] <= self.chessboard_size-1 \
                        and a[1] <= self.chessboard_size-1 and chessboard[a[0]][a[1]] == 0:
                    valueboard[a[0]][a[1]] += 12
                    c = self.candidate_list[0]
                    if valueboard[a[0]][a[1]] > valueboard[c[0]][c[1]]:
                        self.candidate_list.pop()
                        self.candidate_list.append(a)
                        print("list变了39")
                if b[0] >= 0 and b[1] >= 0 and b[0] <= self.chessboard_size-1 \
                        and b[1] <= self.chessboard_size-1 and chessboard[b[0]][b[1]] == 0:
                    valueboard[b[0]][b[1]] += 12
                    c = self.candidate_list[0]
                    if valueboard[b[0]][b[1]] > valueboard[c[0]][c[1]]:
                        self.candidate_list.pop()
                        self.candidate_list.append(b)
                        print("list变了40")
            print("扫描完自己了")
            



            

        print("终")
        print(self.candidate_list[0][0],self.candidate_list[0][1])
        print("新一盘")
        print()












 # Make sure that the position of your decision in chess board is empty.
 #If not, return error.
        assert chessboard[new_pos[0],new_pos[1]]== COLOR_NONE
 #Add your decision into candidate_list, Records the chess board
        #self.candidate_list.append(new_pos)


def sizeok(x,y,size):
    if x>=0 and x<=size-1 and y>=0 and y<=size-1:
        return True
    else:
        return False


def bijiao(dian, candidate_list, valueboard):
    c = candidate_list[0]
    if valueboard[dian[0]][dian[1]] > valueboard[c[0]][c[1]]:
        candidate_list.pop()
        candidate_list.append(dian)







"""
def duyige(x,y)



    if sizeok(a[0], a[0], self.chessboard_size) and chessboard[a[0]][a[1]] == 0:
        valueboard[a[0]][a[1]] += 1
        c = self.candidate_list[0]
        if valueboard[a[0]][a[1]] > valueboard[c[0]][c[1]]:
            self.candidate_list.pop()
            self.candidate_list.append(a)

"""