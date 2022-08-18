#!/usr/bin/python
# Press Shift+F10 to execute it or replace it with your code.

import pandas as pd
import os
import glob
from zipfile import ZipFile

x = 0
file_paths = []
my_set = set()

directory = "med_data"
print(os.listdir(directory))

for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        # print("csv")
        files = list(os.listdir(directory))
        print(files)

for i in files:
    file = i
    position = file.index('.')
    file_date = file[9:position]
    print(file_date)

    if len(file_date) != 14:
        print("invalid date length")
    elif not file_date.isnumeric():
        print("Not a number.")
    else:
        df = pd.read_csv(file)
        if not df.empty:
            print(df)
            print(df.isna().any())
            print(df.dtypes)

    if x == 0:
        for i in df['batch_id']:
            print(df['batch_id'].unique())
            # print(my_set)
    elif x == 1:
        for i in df['batch_id']:
            print(i)
            if i in my_set:
                df['batch_id'].drop(i)
                print("duplicated ids, row dropped")
                print(df['batch_id'])
            else:
                print("unique batch ids")
                my_set.update(df['batch_id'])
        print(my_set)
    elif x == 2:
        for i in df['batch_id']:
            print(i)
            if i in my_set:
                df['batch_id'].drop(i)
                print("duplicated ids, row dropped")
                print(df['batch_id'])
            else:
                print("unique batch ids")
                my_set.update(df['batch_id'])
        print(my_set)
    elif x == 3:
        for i in df['batch_id']:
            print(i)
            if i in my_set:
                df['batch_id'].drop(i)
                print("duplicated ids, row dropped")
                print(df['batch_id'])
            else:
                print("unique batch ids")
                my_set.update(df['batch_id'])
        print(my_set)
    elif x == 4:
        for i in df['batch_id']:
            print(i)
            if i in my_set:
                df['batch_id'].drop(i)
                print("duplicated ids, row dropped")
                print(df['batch_id'])
            else:
                print("unique batch ids")
                my_set.update(df['batch_id'])
        print(my_set)
    elif x == 5:
        for i in df['batch_id']:
            print(i)
            if i in my_set:
                df['batch_id'].drop(i)
                print("duplicated ids, row dropped")
                print(df['batch_id'])
            else:
                print("unique batch ids")
                my_set.update(df['batch_id'])
        print(my_set)
    else:
        print("Error")

    cols = "batch_id, timestamp"
    # print(cols[0])
    df1 = df.loc[:, df.columns != cols]
    df1.round(3)

    df2 = df[df.isna().any(axis=1)]
    print(df2)

    df3 = df1.dropna(axis=0)
    print(df3)

    df4 = df3[df3.duplicated()]
    df2.append(df4)
    print(df2)

    list_cols = ["batch_id", "timestamp", "reading1", "reading2", "reading3", "reading4", "reading5", "reading6",
                 "reading7", "reading8", "reading9", "reading10"]
    my_list = list(df3)
    if my_list != list_cols:
        print("mismatch of header names")

    df5 = df3.drop(['batch_id', 'timestamp'], axis=1)
    print(df5.dtypes)
    new_list = list_cols[2:]
    print(df5)

    limit = 9.9
    count = (df5[new_list] > limit).sum()
    print('Count of values greater than 9.999 in all columns : ', count)

    y = str(x)
    # cleaned_data_name = y + "clean_data.csv.zip"
    # print(cleaned_data_name)
    x += 1
    print(x)
    # df3.to_csv("clean_data.csv.zip",
    #          index=False,
    #          compression="zip")

    # empty_zip_data = b'PK\x05\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

    # zip = ZipFile('sample.zip', 'w')

    if x == 1:
        df3.to_csv("clean_data.csv")
        file_paths.append("clean_data.csv")
        # zip.write("clean_data.csv")
    elif x == 2:
        df3.to_csv("clean_data1.csv")
        file_paths.append("clean_data1.csv")
        # zip.write("clean_data1.csv")
    elif x == 3:
        df3.to_csv("clean_data2.csv")
        file_paths.append("clean_data2.csv")
        # zip.write("clean_data2.csv")
    elif x == 4:
        df3.to_csv("clean_data3.csv")
        file_paths.append("clean_data3.csv")
        # zip.write("clean_data3.csv")
    elif x == 5:
        df3.to_csv("clean_data4.csv")
        file_paths.append("clean_data4.csv")
        # zip.write("clean_data4.csv")

    else:
        print("Compression not possible.")

    with ZipFile('my_python_files.zip', 'w') as zip:
        # writing each file one by one
        for file in file_paths:
            zip.write(file)
