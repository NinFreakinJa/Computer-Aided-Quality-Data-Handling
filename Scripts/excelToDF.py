import pandas as pd

def excel_to_df(fileName):
    #Determine Excel Type
    xls = pd.ExcelFile(fileName)
    numSheets = len(xls.sheet_names)

    if numSheets == 1:
        repo = pd.read_excel(xls, 'Sum Report')
        repo.dropna(how='all', axis=1, inplace=True)

        return repo
    else:
        proto = pd.read_excel(xls, 'Protokoll_Intern')
        proto.dropna(how='all', axis=1, inplace=True)

        return proto
