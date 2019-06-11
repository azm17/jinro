#!/usr/bin/env python
from __future__ import print_function, division 

# this is main script
# simple version

import aiwolfpy
import aiwolfpy.contentbuilder as cb
import numpy as np
import pandas as pd
import jinro_class as jinro

myname = 'azm17'

class SampleAgent(object):
    def __init__(self, agent_name):
        self.myname = agent_name
        
    def getName(self):
        return self.myname
    
    def initialize(self, base_info, diff_data, game_setting):
        self.base_info = base_info
        self.diff_data = diff_data
        # game_setting
        self.game_setting = game_setting
        #print(base_info)

        self.divined_list = []
        self.vote_list = []
        self.comingout = ''
        self.co_list = []
        self.myresult = ''
        self.not_reported = False
        self.vote_declare = 0
        
    def update(self, base_info, diff_data, request):
        self.base_info = base_info
        self.diff_data = diff_data
        self.update_info()
        
        
        # print(self.diff_data.dtypes)
        #pd.set_option('display.max_rows', 100)
        # print(self.diff_data)
        #self.talks = self.diff_data[self.diff_data['type'].isin(['talk'])]
        #self.divined = self.talks[self.talks['text'].str.contains('DIVINED')]
        #self.divined = self.talks.query('text.astype("str").str.contains("DIVINED")', engine='python')
        # print(self.talks)
        # print(self.divined)
        # print("############### request\n", request)
        
    def dayStart(self):
        self.talk_turn = 0
        return None
        
    def talk(self):
        self.talk_turn += 1
        if self.game_setting['playerNum'] == 15:
            if self.base_info['myRole'] == 'SEER' and self.comingout == '':
                #self.comingout = 'SEER'
                #return cb.comingout(self.base_info['agentIdx'], self.comingout)
                pass
            elif self.base_info['myRole'] == 'MEDIUM' and self.comingout == '':
                self.comingout = 'MEDIUM'
                return cb.comingout(self.base_info['agentIdx'], self.comingout)
            elif self.base_info['myRole'] == 'POSSESSED' and self.comingout == '':
                #self.comingout = 'SEER'
                pass
                #return cb.comingout(self.base_info['agentIdx'], self.comingout)        
            
            elif self.base_info['myRole'] == 'WEREWOLF' and self.comingout == '':
                self.comingout = 'SEER'
                alive_list=[]
                for i in range(1, self.game_setting['playerNum']+1):
                    if i==self.base_info['agentIdx']:
                        pass
                    elif self.base_info['statusMap'][str(i)] == 'ALIVE':
                        alive_list.append(i)
                return cb.comingout(random.choice(alive_list), self.comingout)
        else :
            if self.base_info['myRole'] == 'SEER' and self.comingout == '':
                #self.comingout = 'SEER'
                pass
                return cb.comingout(self.base_info['agentIdx'], self.comingout)
            elif self.base_info['myRole'] == 'MEDIUM' and self.comingout == '':
                self.comingout = 'MEDIUM'
                return cb.comingout(self.base_info['agentIdx'], self.comingout)
            elif self.base_info['myRole'] == 'POSSESSED' and self.comingout == '':
                #self.comingout = 'SEER'
                #return cb.comingout(self.base_info['agentIdx'], self.comingout)   
                pass     
            elif self.talk_turn <= 2:
                return cb.skip()

        return cb.over()
        
    def whisper(self):
        return cb.skip()
        
    def vote(self):
        
        print(self.base_info['statusMap'])
        
        
        print('---VOTE_SETION---')
        white_list = [d[1] for d in self.divined_list if d[2] == "white" and d[1]!=self.base_info['agentIdx']and self.base_info['statusMap'][str(d[1])]=='ALIVE']
        
        list_count_white=[white_list.count(i) for i in range(1,len(self.base_info['statusMap'])+1)]
        print('[white]',list_count_white)
        
        black_list = [d[1] for d in self.divined_list if d[2] == "black" and d[1]!=self.base_info['agentIdx']and self.base_info['statusMap'][str(d[1])]=='ALIVE']
        list_count_black=[black_list.count(i) for i in range(1,len(self.base_info['statusMap'])+1)]
        #print(black_list)
        
        print('[black]',list_count_black)
        
        vote_list = [d[1] for d in self.divined_list if d[2] == "vote" and d[1]!=self.base_info['agentIdx'] and self.base_info['statusMap'][str(d[1])]=='ALIVE']
        
        list_count_vote=[vote_list.count(i) for i in range(1,len(self.base_info['statusMap'])+1)]
        print('[vote] ',list_count_vote)

        #value of vote
        #parameter alpha:vote,beta:black,gamma:white
        
        alpha,beta,gamma=0.3,0.8,-0.2
        list_value_vote=[x*alpha+y*beta+z*gamma for x, y, z in zip(list_count_vote, list_count_black,list_count_white)]

        list_value_vote[int(self.base_info['agentIdx'])-1]=-10
        
        print('[wave] ',list_value_vote)
        

        max_list = [i+1 for i in range(len(list_value_vote)) if list_value_vote[i]==max(list_value_vote)]
        
        tmp=1
        if len(max_list)>0:
            tmp_val=np.random.choice(max_list)
            print('voted',tmp_val)
            
            return tmp_val
            
        #parameter failed
        elif len(black_list)>0:
            print('failed')
            tmp_list=black_list
            tmp=np.random.choice(tmp_list)
            print('voted {}'.format(tmp)+'\n '+'---VOTE_SETION---end')
            return tmp
        
        elif len(vote_list)>0:
            print('failed')
            tmp=np.random.choice(vote_list)
            print('voted',tmp)
            return tmp
        
        else:
            print('failed')
            status_dic = self.base_info['statusMap']
            alive = [i for i in status_dic.keys() if i != self.base_info['agentIdx'] \
                                                    and status_dic[i] == 'ALIVE'     \
                                                    and not(self.is_co_player(i))    \
                                                    and not(i in white_list)]
            tmp = np.random.choice(alive)
            print('voted',tmp)
            return tmp
        
    def attack(self):
        status_dic = self.base_info['statusMap']
        alive = [i for i in status_dic.keys() if i != self.base_info['agentIdx'] and status_dic[i] == 'ALIVE']
        return np.random.choice(alive)
    
    def divine(self):
        #status_dic = self.base_info['statusMap']
        #alive = [i for i in status_dic.keys() if i != self.base_info['agentIdx'] and status_dic[i] == 'ALIVE']
        #return np.random.choice(alive)

        alive_list=[]
        for i in range(1, self.game_setting['playerNum']+1):
            if i==self.base_info['agentIdx']:
                #print("MYID")
                pass
            #elif(sudeniuranaizumi) 
            
            elif self.base_info['statusMap'][str(i)] == 'ALIVE':
                alive_list.append(i)
        #print(alive_list)
        return random.choice(alive_list)
    
    def guard(self):
        status_dic = self.base_info['statusMap']
        #
        alive = [i for i in status_dic.keys() if i != self.base_info['agentIdx'] and status_dic[i] == 'ALIVE']
        return np.random.choice(alive)
    
    def finish(self):
        return None

    def update_info(self):
        # read log
        #print("read log")
        for i in range(self.diff_data.shape[0]):
            # vote
            if self.diff_data.type[i] == 'vote' and self.diff_data.turn[i] == 0:
                pass
            # execute
            elif self.diff_data.type[i] == 'execute':
                pass
            # attacked
            elif self.diff_data.type[i] == 'dead':
                pass
            # talk
            elif self.diff_data.type[i] == 'talk':###########talk###############
                content = self.diff_data.text[i].split()
                #print('---------')
                if content[0]!='Skip' and content[0]!='Over':
                    #print('print_content:',content)
                    pass

                #print('aaaaa',self.diff_data.turn[i], "talk ", content[0], end='')
                
                # comingout ex)
                if content[0] == 'COMINGOUT':
                    #print("co")
                    # self
                    if int(content[1][6:8]) == self.diff_data.agent[i]:
                        if content[2] == 'SEER':
                            self.co_list.append((self.diff_data.agent[i],'SEER'))
                        elif content[2] == 'MEDIUM':
                            self.co_list.append((self.diff_data.agent[i],'MEDIUM'))
                        elif content[2] == 'BODYGUARD':
                            self.co_list.append((self.diff_data.agent[i],'BODYGUARD'))
                        elif content[2] == 'VILLAGER':
                            self.co_list.append((self.diff_data.agent[i],'VILLAGER'))
                ##
                elif content[0] == 'DAY':
                    # divined
                    if content[2][1:] == 'DIVINED':# DAY 2 (DIVINED Agent[01] HUMAN)
                        print(content[4])#役職
                        if content[4][:-1] == 'HUMAN':
                            self.divined_list.append((self.diff_data.agent[i], int(content[3][6:8]), "white"))
                            #print(int(content[3][6:8]), "is white!!")
                        elif content[4][:-1] == 'WEREWOLF':
                            self.divined_list.append((self.diff_data.agent[i], int(content[3][6:8]), "black"))
                            #print(int(content[3][6:8]), "is black!!")
                
                elif content[0] == 'AND'or content[0] == 'BECAUSE':#AND (VOTE Agent[04]) REQUEST ANY(VOTE Agent[04]))
                    if content[1] == '(VOTE':
                        self.divined_list.append((self.diff_data.agent[i], int(content[2][6:8]), "vote"))
                        #print(self.divined_list)
                        #print('AND VOTE')
                    elif content[1] == '(DAY':
                        print('AND DAY')
                        
                        if content[5][:-2] == 'HUMAN':
                            self.divined_list.append((self.diff_data.agent[i], int(content[4][6:8]), "white"))
                            #print(int(content[4][6:8]), "is white!!")
                        elif content[5][:-2] == 'WEREWOLF':
                            self.divined_list.append((self.diff_data.agent[i], int(content[4][6:8]), "black"))
                            #print(int(content[4][6:8]), "is black!!")
                    else:
                        #print('miss')
                        pass
                        
                # identified
                elif content[0] == 'IDENTIFIED':
                    print("identified")

                    # result
                    if content[2] == 'HUMAN':
                        pass
                    elif content[2] == 'WEREWOLF':
                        pass
                else:
                    #print()
                    pass

    def is_alive(self, id_num):
        return self.base_info['statusMap'][id_num] == 'ALIVE'

    def is_killed(self, id_num):
        return self.base_info['statusMap'][id_num] == 'DEAD'

    def is_co_player(self, id_num):
        l = [c[1] for c in self.co_list if c[0] == id_num]
        return len(l) > 0

    def get_co(self, id_num):
        l = [c[1] for c in self.co_list if c[0] == id_num]
        return l[-1]
        
    def is_co_role(self, role):
        return

agent = SampleAgent(myname)
    


# run
if __name__ == '__main__':
    aiwolfpy.connect_parse(agent)
    
