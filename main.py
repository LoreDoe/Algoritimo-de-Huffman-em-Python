import math

# Função para contar a frequência de cada caractere no texto.
def contar_frequencia(texto):
  freq_mapa = {}
  for caractere in texto:
    if caractere in freq_mapa:
      freq_mapa[caractere] += 1
    else:
      freq_mapa[caractere] = 1

  return freq_mapa

# Função para construir a árvore de Huffman a partir das frequências.
def construir_huffman(texto):
  freq_mapa = contar_frequencia(texto)
  nos = []
  for caractere in freq_mapa:
    frequencia = freq_mapa[caractere]
    nos.append((caractere, frequencia, '', ''))

  while len(nos) > 1:

    no_esquerda = nos[0]
    for elemento in nos:
      if elemento[1] < no_esquerda[1]:
        no_esquerda = elemento
    nos.remove(no_esquerda)

    no_direita = nos[0]
    for elemento in nos:
      if elemento[1] < no_direita[1]:
        no_direita = elemento
    nos.remove(no_direita)

    freq_combinada = no_esquerda[1] + no_direita[1]
    no_combinado = (None, freq_combinada, no_esquerda, no_direita)

    nos.append(no_combinado)

  return nos[0]

# Função para construir a tabela de Huffman a partir da árvore de Huffman.
def construir_tabela_huffman(raiz):
  tabela_huffman = {}

  # Função interna para percorrer a árvore e construir a tabela.
  def percorrer_arvore(no, codigo):
    if no[0] is not None:
      tabela_huffman[no[0]] = (no[1], codigo)
    else:
      percorrer_arvore(no[2], codigo + '0')
      percorrer_arvore(no[3], codigo + '1')

  percorrer_arvore(raiz, '')

  return tabela_huffman

# Função para compactar o texto usando a codificação de Huffman.
def compactar(texto):
  raiz = construir_huffman(texto)
  tabela_huffman = construir_tabela_huffman(raiz)
  texto_compactado = ''
  for caractere in texto:
    texto_compactado += tabela_huffman[caractere][1]

  return texto_compactado, raiz, tabela_huffman

# Função para descompactar o texto usando a árvore de Huffman.
def descompactar(texto_compactado, raiz):
  no_atual = raiz
  texto_descompactado = ''

  for bit in texto_compactado:
    if bit == '0':
      no_atual = no_atual[2]
    else:
      no_atual = no_atual[3]
    if no_atual[0] is not None:
      texto_descompactado += no_atual[0]
      no_atual = raiz

  return texto_descompactado

# Função para compactar o texto usando a codificação ASCII.
def compactar_ascii(texto):
  freq_mapa = contar_frequencia(texto)
  tabela_mapeamento = {}

  for caractere in freq_mapa:
    codigo_binario = bin(ord(caractere))[2:].zfill(8)
    tabela_mapeamento[caractere] = (freq_mapa[caractere], codigo_binario)

  texto_compactado = ''
  for caractere in texto:
    texto_compactado += tabela_mapeamento[caractere][1]

  return texto_compactado, tabela_mapeamento

# Função principal do programa.
def main():
  # Texto original.
  texto = 'Olá, Mundo'

  # Compacta o texto usando Huffman e ASCII.
  texto_compactado, raiz, tabela_huffman = compactar(texto)
  texto_compactado_ascii, tabela_ascii = compactar_ascii(texto)

  # Imprime informações.
  print(f'Texto original: {texto} \n')
  print(f'Texto compactado: {texto_compactado} \n')
  print(f'Texto compactado ASCII: {texto_compactado_ascii} \n')
  print('Tabela de Huffman:')

  # Imprime a tabela de Huffman.
  for caractere, (frequencia, codigo) in tabela_huffman.items():
    print(f'Caractere: {caractere}, Frequência: {frequencia}, Código: {codigo}')
  print()

  print('Tabela em ASCII:')
  for caractere in tabela_ascii:
        frequencia, codigo = tabela_ascii[caractere]
        print(f'Caractere: {caractere}, Frequência: {frequencia}, Código: {codigo} ')
  print()
  
  # Descompacta o texto usando Huffman.
  texto_descompactado = descompactar(texto_compactado, raiz)
  print(f'Texto descompactado: {texto_descompactado} \n')

  # Calcula e imprime a quantidade de bytes nos textos compactados.
  bits_huffman = len(texto_compactado)
  bytes_huffman = math.ceil(bits_huffman / 8)
  print(f'Bytes no texto compactado (Huffman): {bytes_huffman} bytes')

  bits_ascii = len(texto_compactado_ascii)
  bytes_ascii = math.ceil(bits_ascii / 8)
  print(f'Bytes no texto compactado (ASCII): {bytes_ascii} bytes')

if __name__ == "__main__":
  main()
