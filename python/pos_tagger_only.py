import re
import sys
import traceback
import pos_tagger_stdin


def main():
    pos_tagger = pos_tagger_stdin.PosTagger()
    words = []
    sentence_count = 0

    for line in sys.stdin:
        line = line.strip()
        parts = line.split(" ")
        if line:
            words.append(re.sub(r'[^\x00-\x7f]', r'+', parts[0]))
        else:
            try:
                tags = pos_tagger.TagSentence(words)
            except:
                print >> sys.stderr, "Cannot process %s" % words
                traceback.print_exc()
                sys.exit(1)

            for word, tag in zip(words, tags):
                tag = re.sub(r':[^:]*$', '', tag)
                print "%s %s" % (word, tag)
            print

            del words[:]

            sentence_count += 1
            if sentence_count % 100 == 0:
                print >> sys.stderr, "Processed %d sentences." % sentence_count


if __name__ == "__main__":
    main()
