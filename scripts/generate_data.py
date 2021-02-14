import argparse


def read_data(path):
    with open(path, encoding='utf8', mode='r') as f:
        return f.readlines()

def generate(indef_arts, def_arts, spros, opros, nouns, templates, 
             lang, output_dir):
    """
    Generates synthetic data by filling the templates
    Args:
        indef_arts: dict of indefinite articles in spanish or french
        def_arts: dict of definite articles in spanish or french
        spors: dict subjective pronouns in spanish or french
        opros: dict objective pronouns in spanish or french
        nouns: dict of masculine and feminine nouns
        templates: list of templates
    """

    outfile = open(output_dir, 'w')
    french_vowels = ['i', 'u', 'o', 'a', 'h', 'e', 'é']
    m_nouns, f_nouns = nouns['m'], nouns['f']

    for i, template in enumerate(templates): # for each template
        template = template.split()
        # words to keep
        words_to_keep = [i for i, w in enumerate(template) if not w.startswith('[')]
        # words to change
        words_to_change = [i  for i, w in enumerate(template) if w.startswith('[')]
        for k, noun in enumerate(m_nouns):
            m_sentence = ['*'] *  len(template)
            f_sentence = ['*'] *  len(template)
            for idx, w in enumerate(words_to_change):
                word_to_change = template[w]

                if word_to_change == '[noun]':
                    m_sentence[w] = m_nouns[k]
                    f_sentence[w] = f_nouns[k]  

                    # handle the special def arts in french
                    if lang == 'fr' and template[w - 1] == '[def_art]':
                        # in our case, the def articles
                        # only comes before nouns

                        if m_nouns[k][0].lower() in french_vowels:

                            m_sentence[w - 1] = def_arts['special']
                        if f_nouns[k][0].lower() in french_vowels:
                            f_sentence[w - 1] = def_arts['special']

                elif word_to_change == '[indef_art]':
                    m_sentence[w] = indef_arts['m']
                    f_sentence[w] = indef_arts['f']

                elif word_to_change == '[def_art]':
                    m_sentence[w] = def_arts['m']
                    f_sentence[w] = def_arts['f']

                elif word_to_change == '[spro]':
                    m_sentence[w] = spros['m']
                    f_sentence[w] = spros['f']

                elif word_to_change == '[opro]':
                    m_sentence[w] = opros['m']
                    f_sentence[w] = opros['f']

            for w in words_to_keep:
                m_sentence[w] = template[w]
                f_sentence[w] = template[w]

            print(m_sentence)
            print(f_sentence)
            if lang == 'fr':
                out_m_sentence = ' '.join(m_sentence).replace("l' ", "l'").replace("qu' ", "qu'")
                out_f_sentence = ' '.join(f_sentence).replace("l' ", "l'").replace("qu' ", "qu'")
            else:
                out_m_sentence = ' '.join(m_sentence)
                out_f_sentence = ' '.join(f_sentence)

            # src, trg, src_gender, trg_gender
            outfile.write(out_m_sentence + '\t' + out_m_sentence + '\t' + 'M' + '\t' + 'M')
            outfile.write('\n')
            outfile.write(out_m_sentence + '\t' + out_f_sentence + '\t' + 'M' + '\t' + 'F')
            outfile.write('\n')
            outfile.write(out_f_sentence + '\t' + out_m_sentence + '\t' + 'F' + '\t' + 'M')
            outfile.write('\n')
            outfile.write(out_f_sentence + '\t' + out_f_sentence + '\t' + 'F'+ '\t' + 'F')
            outfile.write('\n')
    outfile.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--language",
        type=str,
        default=None,
        required=True,
        help="The language to generate data in: es for Spanish, fr for French"
    )
    parser.add_argument(
        "--nouns",
        type=str,
        default=None,
        help="The path of the translated nouns"
    )
    parser.add_argument(
        "--templates",
        type=str,
        default=None,
        help="The path of the translated templates"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=None,
        help="The path of the output file"
    )

    args = parser.parse_args()

    rules = {
        'fr': {'indef_arts': {'m': 'un', 'f': 'une'}, # a, an,
               'def_arts': {'m': 'le', 'f': 'la', 'special': "l'"}, # the
               'spros': {'m': 'il', 'f': 'elle'}, # he, she
               'opros': {'m': 'lui', 'f': 'elle'} # him, her
              },
        'es': {'indef_arts': {'m': 'un', 'f': 'una'}, # a, an,
               'def_arts': {'m': 'el', 'f': 'la'}, # the
               'spros': {'m': 'el', 'f': 'ella'}, # he, she
               'opros': {'m': 'el', 'f': 'ella'} # him, her
             }
        }


    nouns = read_data(args.nouns)
    templates = read_data(args.templates)

    m_nouns = [l.strip().split('\t')[0] for l in nouns]
    f_nouns = [l.strip().split('\t')[1] for l in nouns]
    assert len(m_nouns) == len(f_nouns)

    lang_rules = rules[args.language]
    input_nouns = {'m': m_nouns, 'f': f_nouns}

    input_templates = [l.strip() for l in templates]

    generate(**lang_rules, nouns=input_nouns, templates=input_templates,
             lang=args.language, output_dir=args.output_dir)


if __name__ == "__main__":
    main()