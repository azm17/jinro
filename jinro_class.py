class GIData:

    def __init__(self):
        self.alive_list = []
        self.divined_list = []#uranatta-
        self.co_list = []#comingout
        self.lier_list = []#uso
        
    def update_day_first(self, base_info, diff_data):
        pass
        
    def update_turn(self, base_info, diff_data):

        self.alive_list = [i for i in base_info['statusMap'].keys() if i != base_info['agentIdx'] \
                            and base_info['statusMap'][i] == 'ALIVE']

        # read log
        # print("read log")
        for i in range(diff_data.shape[0]):
            # vote
            #print("line:\n"+str(diff_data[i:i+1]))
            day = diff_data.day[i]
            turn = diff_data.turn[i]
            if diff_data.type[i] == 'vote' and diff_data.turn[i] == 0:
                #self.x_3d[self.diff_data.idx[i] - 1, self.diff_data.agent[i] - 1, 0] += 1
                #print("vote")
                pass
            # execute
            elif diff_data.type[i] == 'execute':
                #self.x_2d[self.diff_data.agent[i] - 1, 0] = 1
                #print("execute")
                pass
            # attacked
            elif diff_data.type[i] == 'dead':
                #self.x_2d[self.diff_data.agent[i] - 1, 1] = 1
                #print("dead")
                pass
            # talk
            elif diff_data.type[i] == 'talk':
                # content = self.diff_data.text[i].split()
                a_num = diff_data.agent[i]
                tmp = read_text(day, turn, a_num, diff_data.text[i])
                # print(self.diff_data.turn[i], "talk ", content[0], end='')
                # comingout

                if tmp.op == 'BECAUSE':
                    pass
                    # self.evaluate_sentence(tmp.sen_list[1])
                elif tmp.op == 'AND':
                    for sen in tmp.sen_list:
                        self.evaluate_sentence(sen)
                elif tmp.op == 'DAY':
                    for sen in tmp.sen_list:
                        self.evaluate_sentence(sen)

    def evaluate_sentence(self, sentence):
        if sentence.verb == 'DIVINED':
            #print("divinded!!")
            self.divined_list.append(sentence)
        elif sentence.verb == 'COMINGOUT':
            #print("comingout!!")
            self.co_list.append(sentence)

    def is_co_player(self, num):#barasita
        return len([sen for sen in self.co_list if sen.sub_id == num]) > 0

    def get_white_list(self):#janai
        return [sen.tar_id for sen in self.divined_list if sen.comp == 'HUMAN']

    def get_black_list(self):#sou
        return [sen.tar_id for sen in self.divined_list if sen.comp == 'WEREWOLF']


class Sentence:
    def __init__(self, pub_day=0, pub_turn=0, \
                        sub_id=-2, verb='', tar_id=-2, \
                        comp='', occ_day=0):
        self.pub_day = pub_day
        self.pub_turn = pub_turn
        self.sub_id = sub_id#
        self.verb = verb#
        self.tar_id = tar_id#
        self.comp = comp#
        self.occ_day = occ_day

        self.array = [self.pub_day, \
                      self.pub_turn, \
                      self.sub_id, \
                      self.verb, \
                      self.tar_id, \
                      self.comp, \
                      self.occ_day]


class Section:
    def __init__(self, pub_day=-2, pub_turn=-2, op='', sen_list=[], occ_day=-2):
        self.pub_day = pub_day
        self.pub_turn = pub_turn
        self.op = op
        self.sen_list = sen_list
        self.occ_day=occ_day

        if len(sen_list) > 0:
            for sen in sen_list:
                sen.pub_day = self.pub_day
                sen.pub_turn = sen.pub_turn
                sen.occ_day = self.occ_day

    def is_sentence(self):
        return self.op == ''

    def has_verb(self, verb):
        return len([sen for sen in sen_list \
                                if sen.verb == verb]) > 0

    #def get_

def is_alive(id_num, base_info):
    return base_info['statusMap'][id_num] == 'ALIVE'

def is_killed(id_num, base_info):
    return base_info['statusMap'][id_num] == 'DEAD'

def is_co_player(id_num, co_list):
    l = [c[1] for c in co_list if c[0] == id_num]
    return len(l) > 0

def get_co(id_num, co_list):
    l = [c[1] for c in co_list if c[0] == id_num]
    return l[-1]

def is_co_role(role, co_list):
    return

def read_text(pd, pt, a_num, text):
    #print("text:", text)
    
    content = text.split(' ', 1)
    head = content[0]

    if len(content) > 1:
        rest = content[1]
    
    # 2.1
    if head == 'ESTIMATE':
        pass
    elif head == 'COMINGOUT':
        words = rest.split(" ")
        sen = Sentence(sub_id=a_num, verb='COMINGOUT', \
                        tar_id=a_num, comp=words[1])
        return Section(pub_day=pd, pub_turn = pt, sen_list=[sen])

    # 2.2
    elif head == 'DIVINATION':
        pass
    elif head == 'GUARD':
        pass
    elif head == 'VOTE':
        pass
    elif head == 'ATTACK':
        pass

    # 2.3
    elif head == 'DIVINED':
        words = rest.split(" ")
        sen = Sentence(sub_id=a_num, verb='DIVINED', \
                        tar_id=int(words[0][6:8]), comp=words[1])
        return Section(pub_day=pd, pub_turn = pt, sen_list=[sen])
    elif head == 'IDENTIFIED':
        pass
    elif head == 'GUARDED':
        pass
    elif head == 'VOTED':
        pass
    elif head == 'ATTACKED':
        pass
    
    # 2.4
    elif head == 'AGREE':
        pass
    elif head == 'DISAGREE':
        pass

    # 2.5
    elif head == 'OVER':
        pass
    elif head == 'SKIP':
        pass


    # 3.1
    elif head == 'REQUEST':
        pass
    elif head == 'INQUIRE':
        pass

    # 3.2
    elif head == 'BECAUSE':
        sections = [read_text(pd, pt, a_num, tmp) for tmp in split_blancket(rest)]
        sentences = []
        for sec in sections:
            sentences.extend(sec.sen_list)
        sec = Section(pub_day=pd, pub_turn=pt, op='BECAUSE', sen_list=sentences)
        return sec

    # 3.3 
    elif head == 'DAY':
        w = rest.split(" ", 1)
        day = int(w[0])
        nobl = split_blancket(w[1])
        tmp = read_text(pd, pt, a_num, nobl[0])
        tmp.op = 'DAY'
        for sen in tmp.sen_list:
            sen.occ_day = day
        return tmp

    # 3.4
    elif head == 'NOT':
        pass
    elif head == 'AND':
        sections = [read_text(pd, pt, a_num, tmp) for tmp in split_blancket(rest)]
        sentences = []
        for sec in sections:
            sentences.extend(sec.sen_list)
        sec = Section(pub_day=pd, pub_turn=pt, op='AND', sen_list=sentences)
        return sec
    elif head == 'OR':
        sections = [read_text(pd, pt, a_num, tmp) for tmp in split_blancket(rest)]
        sentences = []
        for sec in sections:
            sentences.extend(sec.sen_list)
        sec = Section(pub_day=pd, pub_turn=pt, op='OR', sen_list=sentences)
        return sec
    elif head == 'XOR':
        sections = [read_text(pd, pt, a_num, tmp) for tmp in split_blancket(rest)]
        sentences = []
        for sec in sections:
            sentences.extend(sec.sen_list)
        sec = Section(pub_day=pd, pub_turn=pt, op='XOR', sen_list=sentences)
        return sec


    else:
        print('error')
        return Section()

    return Section()


def split_blancket(text):
    ret = []
    while True:
        text = text.strip()
        if len(text) <= 0:
            break

        tmp = 0
        l = 0
        for i in range(len(text)):
            if text[i] == '(':
                tmp += 1
            elif text[i] == ')':
                tmp -= 1

            if tmp == 0:
                l = i
                break

        ret.append(text[1:l])
        if len(text) -1 == l:
            break
        text = text[l+1:]

    return ret



