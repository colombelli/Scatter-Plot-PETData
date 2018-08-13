import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('AvalDiscente_20xx-x.csv', sep=';', encoding='utf-8')

header = list(df.columns.values)  # cria um lista com o nome das colunas

# pegando header[2:-1] pegamos apenas as 11 questões (que começam no terceiro item,2, e vão até o penúltimo, -1)
for i in header[2:-1]:
    # no lugar de vírgula, inserimos ponto para calcular a média corretamente
    df[i] = df[i].str.replace(",", ".")
    # converte os valores para float para poder calcular a média
    df[i] = df[i].astype(float)

# pega as médias de da chave (disciplina, turma) retornando outro dataframe no padrão "SQL-style"
media_df_agrupado = df.groupby(['Disciplina', 'Turma'], as_index=False).mean(numeric_only=True)

# deleta tamanho da turma
del media_df_agrupado['TamTurma']

# print(media_df_agrupado.to_string())


# separa os dados para comparar as notas médias entre turmas A e B da mesma disciplina
for questao in header[2:-1]:  # montar um gráfico por questão

    disciplinas = []  # lista de disciplinas no gráfico
    x_ax = []  # eixo x do plot
    y_ax = []  # eixo y do plot

    # faz as listas x y para plot
    for index, row in media_df_agrupado.iterrows():
        if row['Turma'] == 'A':  # nova disciplina para comparar
            disciplinas.append(row['Disciplina'])  # adiciona essa disciplina na lista
            x_ax.append(row[questao])  # adiciona a nota da questao na lista

        elif row['Turma'] == 'B':  # disciplina já foi adicionada na lista
            y_ax.append(row[questao])  # adiciona a nota da questao na lista

    plt.scatter(x=x_ax, y=y_ax, c='r')
    plt.grid()
    plt.xlabel('Nota média turma A')
    plt.ylabel('Nota média turma B')
    plt.title('Comparação das disciplinas em 20xx-x com duas turmas')

    # anota o que cada ponto no gráfico representa, ou seja, o nome das disciplinas
    for i, txt in enumerate(disciplinas):
        plt.annotate(txt, (x_ax[i], y_ax[i]))

    plt.savefig(questao + '.png', bbox_inches='tight')
    plt.close()
