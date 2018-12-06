
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup


# In[2]:


import requests


# In[3]:


import pandas as pd


# In[4]:


isl_url = 'http://www.espn.in/football/table/_/league/ind.1'


# In[5]:


ileague_url = 'http://www.espn.in/soccer/table/_/league/ind.2'


# In[97]:


# r = requests.get(ileague_url)
# soup = BeautifulSoup(r.text, 'lxml')

# table = soup.find('table')


# In[15]:


# for line in table.findAll('tr'):
#     for l in line.findAll('td'):
#         if l.find('sup'):
#             l.find('sup').extract()
#         print l.getText(),'|',
#     print


# In[127]:


# for x in table.find_all('th'):
#     print x.get_text()


# In[6]:


def make_table(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.find('table')
    new_table = pd.DataFrame(columns=['Team', 'Played', 'Won', 'Draw', 'Lost', 'For', 'Against', 'GD', 'Points'], 
                             index = range(0,len(table.find_all('tr')) )) # I know the size 

    row_marker = 0

    for row in table.find_all('tr'):
        column_marker = 0
        columns = row.find_all('td')
        for column in columns:
            if(column_marker == 0):
                new_table.iat[row_marker,column_marker] = column.find('abbr').get_text()
                if(new_table.iat[row_marker,column_marker] == ''):
                    new_table.iat[row_marker,column_marker] = 'RKFC' #Due to no abbr for Real Kashmir
                elif(new_table.iat[row_marker,column_marker] == 'KEB'):
                    new_table.iat[row_marker,column_marker] = 'QEB'
            else:
                new_table.iat[row_marker,column_marker] = column.get_text()
            column_marker += 1

        row_marker += 1
        
    new_table['W-D-L'] = new_table['Won'].astype(str) +'-'+ new_table['Draw'] + '-'+ new_table['Lost']
    new_table = new_table[['Team','Played','Points','W-D-L','GD']]
        
    return new_table
    


# In[128]:


# new_table = pd.DataFrame(columns=['Team', 'Played', 'Won', 'Draw', 'Lost', 'For', 'Against', 'GD', 'Points'], index = range(0,len(table.find_all('tr')) )) # I know the size 
    
# row_marker = 0

# for row in table.find_all('tr'):
#     column_marker = 0
#     columns = row.find_all('td')
#     for column in columns:
#         if(column_marker == 0):
#             new_table.iat[row_marker,column_marker] = column.find('abbr').get_text()
#         else:
#             new_table.iat[row_marker,column_marker] = column.get_text()
#         column_marker += 1
    
#     row_marker += 1
    
# new_table


# In[78]:


# new_table['W-D-L'] = new_table['Won'].astype(str) +'-'+ new_table['Draw'] + '-'+ new_table['Lost']

# new_table = new_table[['Team','Played','Points','W-D-L','GD']]


# In[8]:


club_map_isl = {'BFC': '[](/Bengaluru)', 'NEU':'[](/NorthEast-United)', 'GOA':'[](/Goa)', 
            'MUM':'[](/Mumbai-City)', 'JAM':'[](/Jamshedpur)', 'ATK':'[](/ATK)', 'KER':'[](/Kerala-Blasters)',
           'CHE':'[](/Chennaiyin)', 'PUNE':'[](/Pune-City)', 'DEL':'[](/Delhi-Dynamos)'}


# In[9]:


club_map_ileague = {'CHE':'[](/Chennai-City)',
'QEB': '[](/East-Bengal)',
'MOH': '[](/Mohun-Bagan)',
'GOK': '[](/Gokulam)',
'NER': '[](/NEROCA)',
'MIN': '[](/Minerva-Punjab)',
'RKFC': '[](/Real-Kashmir)',
'CHU': '[](/Churchill-Brothers)',
'SHL': '[](/Shillong-Lajong)',
'IAR': '[](/Indian-Arrows)',
'AIZ': '[](/Aizawl)'}


# In[13]:


def print_isl_table():
    new_table= make_table(isl_url)
    for p in range(0,len(new_table.columns)):
        if(p!= len(new_table.columns) - 1):
            print new_table.columns[p], '|',
        else:
            print new_table.columns[p]

    print ':------|:-------:|:-----:|:----:|:-----:|:-----:|:------:|'

    for r in range(0, len(new_table)):
        for c in range(0, len(new_table.columns)):
            if(c!= len(new_table.columns) - 1):
                if(c == 0):
                    print club_map_isl[new_table.iloc[r,c]] + new_table.iloc[r,c], '|',
                else:
                    print new_table.iloc[r,c], '|',
            else:
                print new_table.iloc[r,c]
    #     print


# In[11]:


def print_ileague_table():
    new_table= make_table(ileague_url)
    for p in range(0,len(new_table.columns)):
        if(p!= len(new_table.columns) - 1):
            print new_table.columns[p], '|',
        else:
            print new_table.columns[p]

    print ':------|:-------:|:-----:|:----:|:-----:|:-----:|:------:|'

    for r in range(0, len(new_table)):
        for c in range(0, len(new_table.columns)):
            if(c!= len(new_table.columns) - 1):
                if(c == 0):
                    print club_map_ileague[new_table.iloc[r,c]] + new_table.iloc[r,c], '|',
                else:
                    print new_table.iloc[r,c], '|',
            else:
                print new_table.iloc[r,c]
    #     print


# In[14]:


print_isl_table()


# In[12]:


print_ileague_table()

