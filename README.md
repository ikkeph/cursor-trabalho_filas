# Simulador de filas de atendimento

Trabalho de Programação II (UFSC). Simulação discreta de uma central com filas, atendentes e duas políticas: FIFO e prioridade com anti-starvation.

Este README é provisório.

## Como rodar

Python 3, sem bibliotecas extras.

```bash
# modo aleatório (padrão: 1000 ticks, 3 atendentes, FIFO)
python3 main.py --modo aleatorio --seed 42

# mesma coisa, política com prioridade
python3 main.py --modo aleatorio --politica prioridade --seed 42

# 1 cliente por tick (1000 chegadas)
python3 main.py --modo aleatorio --tempo 1000 --prob-chegada 1.0 --seed 42

# passo a passo no terminal
python3 main.py --modo aleatorio --tempo 50 --verbose --seed 42
```

No fim o programa espera **ENTER**.

## Argumentos

| Argumento | Padrão | O que faz |
|---|---|---|
| `--modo` | obrigatório | `aleatorio` ou `arquivo` |
| `--entrada` | — | CSV no modo arquivo (`id,tipo,chegada,duracao`) |
| `--tempo` | 1000 | duração da simulação no modo aleatório |
| `--atendentes` | 3 | número de guichês |
| `--prob-chegada` | 0.30 | chance de nascer 1 cliente em cada tick |
| `--tempo-min` / `--tempo-max` | 2 / 8 | duração do atendimento |
| `--prioritarios` | 0.20 | fração de clientes prioritários (modo aleatório) |
| `--politica` | `fifo` | `fifo` ou `prioridade` |
| `--seed` | — | deixa o experimento repetível |
| `--verbose` | off | imprime cada chegada e atendimento |

## Políticas

- **FIFO:** todo mundo na mesma fila, ordem de chegada.
- **Prioridade:** fila comum + fila prioritária. Atende até 3 prioritários seguidos e depois força 1 comum (anti-starvation).

## Testes

```bash
python3 -m unittest discover -s testes -v
```

## Estrutura

```
main.py              entrada (argparse)
configuracao.py      opções da linha de comando
simulacao.py         relógio da simulação
central.py           coordena filas, guichês e métricas
politicas.py         FIFO e prioridade
fila.py              fila encadeada
cliente.py / atendente.py
gerador_clientes.py  CSV ou sorteio
relatorio.py         imprime o resumo
dados/               cenários (ainda vazios)
testes/
```

## Observações

- No modo `arquivo`, a simulação roda até o último horário de chegada **+ 100** ticks. Quem ainda estiver na fila ou no guichê não conta como atendido.
- No modo `aleatorio`, para no `--tempo`.
- Pasta `dados/` e comparação formal das políticas ainda vão entrar.
