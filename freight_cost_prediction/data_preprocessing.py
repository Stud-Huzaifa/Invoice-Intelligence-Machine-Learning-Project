def load_vendor_invoice_data(db_path: str):
    '''''
     Load Vendor Invoice Data From SQlite Database
     '''''
    conn =sqlite3.connect(db_path)
    query = "SELECT * FROM vendor_invoice"
    df  =pd.read_sql_query(query,conn)
    conn.close()
    return df



def  prepare_features(df : pd.Dataframe):
    ''' select features & target variable
    '''
    x = df["Dollars"]
    y = df["Freight"]
    return x,y

def split_data(X,y,test_size =0.2 ,random_state =42)
        """""
        spilit the dataset into training & testing 
        """""
        return train_test_split(
                    X,y,test_size=test_size,random_state = random_state)
        