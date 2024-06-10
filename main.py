from nicegui import ui

import pandas as pd
from pandas.api.types import is_bool_dtype, is_numeric_dtype

from nicegui import ui

url1="https://people.sc.fsu.edu/~jburkardt/data/csv/hw_200.csv"
df = pd.read_csv(url1,header=0,names=['Index', 'Height', 'Weight'], usecols = [0,1,2])
df = df.assign(BMI = (df['Weight']* 0.4535) / (df['Height']*0.0254)**2).round(2)
print(df)

def update(*, df: pd.DataFrame, r: int, c: int, value):
    df.iat[r, c] = value
    df.to_excel('f.xlsx')
    print("DF",df)
    ui.notify(f'Set ({r}, {c}) to {value}')


ui.button('Загрузить файл Excel', on_click=lambda: ui.download('f.xlsx'))

with ui.grid(rows=len(df.index)+1).classes('grid-flow-col mx-8 mt-8'):
    for c, col in enumerate(df.columns):
        ui.label(col).classes('font-bold')
        for r, row in enumerate(df.loc[:, col]):
            if is_bool_dtype(df[col].dtype):
                cls = ui.checkbox
                print(cls)
            elif is_numeric_dtype(df[col].dtype):
                cls = ui.number
                print(cls)
            else:
                cls = ui.input
            cls(value=row, on_change=lambda event, r=r, c=c: update(df=df, r=r, c=c, value=event.value))

ui.run(uvicorn_logging_level='debug')