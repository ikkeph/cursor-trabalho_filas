# Simulador de filas de atendimento

Trabalho de Programação II (UFSC). Simulação discreta de uma central de atendimento:
clientes chegam, entram na fila da disciplina, são atendidos e o programa imprime métricas.
Duas políticas: FIFO e prioridade com anti-starvation (3 prioritários seguidos, depois 1 comum).

Python 3, sem bibliotecas extras.

## Como rodar

```bash
python3 main.py --help

# modo aleatório (padrão: 1000 ticks, 3 atendentes, FIFO)
python3 main.py --modo aleatorio --seed 42

python3 main.py --modo aleatorio --politica prioridade --seed 42

# passo a passo no terminal
python3 main.py --modo aleatorio --tempo 50 --verbose --seed 42

# cenários em arquivo
python3 main.py --modo arquivo --entrada dados/cenario1.csv --atendentes 3 --politica fifo
python3 main.py --modo arquivo --entrada dados/cenario2.csv --atendentes 2 --politica prioridade
python3 main.py --modo arquivo --entrada dados/cenario3.csv --atendentes 3 --politica fifo

# experimento do enunciado (mesma demanda, muda o N de mesas)
python3 main.py --modo aleatorio --tempo 10000 --atendentes 2 --seed 42
```
## Argumentos

| Argumento | Padrão | O que faz |
|---|---|---|
| `--modo` | obrigatório | `aleatorio` ou `arquivo` |
| `--entrada` | — | CSV no modo arquivo (`id,tipo,chegada,duracao`) |
| `--tempo` | 1000 | duração no modo aleatório |
| `--atendentes` | 3 | número de guichês |
| `--prob-chegada` | 0.30 | chance de 1 cliente por tick (aleatório) |
| `--tempo-min` / `--tempo-max` | 2 / 8 | duração do atendimento |
| `--prioritarios` | 0.20 | fração de prioritários (aleatório) |
| `--politica` | `fifo` | `fifo` ou `prioridade` |
| `--seed` | — | deixa o sorteio repetível |
| `--verbose` | off | imprime cada chegada e atendimento |

`--modo arquivo` exige `--entrada`. Valores inválidos (atendente ≤ 0, probabilidade fora de [0,1], etc.) encerram com mensagem.

`main.py` só chama `Configuracao.parse_args()` e `Simulacao.executar()`.
A espera usa a `Fila` da disciplina (interface pública: `enfileira`, `desinfileira`, `vazia`, `cabeca`, `tamanho`).

## Políticas

- **FIFO:** todo mundo na `fila_comum`, ordem de chegada. A `fila_prioritaria` fica vazia.
- **Prioridade:** prioritário na `fila_prioritaria`, o resto na comum. Depois de 3 prioritários seguidos, se houver comum esperando, atende o comum. Se a comum estiver vazia, segue no prioritário (o contador passa de 3).


## Testes

```bash
python3 -m unittest discover -s testes -v
```

- `test_cliente.py` — criação, espera, validações, `eh_prioritario`
- `test_atendente.py` — livre → ocupado → termina em 2 ticks
- `test_central.py` — FIFO e anti-starvation
- `test_simulacao.py` — cenário com `--seed 42`; conservação: chegaram = atendidos + fila + na mesa

## Estrutura

```
main.py              argparse + inicialização
configuracao.py      lê a linha de comando e valida
simulacao.py         monta o cenário e anda o relógio
central.py           um tick: chega, termina, ocupa mesa
politicas.py         FIFO e prioridade
fila.py              fila da disciplina
cliente.py / atendente.py
gerador_clientes.py  CSV ou sorteio
estatisticas.py      contas do enunciado
relatorio.py         imprime o resumo
dados/               cenario1.csv, cenario2.csv, cenario3.csv
testes/
```

## Observações

- Modo `arquivo`: para no último horário de chegada **+ 100** ticks (folga, não “roda até esvaziar”).
- Modo `aleatorio`: para no `--tempo`.
- O aleatório nasce no máximo 1 cliente por tick; o CSV pode ter vários no mesmo horário.
