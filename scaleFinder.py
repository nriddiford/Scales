#!/usr/bin/python

import sys, os, re
from optparse import OptionParser
from collections import defaultdict

# import pandas as pd
#
# import numpy as np
#
# import matplotlib.pyplot as plt

def major_scale(notes):
    pos = 0
    d = {}
    scale = defaultdict(list)

    for n in notes:
        d[n] = {}
        root_v = notes[pos]
        second_v = notes[pos+2]
        third_v = notes[pos+4]
        fourth_v = notes[pos+5]
        fifth_v = notes[pos+7]
        sixth_v = notes[pos+9]
        seventh_v = notes[pos+11]
        scale[n] = [root_v, second_v, third_v, fourth_v, fifth_v, sixth_v, seventh_v]

        d[n]['root'] = root_v
        d[n]['second'] = second_v
        d[n]['third'] = third_v
        d[n]['fourth'] = fourth_v
        d[n]['fifth'] = fifth_v
        d[n]['sixth'] = sixth_v
        d[n]['seventh'] = seventh_v

        pos +=1
        if pos > 12:
            break

    return(scale, d)

def find_interval(scales, note, interval):
    for k in scales:
        if scales[k][interval] == note:
            print("%s is the %s note of %s major") % (note, interval, k)
            relative_key = k
    return(relative_key)

def print_maj(d, maj_scales, key):
    print("--------")
    print("%s Major" % key)
    print("--------")

    root, maj_third, fifth, seventh = d[key]['root'], d[key]['third'], d[key]['fifth'], d[key]['seventh']

    print_maj_scale = '\t'.join(maj_scales[key])
    chords = [ "I", "II", "III", "IV", "V", "VI", "VII" ]
    maj_chrods = '\t'.join(chords)

    print
    print("%s triad:   %s %s %s") % ('major', root, maj_third, fifth)
    print("%s seventh: %s %s %s %s") % ('major', root, maj_third, fifth, seventh)

    print
    print("%s" % maj_chrods)
    print("%s" % print_maj_scale)
    print



def get_args():
    parser = OptionParser()

    parser.add_option("-k", \
                    "--key", \
                    dest="key",
                    action="store",
                    help="The key you want to look up ")

    parser.add_option("-i", \
                    "--interval", \
                    dest="interval",
                    action="store",
                    help="The interval ['maj', 'min', 'aug']")

    parser.add_option("-n", \
                      "--note", \
                      dest="note",
                      action="store",
                      help="What scales have this note in them?")

    parser.add_option("-p", \
                      "--position", \
                      dest="position",
                      action="store",
                      help="The location in a scale ['root', 'second' ...]?")

    parser.set_defaults(interval='maj', key='C', position='third')
    options, args = parser.parse_args()


    if options.key is None and options.note is None:
      parser.print_help()
      print

    return(options, args)


def main():
    options, args = get_args()
    key = options.key
    interval = options.interval
    position = options.position

    if options.key is not None:

        if options.note is not None:
            lookup = options.note
        else:
            lookup = key

        if re.search('b', lookup):
            notes = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B",
                     "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
        else:
            notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B",
                  "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

        maj_scales, d = major_scale(notes)

        if options.note is not None:
            note = options.note
            relative_key = find_interval(d, note, position)
            print_maj(d, maj_scales, relative_key)


        else:
            if not key in maj_scales:
                print("%s not a valid key. Exiting" % key)
                sys.exit()

            print_maj(d, maj_scales, key)



if __name__ == "__main__":
    sys.exit(main())
