import random
from pandas import DataFrame

def getPairPool(player_name,num_round):
    random_seed = 123
    random.seed(random_seed)
    num_people = len(player_name)
    print(num_people)
    # all_pair有多少对搭档，必须是偶数
    if num_people*num_round%4 == 0:
        num_pair = num_people*num_round//2
    else:
        num_pair = (num_people*num_round//4+1)*2

    num_person_add_one = num_pair*2-num_people*num_round # 有多少人是多一局的，字典从-1开始
    round_lis = [-1]*num_person_add_one
    round_lis.extend([0]*(num_people-num_person_add_one)) # 局数分布
    random.seed(random_seed)
    random.shuffle(round_lis)

    dict_person_round = dict(zip(player_name,round_lis))
    # print(dict_person_round)
    candidate_pool =[]  # 候选的搭档池
    for i in range(num_people):
      for j in range(i+1,num_people):
          candidate_pool.append([player_name[i],player_name[j]])
    # print(candidate_pool)

    random.seed(random_seed)                                              
    random.shuffle(candidate_pool)
    # print(candidate_pool)
    pair_pool =[]  # 用于参赛的搭档池子
    for i in range(100):
        # print(candidate_pool)
        candidate = candidate_pool.pop(0)
        p1 = str(candidate[0])
        p2 = str(candidate[1])
        if  dict_person_round.get(p1,num_round)<num_round and dict_person_round.get(p2,num_round)<num_round:
            pair_pool.append(candidate)
            dict_person_round[p1] += 1
            dict_person_round[p2] += 1
        else:
            candidate_pool.append(candidate)
        if len(pair_pool)==num_pair: 
            break
    
    if len(pair_pool)<num_pair:
        # 情况一：多于两个人不满足局数
        person_dissatisfy = [k for k,v in dict_person_round.items() if v<num_round]
        while len(person_dissatisfy)>=2: 
            p1 = person_dissatisfy[0]
            contain_p1 =[]
            for candidate in candidate_pool:
                if p1 in candidate:
                    contain_p1.append(candidate)
        
            p2 = person_dissatisfy[1]
            contain_p2 =[]
            for candidate in candidate_pool:
                if p2 in candidate:
                    contain_p2.append(candidate)
        
            for i in range(len(contain_p1)):
                for j in range(len(contain_p2)):
                    tmp =contain_p1[i]+contain_p2[j]
                    tmp.remove(p1)
                    tmp.remove(p2)
                    if tmp in pair_pool:
                        exchange_pair= tmp
                        break
                    elif [tmp[1],tmp[0]] in pair_pool:
                        exchange_pair= [tmp[1],tmp[0]]
                        break
                    else:
                        continue
                if exchange_pair:
                    break
            
            pair_pool.remove(exchange_pair)
            pair_pool.append(contain_p1[i])
            pair_pool.append(contain_p2[j])
            
            candidate_pool.append(exchange_pair)
            candidate_pool.remove(contain_p1[i])
            candidate_pool.remove(contain_p2[j])
            
            dict_person_round[p1] += 1
            dict_person_round[p2] += 1
            person_dissatisfy = [k for k,v in dict_person_round.items() if v<num_round]

    # 情况二：只有一个人不满足局数
        if len(person_dissatisfy)==1:
            person = person_dissatisfy[0]
            contain_person = []
            for candidate in candidate_pool:
                if person in candidate:
                    contain_person.append(candidate)

            for i in range(len(contain_person)):
                for j in range(i+1,len(contain_person)):
                    tmp = contain_person[i]+contain_person[j]
                    tmp.remove(person)
                    tmp.remove(person)
                    if tmp in pair_pool:
                        exchange_pair= tmp
                        break
                    elif [tmp[1],tmp[0]] in pair_pool:
                        exchange_pair= [tmp[1],tmp[0]]
                        break
                    else:
                        continue
                if exchange_pair:
                    break

            pair_pool.remove(exchange_pair)
            pair_pool.append(contain_person[i])
            pair_pool.append(contain_person[j])
            dict_person_round[person] += 2
    return pair_pool

def getLineupTable(num_people,num_round):
    pair_pool = getPairPool(num_people,num_round)
    all_round = len(pair_pool)//2 # 所有场
    res =[]
    rivalry =[]
    for i in range(201):
        per = pair_pool.pop(0)
        if len(rivalry)==0:
            rivalry.append(per)
        elif len(set(per) & set(rivalry[0]))==0:
            rivalry.append(per)
        else:
            pair_pool.append(per)
        if len(rivalry)==2:
            res.append(rivalry)
            rivalry =[]
            if len(res)==all_round:
                break
        if i==200:  # 不满足对阵要求
            pair_pool.extend(rivalry)
            pool_ele = set([x for y in pair_pool for x in y])
            for i in range(len(res)):
                if len(set([x for y in res[i] for x in y]) & pool_ele)==0:
                    tmp = res[i][0]
                    res[i][0] = pair_pool[0]
                    pair_pool[0] = tmp
                    break
            res.append(pair_pool)
    df = DataFrame(res,columns=['A','B'])
    df['A1'] = df['A'].apply(lambda x:x[0])
    df['A2'] = df['A'].apply(lambda x:x[1])
    df['B1'] = df['B'].apply(lambda x:x[0])
    df['B2'] = df['B'].apply(lambda x:x[1])
    return df[['A1','A2','B1','B2']]



if __name__ == "__main__":
    multi_player = ['135','jintianwochibao','Anthony','Morpheus','xuguanquan','guoqing','yuli','CYP','Yvone','Eager','Rocket','Alan','tuanzi','qiqi','longlong','CC']
    single_player = ['Morpheus','tuanzi','longlong','takki','xuziyi','Vincent','Rocket','CC']
    # multi_result = getPairPool(multi_player, num_round=7)
    # print(multi_result)
    # multi_result2 = getLineupTable(multi_player,num_round=7)
    # print(multi_result2)
    single_result = getPairPool(single_player, num_round=7)
    # print(single_result)
