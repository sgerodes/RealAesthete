with open('./immowelt_postal_codes.csv', 'r') as f, open('./immowelt_postal_code_insert.sql', 'w+') as f2:
    postal_code_list = f.readlines()
    f2.write('INSERT INTO ImmoweltPostalCodeStatistics (postal_code, exposition_type, estate_type, total_entries) VALUES\n')
    values = list()
    for estate_type in ['HOUSE', 'FLAT']:
        for exposition_type in ['RENT', 'BUY']:
            for postal_code in postal_code_list:
                values.append(f'("{postal_code.strip()}","{exposition_type}","{estate_type}",0)')
                #f2.write(f'("{postal_code.strip()}","{exposition_type}","{estate_type}",0)')
    f2.write(',\n'.join(values))
    f2.write(';\n')
