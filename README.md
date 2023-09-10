# PE2LGP: translating Portuguese to Portuguese Sign Language

PE2LGP is a translation system from European Portuguese text into Portuguese sign language. Translator Demo: https://portallgp.ics.lisboa.ucp.pt/tradutor-para-lgp/

## Description

The translation system is divided into two modules. The first module, the construction of translation rules, consists in extracting linguistic information from the Portuguese Sign Language reference corpus and, based on this this information, creating automatic rules. The second module, the machine translation, consists in the translation of a European Portuguese text into Portuguese Sign Language (LGP), in which the LGP sentence is represented by a sequence of glosses, a sequence of visemes separated by syllables for each gloss, and the identification of additional linguistic aspects (e.g., composite utterances, pauses and facial expressions). The translation is based on automatic rules and manual rules.

We also provide the script for the automatic evaluation of the translation system, using the TER and BLEU measurements.

## Requirements

**To execute PE2LGP:**

1. Install Python 3


2. Install all necessary Python libraries:

```bash
pip install -r requirements.txt
```

3. Install the library [Freeling 4.1](https://freeling-user-manual.readthedocs.io/en/v4.1/toc/)
  3.1. Install Freeling Requirements:
  ```bash
  sudo apt-get install build-essential
  sudo apt-get install cmake
  sudo apt install libboost-all-dev
  sudo apt-get -y install swig
  ```
  3.2. Download Freeling folder from source and then Build FreeLing:
    ```bash
  mkdir build
  cd build
  cmake .. -DPYTHON3_API=ON
  make install
  ```



4. Download SpaCy pre-trained model for dependency analysis:

```bash
python -m spacy download pt_core_news_sm
```


**To execute the automatic evaluation script:**

1. Install Python 2

2. Install the library [pyter](https://pypi.org/project/pyter/):


```bash
pip2 install pyter
```


## Execute Project (Ubuntu)

**Construction of Translation Rules Module**
```bash
cd Modulo_construcao_regras
python3 criacao_regras_automaticas.py ficheiro.html
```

`ficheiro.html` is the html file exported from ELAN. An example of this file is in `/modulo_construcao_regras/Corpus/exemplo.html`


**Machine Translation**
1. Uncomment the last 6 lines in script "tradutor.py"
```bash
cd Modulo_tradutor
python3 tradutor.py
```

**Machine Translation with server**
1. Comment the last 6 lines in script "tradutor.py"
```bash
cd Modulo_tradutor
python3 server.py
```

**Automatic Evaluation**
```bash
cd Avaliacao
python aval_automatica.py corpus_teste.csv traducoes.csv
```

`corpus_teste.csv` is the file that contains the test corpus. The test corpus used in the evaluation of the system can be found in `/Avaliacao/corpus_teste.csv`.

`traducoes.csv` is the file with the translations of the Portuguese sentences from the test corpus in the machine translation system. This file can be found in `/Avaliacao/traducoes.csv`.

**Enter Virtual Machine**
- install "virt-viewer" -- https://virt-manager.org/download/sources/virt-viewer/virt-viewer-x64-2.0.msi
- Create SSL Tunnel to address: "localhost:5920":
```bash
sudo ssh -f -L localhost:5920:v07.hlt.inesc-id.pt:5900 username@ssh.hlt.inesc-id.pt -N
```
- Open "virt-viewer"
  - Type "spice://localhost:5920" 

##### Error: "Could not resolve host: github.com" or Error: "Temporary failure resolving..." in "sudo apt install/update"
- add "nameserver 8.8.8.8" in "etc/resolv.conf":
```bash
  echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf > /dev/null
```


## Contactos

Developed by:
- Matilde Gonçalves, matilde.do.carmo.lages.goncalves@tecnico.ulisboa.pt
- Inês Lacerda, ines.lacerda@tecnico.ulisboa.pt
