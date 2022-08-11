TABLENAME = 'immowelt_postal_code_statistics'

def var_1():
    with open('./immowelt_postal_codes.csv', 'r') as f, open('./immowelt_postal_code_insert.sql', 'w+') as f2:
        postal_code_list = f.readlines()
        f2.write(
            f'INSERT INTO {TABLENAME} (postal_code, exposition_type, estate_type, total_entries, created_at) VALUES\n')
        values = list()
        for estate_type in ['FLAT', 'HOUSE']:
            for exposition_type in ['RENT', 'BUY']:
                for postal_code in postal_code_list:
                    values.append(f'("{postal_code.strip()}","{exposition_type}","{estate_type}",0, DATETIME("now"))')
        f2.write(',\n'.join(values))
        f2.write(';\n')

def var_2():
    with open('./immowelt_postal_codes.csv', 'r') as f, open('./immowelt_postal_code_insert.sql', 'w+') as f2:
        postal_code_list = f.readlines()
        for estate_type in ['FLAT', 'HOUSE']:
            for exposition_type in ['RENT', 'BUY']:
                for postal_code in postal_code_list:
                    f2.write(
                        f'INSERT INTO {TABLENAME} (postal_code, exposition_type, estate_type, total_entries, created_at) '
                        f'VALUES ("{postal_code.strip()}","{exposition_type}","{estate_type}",0, DATETIME("now"));\n')
def var_3():
    with open('./immowelt_postal_codes.csv', 'r') as f, open('./immowelt_postal_code_insert.sql', 'w+') as f2:
        postal_code_list = f.readlines()
        for estate_type in ['FLAT', 'HOUSE']:
            for exposition_type in ['RENT', 'BUY']:
                f2.write(
                    f'INSERT INTO {TABLENAME} (postal_code, exposition_type, estate_type, total_entries, created_at) VALUES\n')
                values = list()
                for postal_code in postal_code_list:
                    values.append(f'("{postal_code.strip()}","{exposition_type}","{estate_type}",0, DATETIME("now"))')
                f2.write(',\n'.join(values))
                f2.write(';\n')
var_3()
