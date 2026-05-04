# CEP — Controle Estatístico de Processo

Análise completa de capacidade e estabilidade de processo.

## Indicadores calculados
- **Cp** — Capacidade Potencial
- **Cpk** — Capacidade Real
- **Cpu / Cpl** — Capacidade Superior / Inferior
- **X̄** — Média do processo
- **R̄** — Amplitude média
- **σ** — Desvio padrão (within)
- **UCL / LCL** — Limites de controle
- **PPM** — Estimativa de não conformidades
- Regras de Nelson (instabilidade)

## Deploy no Streamlit Community Cloud

1. Fork ou suba este repositório no GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Clique em **"New app"**
4. Selecione o repositório
5. Main file: `cep_app.py`
6. Clique **Deploy**

## Rodar localmente

```bash
pip install -r requirements.txt
streamlit run cep_app.py
```
