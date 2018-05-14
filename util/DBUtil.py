import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017')

db = client['bcunn']

data_db = db['second_data']


def save(data_list):
    result = []
    for i in data_list:
        result.append(data_db.save(i))
    return result

#
# if __name__ == '__main__':
#     save_result = save()
#     find_result = find()
#     print("end")
