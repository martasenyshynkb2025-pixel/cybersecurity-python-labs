import df
from sympy.physics.quantum.circuitplot import np

df['Profit_per_Employee'] = df['Profit_Numeric'] / df['Employees_Numeric']

     df .replace([ np.inf, -np.inf], np.nan, inplace=True)

    df_n = df.dropna(subset=['Profit_per_Employee']).sort_values(by='Profit_per_Employee', ascending=True).head(10)

    df_n['$ Profit per Employee'] = df_n['Profit_per_Employee'].apply(lambda x: f"{x:,.2f}")

    display_df_n = df_n[[
        column_map['Name'],
        column_map['Profit'],
        column_map ['Employees'],
        '$ Profit per Employee'
    ]].reset_index(drop=True)

    display_rich_table(
        "n. Найгірші 10 компаній за співвідношенням прибуток/співробітник (Bottom 10 by Profit per Employee)",
        display_df_n)


if name == "__main__":
    main()