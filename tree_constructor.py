### Convert my cache data into a tree structure####

import json

def tree_constructor(cache_data):
    ''' organize the cached congressmen data into a tree
    The cached Congress member's data will be organized into a tree-structured nested dictionary. 
    The first-level keys comprise 4 Congress (114-117). 
    The second-level keys comprise 2 chambers (senate and house). 
    The third-level keys comprise 50 US state abbreviations. 
    The fourth-level keys comprise the Twitter accounts of the Congress member affiliated with the state. 
    The fifth-level keys comprise the information of the congress member. 

    Parameters
    ----------
    cache_data: a nested dictionary
        a dictionary that contains restaurant data based on the user input
    Returns
    -------
    new_json: a nested dictionary
        an organized tree structure dictionary of comgress members' information based on the user entries.
    '''
    new_json = {'114':{'senate': {}, 'house': {}}, 
        '115':{'senate': {}, 'house': {}},
        '116':{'senate': {}, 'house': {}},
        '117':{'senate': {}, 'house': {}}}
    for key_cache in cache_data.keys():
        if key_cache[-2:] == 'NO':
            del cache_data[key_cache]
        for key_json in new_json.keys():
            if key_cache[0:3] == key_json:
                if key_cache[3] == 's':
                    new_json[key_json]['senate'][key_cache[-2:]] = cache_data[key_cache]
                if key_cache[3] == 'h':
                    new_json[key_json]['house'][key_cache[-2:]] = cache_data[key_cache]
    for key1 in new_json.keys():
        for key2 in new_json[key1].keys():
            for key3 in new_json[key1][key2].keys():
                temp = {item['twitter_account']: item for item in new_json[key1][key2][key3]}
                for value in temp.values():
                    del value['state']
                    del value['short_title']
                    del value['twitter_account']
                new_json[key1][key2][key3] = temp
    return new_json




if __name__ == "__main__":
    with open("congressmen_cache.json", 'r') as file:
       cache_data = json.load(file)
    new_json = tree_constructor(cache_data)
    with open("my_tree.json", 'w') as file:
        json.dump(new_json, file, indent = 4)


