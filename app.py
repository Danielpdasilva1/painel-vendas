from flask import Flask, render_template_string
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

data = [
    {"VENDEDOR": "João", "CLIENTE": "Empresa A", "PRODUTO": "Produto X", "VALOR_MERCADORIA": 1500.00, "DATA_EMISSAO": "2024-01-15"},
    {"VENDEDOR": "Maria", "CLIENTE": "Empresa B", "PRODUTO": "Produto Y", "VALOR_MERCADORIA": 2300.00, "DATA_EMISSAO": "2024-02-10"},
    {"VENDEDOR": "Carlos", "CLIENTE": "Empresa C", "PRODUTO": "Produto Z", "VALOR_MERCADORIA": 1800.00, "DATA_EMISSAO": "2024-02-20"},
    {"VENDEDOR": "João", "CLIENTE": "Empresa D", "PRODUTO": "Produto X", "VALOR_MERCADORIA": 1200.00, "DATA_EMISSAO": "2024-03-05"},
]

df = pd.DataFrame(data)
df["DATA_EMISSAO"] = pd.to_datetime(df["DATA_EMISSAO"])
df["MES"] = df["DATA_EMISSAO"].dt.strftime("%b")

monthly_sales = df.groupby("MES")["VALOR_MERCADORIA"].sum()
fig, ax = plt.subplots()
monthly_sales.plot(kind='bar', ax=ax)
ax.set_title("Vendas por Mês")
ax.set_ylabel("Valor Total (R$)")
plt.tight_layout()

img = io.BytesIO()
plt.savefig(img, format='png')
img.seek(0)
plot_url = base64.b64encode(img.getvalue()).decode()

template = """
<!DOCTYPE html>
<html>
<head>
    <title>Painel de Vendas</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        img { max-width: 600px; }
    </style>
</head>
<body>
    <h1>Painel de Vendas</h1>
    <h2>Gráfico de Vendas por Mês</h2>
    <img src="data:image/png;base64,{{ plot_url }}" alt="Gráfico de Vendas">
    <h2>Tabela de Vendas</h2>
    <table>
        <tr>
            <th>Vendedor</th>
            <th>Cliente</th>
            <th>Produto</th>
            <th>Valor da Mercadoria</th>
            <th>Data de Emissão</th>
        </tr>
        {% for row in data %}
        <tr>
            <td>{{ row.VENDEDOR }}</td>
            <td>{{ row.CLIENTE }}</td>
            <td>{{ row.PRODUTO }}</td>
            <td>R$ {{ "%.2f"|format(row.VALOR_MERCADORIA) }}</td>
            <td>{{ row.DATA_EMISSAO.strftime("%d/%m/%Y") }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(template, plot_url=plot_url, data=df.to_dict(orient='records'))

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
