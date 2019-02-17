import ast

test_dict = {'cb': 21, 'cl': 9, 'cr': 21, 'ct': 18, 'id': 'ir7SMNAH2QJQiM:', 'isu': 'songmetro.com', 'itg': 1, 'ity': '', 'oh': 300, 'ou': 'https://i.scdn.co/image/cfeeaf0eb9bd922cfb8ff13ce16e907be0e543b8', 'ow': 300, 'pt': 'Quang Linh - Sợi Tóc Để Quên 🎵500/Quang%20Linh/S%E1%BB%A3i%20T%C3%B3c%20%C4%90%E1%BB%83%20Qu%C3%AAn', 's': 'Quang Linh - Sợi Tóc Để Quên', 'tu': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRV361Rnsi4ofw4_h4rvontRuKpfVakm_uS3HTcZ1Q4E2UQamfC_w', 'tw': 225}


def cvdb2utf8():
    from django.db import connection
    from django.conf import settings
    cursor = connection.cursor()
    cursor.execute('SHOW TABLES')
    results=[]
    for row in cursor.fetchall(): 
        results.append(row)

    for row in results: 
        cursor.execute('ALTER TABLE %s CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;' % (row[0]))

    cursor.execute('ALTER DATABASE %s CHARACTER SET utf8mb4;' % settings.DATABASES['default']['NAME']) 


def map_nested_dicts(obj, func):
    import collections
    if isinstance(obj, collections.Mapping):
        return {k: map_nested_dicts(v, func) for k, v in obj.iteritems()}
    else:
        return func(obj)

# def test():
    # t = map_nested_dicts(test_dict, lambda x:x.encode('utf8mb4'))
    # print (t)
    
cvdb2utf8()