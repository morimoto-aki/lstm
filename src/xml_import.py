'''xml形式の楽譜をインポートするプログラム'''
import glob
import pickle
import csv
from music21 import converter, instrument, note, chord, interval, pitch


def file_path():
    '''ファイルのパスを取得する関数'''

    midipath_list = glob.glob("music/midi/*.mid")
    xmlpath_list = glob.glob("music/xml/*.xml")

    return midipath_list, xmlpath_list


def get_onset():
    '''楽譜をcsvにする関数'''
    path = file_path()
    filepath = path[1]
    notes = []
    note_list = ["quarterLength"]
    measure_no = 0
    tie_quarter_length = 0

    for file in filepath:
        xml = converter.parse(file)
        print("Parsing %s" % file)
        notes_to_parse = None

        try:  # file has instrument parts
            s2 = instrument.partitionByInstrument(xml)
            notes_to_parse = s2.parts[0].recurse().notesAndRests
        except:  # file has notes in a flat structure
            notes_to_parse = xml.flat.notes

        for element in notes_to_parse:
            if isinstance(element, note.Note) or isinstance(element, note.Rest):

                if element.tie is not None:
                    tie = element.tie.type
                    if tie == "start":
                        tie_quarter_length = str(element.quarterLength)

                    elif tie == "stop":
                        noteinfo = tie_quarter_length + "+" + str(element.quarterLength)
                        notes.append(noteinfo)
                        note_list.append(noteinfo)

                elif element.isRest:
                    noteinfo = str(element.quarterLength)
                    notes.append(noteinfo)
                    note_list.append(noteinfo)

                else:
                    noteinfo = str(element.quarterLength)
                    notes.append(noteinfo)
                    note_list.append(noteinfo)

        print(notes)

    with open('src/data/onset.csv', 'w') as filepath:
        writer = csv.writer(filepath, lineterminator='\n')
        writer.writerows(note_list)

    with open('src/data/onset', 'wb') as filepath:
        pickle.dump(notes, filepath)


def get_pitch():
    '''楽譜をcsvにする関数'''
    path = file_path()
    filepath = path[1]
    notes_major = []
    notes_minor = []
    note_list_major = []
    note_list_minor = []
    title_list = ["interval"]
    root = ""
    chord_name = ""
    quality = ""
    octave = 2

    # リストに項目名追加
    note_list_major.append(title_list)
    note_list_minor.append(title_list)

    for file in filepath:
        xml = converter.parse(file)
        print("Parsing %s" % file)
        notes_to_parse = None

        try:  # file has instrument parts
            s2 = instrument.partitionByInstrument(xml)
            notes_to_parse = s2.parts[0].recurse().notesAndRests
        except:  # file has notes in a flat structure
            notes_to_parse = xml.flat.notes

        for element in notes_to_parse:
            if isinstance(element, chord.Chord):
                root = element.pitchNames[0]
                chord_name = element.figure
                quality = element.quality

            if isinstance(element, note.Note) or isinstance(element, note.Rest):
                if quality == "major":
                    p1 = pitch.Pitch(root + str(octave))
                    if element.tie is not None:
                        tie = element.tie.type
                        p2 = element.pitch
                        interval_name = (interval.Interval(p1, p2)).directedName
                        if tie == "start":
                            tie_quarter_length = str(element.quarterLength)
                            offset = element.offset
                        elif tie == "stop":
                            noteinfo = interval_name
                            notes_major.append(noteinfo)
                            note_list_major.append(noteinfo)

                    elif element.isRest:
                        noteinfo = "Rest"
                        notes_major.append(noteinfo)
                        note_list_major.append(noteinfo)

                    elif element.notehead is "x":
                        noteinfo = "x"
                        notes_major.append(noteinfo)
                        note_list_major.append(noteinfo)

                    else:
                        p2 = element.pitch
                        interval_name = (interval.Interval(p1, p2)).directedName
                        noteinfo = interval_name
                        notes_major.append(noteinfo)
                        note_list_major.append(noteinfo)

                elif quality == "minor":
                    p1 = pitch.Pitch(root + str(octave))
                    if element.tie is not None:
                        tie = element.tie.type
                        p2 = element.pitch
                        interval_name = (interval.Interval(p1, p2)).directedName
                        if tie == "start":
                            tie_quarter_length = str(element.quarterLength)
                            offset = element.offset
                        elif tie == "stop":
                            noteinfo = interval_name
                            notes_minor.append(noteinfo)
                            note_list_minor.append(noteinfo)

                    elif element.isRest:
                        noteinfo = "Rest"
                        notes_minor.append(noteinfo)
                        note_list_minor.append(noteinfo)

                    elif element.notehead is "x":
                        noteinfo = "x"
                        notes_minor.append(noteinfo)
                        note_list_minor.append(noteinfo)

                    else:
                        p2 = element.pitch
                        interval_name = (interval.Interval(p1, p2)).directedName
                        noteinfo = interval_name
                        notes_minor.append(noteinfo)
                        note_list_minor.append(noteinfo)

    with open('src/data/major.csv', 'w') as filepath:
        writer = csv.writer(filepath, lineterminator='\n')
        writer.writerows(note_list_major)

    with open('src/data/minor.csv', 'w') as filepath:
        writer = csv.writer(filepath, lineterminator='\n')
        writer.writerows(note_list_minor)

    with open('src/data/major', 'wb') as filepath:
        pickle.dump(notes_major, filepath)

    with open('src/data/minor', 'wb') as filepath:
        pickle.dump(notes_minor, filepath)


def main():
    '''main関数'''
    # get_onset()
    get_pitch()


if __name__ == '__main__':
    main()
