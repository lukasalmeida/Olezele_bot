# Olezele Bot

![Discord](https://img.shields.io/badge/discord-olezele-orange?logo=discord)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-online-brightgreen)

[Instale em seu servidor Discord](https://discord.com/oauth2/authorize?client_id=1501397537607913542&permissions=8&integration_type=0&scope=bot+applications.commands)

Bot de Discord desenvolvido em Python com sistema de tickets,
logs, moderação e arquitetura escalável.

---

## Instalação

```bash
git clone https://github.com/lukasalmeida/olezelebot.git
```

```bash
cd olezelebot
```

```bash
pip install -r requirements.txt
```

## Configuração

Crie um arquivo `.env`

```env
TOKEN=seu_token
DATABASE_URL=postgresql://user:password@localhost:5432/db
```

## Executando o projeto

```bash
python main.py
```

## Estrutura

src/
├── asset/
├── cogs/
├── database/
├── views/
└── models/
└── utils/

## Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

![Banner](./asset/img/logo_olezelebot.png)
