from nicegui import ui
import pandas as pd
from pandas.api.types import is_bool_dtype, is_numeric_dtype

url1="https://people.sc.fsu.edu/~jburkardt/data/csv/hw_200.csv"
df = pd.read_csv(url1,header=0,names=['Index', 'Height', 'Weight'], usecols = [0,1,2])
#df = df.assign(BMI = (df['Weight']* 0.4535) / (df['Height']*0.0254)**2).round(2)
df['BMI'] = round(df.Weight / df.Height**2*703,1)
print(df)

def update(*, df: pd.DataFrame, r: int, c: int, value):
    df.iat[r, c] = value 
    upbmi = round(df.iat[r,2] / df.iat[r,1]**2*703,1)
    df.iat[r,3]=upbmi 
    bmihtml[r].content=str(upbmi)                               
    df.to_excel('f.xlsx') 

ui.button('Загрузить файл Excel', on_click=lambda: ui.download('f.xlsx'))
sb=df.BMI
print(df.iloc[[0],[3]]['BMI'][0])

bmihtml={}
with ui.grid(rows=len(df.index)+1).classes('grid-flow-col mx-1 mt-1 items-center'):
    for c, col in enumerate(df.columns):
        ui.label(col).classes('font-bold')
        for r, row in enumerate(df.loc[:, col]):
            if c == 0 :
                ui.html(f'{df.iloc[r,c]}',tag='div') 
            elif c == 3:
                bmi = ui.html(f'{df.iloc[r,c]}').classes('grid-flow-col mx-1 mt-1 items-center') 
                bmihtml[r] = bmi 
            elif c in (1, 2): 
                cls = ui.number
                cls(value=row,on_change=lambda event, r=r, c=c: update(df=df, r=r, c=c, value=event.value))

ui.run(uvicorn_logging_level='info')