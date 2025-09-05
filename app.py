import streamlit as st

# Tabela de alíquotas interestaduais para o MT
aliquotas_icms = {
    'AC': 12, 'AL': 12, 'AM': 12, 'AP': 12, 'BA': 12, 'CE': 12, 'DF': 12,
    'ES': 12, 'GO': 12, 'MA': 12, 'MG': 7,  'MS': 12, 'PA': 12, 'PB': 12,
    'PR': 7, 'PE': 12, 'PI': 12, 'RJ': 7,  'RN': 12, 'RO': 12, 'RR': 12,
    'RS': 7,  'SC': 7,  'SP': 7,  'SE': 12, 'TO': 12
}

ufs = list(aliquotas_icms.keys())

st.set_page_config(page_title="Calculadora DIFAL - MT", layout="centered")
st.title("Simulador de ICMS DIFAL para o Estado de Mato Grosso")

st.markdown("Preencha os dados abaixo para calcular o ICMS DIFAL (Diferencial de Alíquota) a ser recolhido:")

# Entrada do valor da compra
valor_compra = st.number_input("Valor Total da Compra (R$)", min_value=0.0, format="%.2f")

# Seleção da UF de origem
uf_origem = st.selectbox("UF de Origem da Mercadoria", options=ufs)

# Simulação de item com conteúdo importado (4%)
conteudo_importado = st.checkbox("Item com conteúdo de importação superior a 40% (alíquota de 4%)")

# Botão para calcular
if st.button("Calcular DIFAL"):
    if valor_compra <= 0:
        st.warning("Informe um valor de compra válido.")
    else:
        aliquota_interna_mt = 17.0
        if conteudo_importado:
            aliquota_interestadual = 4.0
        else:
            aliquota_interestadual = aliquotas_icms.get(uf_origem, 12)

        # Cálculo oficial (base dupla - art. 96 §1º RICMS-MT)
        icms_origem = valor_compra * (aliquota_interestadual / 100)  # imposto na origem
        valor_liquido = valor_compra - icms_origem                   # sem ICMS origem
        base_calculo = valor_liquido / (1 - (aliquota_interna_mt / 100))  # base por dentro
        icms_interno = base_calculo * (aliquota_interna_mt / 100)    # ICMS devido em MT

        # DIFAL é a diferença
        difal = icms_interno - icms_origem
        custo_total = valor_compra + difal

        def format_brl(valor):
            return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        st.success(f"ICMS DIFAL a recolher: {format_brl(difal)}")

        st.markdown(
            f"### Resultado Detalhado\n\n"
            f"Você comprou um item por {format_brl(valor_compra)}.\n\n"
            f"Como a operação é interestadual, será necessário recolher {format_brl(difal)} de ICMS DIFAL ao Estado de Mato Grosso.\n\n"
            f"Portanto, o **custo total efetivo** do item será de {format_brl(custo_total)}."
        )

        st.markdown("---")
        st.markdown(
            f"### Comparativo Estratégico\n\nSe no mercado interno de MT você encontrar o mesmo item por até {format_brl(custo_total)}, "
            f"vale mais a pena comprar **dentro do estado** para evitar o recolhimento do DIFAL."
        )
