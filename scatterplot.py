import pandas as pd
import matplotlib.pyplot as plt


def ajustaListas(disciplinas_list, x_ax_list):

    global flagNovaTurma
    flagNovaTurma = 1  # liga o flag
    disciplinas_list.pop()  # retira a última disciplina da lista
    x_ax_list.pop()  # retira a última nota da lista x_ax também


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
    flagNovaTurma = 1

    # faz as listas x y para plot
    for index, row in media_df_agrupado.iterrows():
        if row['Turma'] == 'A' and flagNovaTurma == 1:  # nova disciplina para comparar
            disciplinas.append(row['Disciplina'])  # adiciona essa disciplina na lista
            x_ax.append(row[questao])  # adiciona a nota da questao na lista
            flagNovaTurma = 0

        elif row['Turma'] == 'A' and flagNovaTurma == 0:  # a disciplina anterior só tinha turma A
            ajustaListas(disciplinas, x_ax)

        elif row['Turma'] == 'B' and flagNovaTurma == 0:  # disciplina já foi adicionada na lista
            y_ax.append(row[questao])  # adiciona a nota da questao na lista
            flagNovaTurma = 1

    if flagNovaTurma == 0:  # caso o último elemento da lista tiver somente turma A
        ajustaListas(disciplinas, x_ax)

    plt.scatter(x=x_ax, y=y_ax, c='r', s=12)
    plt.grid()
    plt.xlabel('Nota média turma A')
    plt.ylabel('Nota média turma B')
    plt.title('Comparação das disciplinas em 20xx-x com duas turmas')

    # anota o que cada ponto no gráfico representa, ou seja, o nome das disciplinas
    for i, txt in enumerate(disciplinas):
        plt.text(x_ax[i], y_ax[i], txt, fontsize=5, horizontalalignment='center',
                 verticalalignment='bottom')

    plt.savefig(questao + '.png', bbox_inches='tight')
    plt.close()
