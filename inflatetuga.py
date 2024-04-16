import struct
from optparse import OptionParser
import requests
import random

parser = OptionParser()
parser.add_option("-f", "--file", dest="input_file",
                  help="Binary name or file path including binary name", metavar="example.com")
parser.add_option("-s", "--size", dest='inflate_size',
                  help="Size in MB to inflate binary by", metavar="10", type=int)
(options, args) = parser.parse_args()

def get_random_word():
    # Substitua 'random' pelo endpoint correto se necessário.
    response = requests.get('https://api.dicionario-aberto.net/random')
    if response.status_code == 200:
        word_data = response.json()
        # Ajuste a chave de acordo com a estrutura da resposta da API.
        return word_data['word']
    else:
        return 'palavra'  # palavra padrão em caso de falha na API

def transform(file, size):
    print("[!]\tInflating %s by %s MB" % (file, size))
    words = [get_random_word() for _ in range(1000)]
    # Adiciona um espaço entre cada palavra. Note que o espaço é adicionado como parte da string aqui.
    append_str = ' '.join(words)
    # A string resultante é então convertida para bytes.
    append_bytes = append_str.encode()
    sequence_length = len(append_bytes)
    total_bytes = 1024 * 1024 * size
    repetitions = total_bytes // sequence_length
    remaining_bytes = total_bytes % sequence_length

    transformer = open(file, 'ab')
    transformer.write(append_bytes * repetitions)
    if remaining_bytes:
        transformer.write(append_bytes[:remaining_bytes])
    transformer.close()
    print("[!]\tOperation Complete...\n")

if not options.input_file or not options.inflate_size:
    print("[ERROR] - Enter an input file and an inflation size in MB.\n\n"
          "$ python -f c:\\tools\\mimikatz.exe -s 100\n"
          "$ python -f mimikatz.exe -s 250\n\n")
else:
    transform(options.input_file, options.inflate_size)
