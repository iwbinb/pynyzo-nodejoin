def new_pk_file(pk_list_popped):
    with open('data/test2.txt', 'w') as f:
        f.write(pk_list_popped)
    print('Performed PK file rewrite')

def new_ip_data(new_str_dict):
    with open('data/assign', 'w') as f:
        f.write(new_str_dict)

