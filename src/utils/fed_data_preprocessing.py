import numpy as np

# Mapping The Training, Test Data
# Index of user and item in each client is different
    
def dataset_preprocessing(num_clients, train_datas, test_datas):
    """Map global user/item ids to per-client local ids.

    Local user id = rank of the global user id among the client's subgraph users
    (same order as the client's train/val/test json rows and the eigenvector rows).
    Local item id = rank of the global item id among the client's subgraph items.
    Train data is mapped only once (the function is called for test and for val).
    Test/val items outside the client's item set are dropped BEFORE mapping.
    """
    removed_test_datas = []
    for i in range(num_clients):
        item_nodes = train_datas[i][4]
        g2l_item = {g: l for l, g in enumerate(item_nodes)}
        if len(train_datas[i]) < 7:  # not mapped yet
            user_ids = train_datas[i][5]
            g2l_user = {g: l for l, g in enumerate(user_ids)}
            train_datas[i][1] = [(g2l_user[u], g2l_item[it]) for (u, it) in train_datas[i][1]
                                 if u in g2l_user and it in g2l_item]
            train_datas[i][0] = [[g2l_item[it] for it in sub if it in g2l_item] for sub in train_datas[i][0]]
            train_datas[i].append(True)  # mapped flag
        removed_test_datas.append([[g2l_item[v] for v in sub if v in g2l_item] if sub else []
                                   for sub in test_datas[i]])
    return removed_test_datas

def testset_preprocessing(num_clients, train_datas, test_datas, TOP_K, TEST_USER_BATCH, KEEP_PORB):
    para_test = []
    for i in range(num_clients):
        test = [train_datas[i][0], test_datas[i], train_datas[i][2], train_datas[i][3], TOP_K, TEST_USER_BATCH, KEEP_PORB]
        para_test.append(test)
    
    return para_test

def get_item_degrees(interaction_data):
    item_degrees = {}
    
    # Iterate over each interaction (user_id, item_id)
    for interaction in interaction_data:
        item_id = interaction[1]  # Extracting item_id from interaction
        
        # If item_id already exists in item_degrees, increment its degree
        if item_id in item_degrees:
            item_degrees[item_id] += 1
        # If item_id is encountered for the first time, initialize its degree to 1
        else:
            item_degrees[item_id] = 1
    
    return item_degrees

def get_all_degrees(interaction_data):
    user_degrees = {}
    item_degrees = {}
    
    # Iterate over each interaction (user_id, item_id)
    for interaction in interaction_data:
        user_id = interaction[0]  # Extracting user_id from interaction
        item_id = interaction[1]  # Extracting item_id from interaction
        
        # If user_id already exists in user_degrees, increment its degree
        if user_id in user_degrees:
            user_degrees[user_id] += 1
        # If user_id is encountered for the first time, initialize its degree to 1
        else:
            user_degrees[user_id] = 1
        
        # If item_id already exists in item_degrees, increment its degree
        if item_id in item_degrees:
            item_degrees[item_id] += 1
        # If item_id is encountered for the first time, initialize its degree to 1
        else:
            item_degrees[item_id] = 1
            
    return user_degrees, item_degrees

def get_pop_index(degree):
    if degree <= 10: return 0
    elif degree <= 20: return 1
    elif degree <= 30: return 2
    elif degree <= 40: return 3
    elif degree <= 50: return 4
    elif degree <= 100: return 5
    elif degree <= 200: return 6
    elif degree <= 300: return 7
    elif degree <= 400: return 8
    elif degree <= 500: return 9
    else: return 10