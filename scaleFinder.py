#!/usr/bin/python

import sys, os, re
from optparse import OptionParser
from collections import defaultdict

# import pandas as pd
#
# import numpy as np
#
# import matplotlib.pyplot as plt

def get_scales(notes):
    pos = 0
    chrom = {}
    major_scale = defaultdict(list)
    minor_scale = defaultdict(list)

    for n in notes:
        chrom[n] = {}
        root = notes[pos]
        second = notes[pos+2]
        flat_third = notes[pos+3]
        third = notes[pos+4]
        fourth = notes[pos+5]
        fifth = notes[pos+7]
        flat_sixth = notes[pos+8]
        sixth = notes[pos+9]
        flat_seventh = notes[pos+10]
        seventh = notes[pos+11]

        major_scale[n] = [root, second, third, fourth, fifth, sixth, seventh]
        minor_scale[n] = [root, second, flat_third, fourth, fifth, flat_sixth, flat_seventh]


        chrom[n]['I'] = root
        chrom[n]['II'] = second
        chrom[n]['bIII'] = flat_third
        chrom[n]['III'] = third
        chrom[n]['IV'] = fourth
        chrom[n]['V'] = fifth
        chrom[n]['bVI'] = flat_sixth
        chrom[n]['VI'] = sixth
        chrom[n]['bVII'] = flat_seventh
        chrom[n]['VII'] = seventh

        pos +=1
        if pos > 12:
            break

    return(major_scale, minor_scale, chrom)


def find_interval(chromatic_scale, note, interval, major_scale, minor_scale):

    for k in chromatic_scale:
        if chromatic_scale[k][interval] == note:
            if note in major_scale[k]:
                print("* %s is the %s note of %s major") % (note, interval, k)
                scale='major'
                print_scale(chromatic_scale, major_scale, minor_scale, k, 'major')

            if note in minor_scale[k]:
                print("* %s is the %s note of %s minor") % (note, interval, k)
                scale='minor'
                print_scale(chromatic_scale, major_scale, minor_scale, k, 'minor')

            relative_key = k
    return(relative_key, scale)


def print_chord(d, maj_scales, key, interval):
    print("%s %s") % (key, interval)

    root, maj_third, fifth, seventh = d[key]['I'], d[key]['III'], d[key]['V'], d[key]['VII']


def print_scale(chromatic_scale, maj_scale, min_scale, key, interval):
    print("--------")
    print("%s %s") % (key, interval)
    print("--------")

    if interval == 'major':
        one, three, five, seven = chromatic_scale[key]['I'], chromatic_scale[key]['III'], chromatic_scale[key]['V'], chromatic_scale[key]['VII']
        scale = '\t'.join(maj_scale[key])
        chords = [ "I", "II", "III", "IV", "V", "VI", "VII" ]
        print_chords = '\t'.join(chords)
    if interval == 'minor':
        one, three, five, seven = chromatic_scale[key]['I'], chromatic_scale[key]['bIII'], chromatic_scale[key]['V'], chromatic_scale[key]['bVII']
        scale = '\t'.join(min_scale[key])
        chords = [ "I", "II", "bIII", "IV", "V", "bVI", "bVII" ]
        print_chords = '\t'.join(chords)

    print
    print("%s triad:   %s %s %s") % (interval, one, three, five)
    print("%s seventh: %s %s %s %s") % (interval, one, three, five, seven)

    print
    print("%s" % print_chords)
    print("%s" % scale)
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
                    help="The interval ['major', 'minor']")

    parser.add_option("-n", \
                      "--note", \
                      dest="note",
                      action="store",
                      help="What scales have this note in them?")

    parser.add_option("-p", \
                      "--position", \
                      dest="position",
                      action="store",
                      help="The location in a scale ['I', 'II' 'bIII' ... ]?")

    parser.set_defaults(interval='major', key='C', position='III')
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


        major_scale, minor_scale, chromatic_scale = get_scales(notes)


        if options.note is not None:
            note = options.note
            relative_key, interval = find_interval(chromatic_scale, note, position, major_scale, minor_scale)

            # for i in interval:
            #     print chromatic_scale[relative_key][i]
            # print_scale(chromatic_scale, major_scale, minor_scale, relative_key, interval)

        else:
            if not key in chromatic_scale:
                print("%s not a valid key. Exiting" % key)
                sys.exit()

            intervals = ['major', 'minor', 'minor', 'major', 'minor', 'minor']
            print_scale(chromatic_scale, major_scale, minor_scale, key, interval)



if __name__ == "__main__":
    sys.exit(main())
