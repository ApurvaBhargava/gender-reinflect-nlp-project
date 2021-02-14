
import argparse
import time
from googletrans import Translator

TRANSLATOR  = Translator()

def translate(inputs, src, trg):
    translations = []
    for line in inputs:
        translation = TRANSLATOR.translate(text=line, src=src, dest=trg)
        translations.append(translation)
        time.sleep(0.5)

    translated_text = [t.text for t in translations]
    print(translated_text)
    return translated_text

def main():

    p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument('-i', '--input', required=True, help='Input file path')
    p.add_argument('-s', '--source', required=True, help='Source language')
    p.add_argument('-t', '--target', default='en', help='Target language')
    p.add_argument('-o', '--output', default='gt_out.txt', help='Output file path')
    args = p.parse_args()



    with open(args.input, encoding='utf8', mode='r') as f:
        inputs = f.readlines()
        translated_inputs = translate(inputs, src=args.source, trg=args.target)

    output_file = open(args.output, mode='w')
    for line in translated_inputs:
        output_file.write(line)
        output_file.write('\n')
    output_file.close()

if __name__ == '__main__':
    main()