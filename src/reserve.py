
def text_to_columns(data):
    """
    DESCRIPTION : Format the column names
    """
    # Create dictionary to extract fields
    dic = {0: '상권_핵심주소', 1: '상권_주소_1', 2: '상권_주소_2', 3: '상권_주소_3', 4: '상권_주소_4', 5: '상권_주소_5',
           6: '상권_주소_6', 7: '상권_주소_7'}

    sub_dic = {0: '상권_핵심주소', 1: '상권_주소_1', 2: '상권_주소_2', 3: '상권_주소_3', 4: '상권_주소_4', 5: '상권_주소_5'}

    # Extract key address from the field
    df = pd.DataFrame()
    df['상권_코드_명'] = data['상권_코드_명'].str.replace('?', '', regex=True)
    df = pd.concat([df['상권_코드_명'], df['상권_코드_명'].str.split(' ', expand=True)], axis=1).rename(columns=dic)
    df = pd.concat([df['상권_코드_명'], df['상권_핵심주소'].str.split('_', expand=True)], axis=1).rename(columns=sub_dic)

    output = data.merge(df['상권_핵심주소'], left_index=True, right_index=True)

    return output

