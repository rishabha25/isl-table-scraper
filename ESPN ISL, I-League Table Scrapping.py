
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
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


# %%
def parse_html_table(table):
        n_columns = 0
        n_rows=0
        column_names = []

        # Find number of rows and columns
        # we also find the column titles if we can
        for row in table.find_all('tr'):
            
            # Determine the number of rows in the table
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows+=1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)
                    
            # Handle column names if we find them
            th_tags = row.find_all('th') 
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    column_names.append(th.get_text())

        # Safeguard on Column Titles
        if len(column_names) > 0 and len(column_names) != n_columns:
            raise Exception("Column titles do not match the number of columns")

        columns = column_names if len(column_names) > 0 else range(0,n_columns)
        df = pd.DataFrame(columns = columns,
                            index= range(0,n_rows))
        row_marker = 0
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                df.iat[row_marker,column_marker] = column.get_text()
                column_marker += 1
            if len(columns) > 0:
                row_marker += 1
                
        # Convert to float if possible
        # for col in df:
        #     try:
        #         df[col] = df[col].astype(float)
        #     except ValueError:
        #         pass
        
        return df

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


def print_isl_table(new_table):
    # new_table= make_table(isl_url)
    for p in range(0,len(new_table.columns)):
        if(p!= len(new_table.columns) - 1):
            print (new_table.columns[p], '|', end='')
        else:
            print (new_table.columns[p],'\n', end='')

    print (':------|:-------:|:-----:|:----:|:-----:|','\n', end='')

    for r in range(0, len(new_table)):
        for c in range(0, len(new_table.columns)):
            if(c!= len(new_table.columns) - 1):
                # if(c == 0):
                #     print (club_map_isl[new_table.iloc[r,c]] + new_table.iloc[r,c], '|',)
                # else:
                #     print (new_table.iloc[r,c], '|',)
                 print (new_table.iloc[r,c], '|', end='')
            else:
                print (new_table.iloc[r,c],'\n', end='')
    #     print


# In[11]:


def print_ileague_table():
    new_table= make_table(ileague_url)
    for p in range(0,len(new_table.columns)):
        if(p!= len(new_table.columns) - 1):
            print (new_table.columns[p], '|',)
        else:
            print (new_table.columns[p])

    print (':------|:-------:|:-----:|:----:|:-----:|:-----:|:------:|')

    for r in range(0, len(new_table)):
        for c in range(0, len(new_table.columns)):
            if(c!= len(new_table.columns) - 1):
                # if(c == 0):
                #     print club_map_ileague[new_table.iloc[r,c]] + new_table.iloc[r,c], '|',
                # else:
                #     print new_table.iloc[r,c], '|',
                print (new_table.iloc[r,c], '|',)
            else:
                print (new_table.iloc[r,c])
    #     print


# %% 

r = requests.get(isl_url)

# %%

soup = BeautifulSoup(r.text, 'lxml')

# %%

table = soup.find_all('table')[0]


#%%

teams_list = []
for row  in table.find('tbody').find_all('tr'):
    print('\n')
    print(row.find('span', {'class' : 'hide-mobile'}).get_text())
    teams_list.append(row.find('span', {'class' : 'hide-mobile'}).get_text())



# %%


table2 = soup.find_all('table')[1]

# %%

isl_table = parse_html_table(table2)

# %%
isl_table['Team'] = teams_list

# %%
isl_table['W-D-L'] = isl_table['W'].astype(str) +'-'+ isl_table['D'] + '-'+ isl_table['L']

# %%
isl_table = isl_table[['Team', 'GP', 'W-D-L', 'GD', 'P']]

# %%
isl_table.rename(columns={'P':'Pts'}, inplace=True)

# %%

print_isl_table(isl_table)
