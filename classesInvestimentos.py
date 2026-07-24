
INDICADORES= (
    "BenchMark Personalizado - > 105% DO CDI "
    "BenchMark Personalizado -> ÍNDICE IPCA + 5,00% "
    "BenchMark Personalizado -> ÍNDICE INPC + 5,25% "
    "ÍNDICES - > CDI "
    "ÍNDICES - > IBOVESPA "
    "ÍNDICES - > IFIX"
)

classes = [
    {
    'INDICADORES':[]
    },
    {
        'Renda Fixa': [
            'Renda Fixa',
            'Renda Fixa Crédito',
            'Renda Fixa Crédito Livre',
            'Renda Fixa Dívida Externa',
            'Renda Fixa Duração Alta Crédito Livre',
            'Renda Fixa Duração Alta Grau de Investimento',
            'Renda Fixa Duração Alta Soberano',
            'Renda Fixa Duração Baixa Crédito Livre',
            'Renda Fixa Duração Baixa Grau de Investimento',
            'Renda Fixa Duração Baixa Soberano',
            'Renda Fixa Duração Livre Crédito Livre',
            'Renda Fixa Duração Livre Grau de Investimento',
            'Renda Fixa Duração Livre Soberano',
            'Renda Fixa Duração Média Crédito Livre',
            'Renda Fixa Duração Média Grau de Investimento',
            'Renda Fixa Duração Média Soberano',
            'Renda Fixa Indexados',
            'Renda Fixa Índices',
            'Renda Fixa Investimento no Exterior',
            'Renda Fixa Médio e Alto Risco',
            'Renda Fixa Multi Índices',
            'Renda Fixa Simples',
            'Curto Prazo',
        ]
    },
    {
        'Renda Fixa Liquidez': [
            'Renda Fixa',
            'Renda Fixa Crédito',
            'Renda Fixa Crédito Livre',
            'Renda Fixa Dívida Externa',
            'Renda Fixa Duração Alta Crédito Livre',
            'Renda Fixa Duração Alta Grau de Investimento',
            'Renda Fixa Duração Alta Soberano',
            'Renda Fixa Duração Baixa Crédito Livre',
            'Renda Fixa Duração Baixa Grau de Investimento',
            'Renda Fixa Duração Baixa Soberano',
            'Renda Fixa Duração Livre Crédito Livre',
            'Renda Fixa Duração Livre Grau de Investimento',
            'Renda Fixa Duração Livre Soberano',
            'Renda Fixa Duração Média Crédito Livre',
            'Renda Fixa Duração Média Grau de Investimento',
            'Renda Fixa Duração Média Soberano',
            'Renda Fixa Indexados',
            'Renda Fixa Índices',
            'Renda Fixa Investimento no Exterior',
            'Renda Fixa Médio e Alto Risco',
            'Renda Fixa Multi Índices',
            'Renda Fixa Simples',
            'Curto Prazo',
            'Referenciado DI',
            'Referenciado Outros',
        ]
    },
    
    {
        'Long and Short': [
            'Long and Short Direcional',
            'Long and Short Neutro',
            'Long and Short Renda Variável',
        ]
    },
    {
        'Multimercado': [
            'Balanceados',
            'Cambial',
            'Cambial Dólar sem alavancagem',
            'Cambial Euro sem Alavancagem',
            'Capital Protegido',
            'Multimercados Balanceados',
            'Multimercados Capital Protegido',
            'Multimercados com RV',
            'Multimercados com RV com Alavancagem',
            'Multimercados Dinâmico',
            'Multimercados Estratégia Específica',
            'Multimercados Investimento no Exterior',
            'Multimercados Juros e Moedas',
            'Multimercados Livre',
            'Multimercados Long and Short Direcional',
            'Multimercados Long and Short Neutro',
            'Multimercados Macro',
            'Multimercados Multiestratégia',
            'Multimercados Multigestor',
            'Multimercados sem RV',
            'Multimercados sem RV com Alavancagem',
            'Multimercados Trading',
            'Referenciado Dólar',
        ]
    }
    ,
    {
        'FIDC': [
            'FIDC Agro Indústria e Comércio',
            'FIDC Financeiro',
            'FIDC Fomento Mercantil',
            'FIDC Outros',
            'Direitos Creditórios',
        ]
    },
    {
        'Renda Variável': [
            'Ações Dividendos',
            'Ações fechado',
            'Ações FMP - FGTS',
            'Ações Ibovespa ativo',
            'Ações Ibovespa ativo com alavancagem',
            'Ações Ibovespa indexado',
            'Ações IBrX Ativo',
            'Ações IBrX Indexado',
            'Ações IBX ativo',
            'Ações Indexados',
            'Ações Índice Ativo',
            'Ações Livre',
            'Ações outros',
            'Ações Setoriais',
            'Ações Setoriais Livre',
            'Ações Setoriais Privatização Petrobrás - Recursos Próprios',
            'Ações Small Caps',
            'Ações Sustentabilidade/Governança',
            'Ações Valor/Crescimento',
        ]
    },
    {
        'Exterior': [
            'Investimento no Exterior',
            'Ações Investimento no Exterior',
        ]
    },
    {
        'Imobiliários': [
            'FII Desenvolvimento para Renda Gestão Ativa',
            'FII Desenvolvimento para Renda Gestão Passiva',
            'FII Desenvolvimento para Venda Gestão Ativa',
            'FII Desenvolvimento para Venda Gestão Passiva',
            'FII Híbrido Gestão Ativa',
            'FII Híbrido Gestão Passiva',
            'FII Multiestratégia Gestão Ativa',
            'FII Papel Híbrido Gestão Ativa',
            'FII Renda Gestão Ativa',
            'FII Renda Gestão Passiva',
            'FII Tijolo Híbrido Gestão Ativa',
            'FII TVM Gestão Ativa',
            'FII TVM Gestão Passiva',
            'Fundos de Investimento Imobiliário',
        ]
    }
    ]


def tela_lista_e_seleciona_categorias(classes):
    def lista_chaves(classes):
        valores = []
        for classe in classes:
            valores.extend(list(classe.keys()))
        return valores

    def enumera_classes(classes):
        classes_enumeradas = {ordem : cl for ordem,cl in enumerate(lista_chaves(classes), start=1)}
        for ordem,cl in classes_enumeradas.items():
            print(f"{ordem} | {cl}")
        return classes_enumeradas

    classes_enumeradas_retorno = enumera_classes(classes)

    def inputs_usuario():
        entradas = input("Digite os valores associados as classes separados por virgula. Exe: 1,2,3\n")
        if entradas !='0':
            entradas = str(entradas).strip().split(',')
            entradas = [int(e) for e in entradas]
            #print(f"Entradas: {entradas}")
            return entradas
        else:
            entradas = int(entradas)
            print("Rodando todas as classes...")
            return 0

    entradas = inputs_usuario()    

    def lista_classes_associadas_aos_numeros_usuario(classes_enumeradas_retorno,entradas):
        if entradas !=0:
            input_classes = [y for x,y in classes_enumeradas_retorno.items() if x in entradas]
            print(input_classes)
            return input_classes
        else:
            return 0

    classes_usuarios = lista_classes_associadas_aos_numeros_usuario(classes_enumeradas_retorno,entradas)

    def filtra_somente_classes_inputadas_usuario(classes_usuarios,classes):
        if classes_usuarios !=0:
            classes = [x for x in classes if list(x.keys())[0] in classes_usuarios]
            return classes
        return classes
    return filtra_somente_classes_inputadas_usuario(classes_usuarios,classes)
