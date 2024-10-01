import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import calendar

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=["date"], index_col="date")

# Clean data
inferior = df['value'].quantile(0.025)
superior = df['value'].quantile(0.975)

df = df[(df['value'] >= inferior) & (df['value'] <= superior)].copy()


def draw_line_plot():
    # Draw line plot
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df['value'], color='r', linewidth=1)
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    


    fig = plt.gcf()
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copiar e modificar os dados para o gráfico de barras mensais
    df_bar = df.copy()
    df_bar['year'] = df.index.year
    df_bar['month'] = df.index.month

    # Certifique-se de que os meses são válidos e mapeie para nomes completos
    df_bar['month'] = df_bar['month'].apply(lambda x: calendar.month_name[x] if 1 <= x <= 12 else None)

    # Agrupar por 'year' e 'month' e calcular a média
    df_grouped = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Reordenar as colunas para garantir que os meses apareçam na ordem correta
    months_order = list(calendar.month_name[1:])  # ['January', 'February', ..., 'December']
    df_grouped = df_grouped[months_order]

    # Inicializar a figura
    fig = plt.figure(figsize=(12, 8))
    
    # Desenhar o gráfico de barras
    df_grouped.plot(kind='bar', stacked=False, ax=plt.gca())

    # Adicionar rótulos e título
    plt.xlabel('Years', fontweight='bold', fontsize=15)
    plt.ylabel('Average Page Views', fontweight='bold', fontsize=15)
    plt.title('Average Daily Page Views per Month (2016-2019)', fontweight='bold', fontsize=16)

    # Ajustar a legenda para mostrar os nomes dos meses
    plt.legend(title='Months', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Salvar a imagem e retornar a figura
    fig.savefig('bar_plot.png')
    return fig



def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    order_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
   
    fig, ax = plt.subplots(1, 2, figsize=(15, 6))

    
    sns.boxplot(x='year', y='value', data=df_box, ax=ax[0])
    ax[0].set_title('Year-wise Box Plot (Trend)')
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Page Views')

   
    sns.boxplot(x='month', y='value', data=df_box, ax=ax[1], order=order_months)
    ax[1].set_title('Month-wise Box Plot (Seasonality)')
    ax[1].set_xlabel('Month')
    ax[1].set_ylabel('Page Views')

  
    plt.tight_layout()
    




    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
