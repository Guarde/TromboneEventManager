import PySimpleGUI as sg
import json

def open_with():
    return

def validate_song(song:dict): #Issue Structure [(Critical (bool), Description (string))]
    errors = []
    errors += validate_song_info(song)
    if "notes" in song.keys() and len(song["notes"]) > 0:
        errors += validate_song_notes(song)
    if "bgdata" in song.keys() and len(song["bgdata"]) > 0:
        errors += validate_song_events(song)
    if "lyrics" in song.keys() and len(song["lyrics"]) > 0:
        errors += validate_song_lyrics(song)
    if len(errors) == 0:
        return ["No Problems found!"]
    crit = []
    noncrit = []
    for e in errors:
        if e[0]:
            crit.append("⛔ " + e[1])
        else:
            noncrit.append("⚠️ " + e[1])
    return crit + noncrit

def validate_song_notes(song:dict):
    issues = []
    notes = song["notes"]
    if "endpoint" in song.keys():
        end = song["endpoint"]
    i = 0

    for note in notes:
    #Validate Array Length
        if not len(note) == 5:
            issues.append((True, f"Invalid note discovered at index [{i}]"))
            continue

    #Validate Data Classes
        if not validate_note_data_type(note):
            issues.append((True, f"Note at index [{i}] has an invalid component (TypeError)"))
            continue        

    #Validate Pitch Range
        if max(abs(note[2]), note[4]) > 178.75:
            issues.append((False, f"Note at beat [{note[0]}] is not within the playable pitch range"))
                    
    #Validate Length
        if end and note[0] + note[1] > end:
            issues.append((False, f"The note at beat [{note[0]}] is played after the end of the song"))

    #Validate Overlaps
        if i + 1 < len(notes) and note[0] + note[1] > notes[i + 1][0]:
            issues.append((False, f"The note at beat [{note[0]}] is overlapping with the next note"))
        i += 1

    return issues

def validate_note_data_type(note:list):
    for v in note:
        if not isinstance(v, float) and not isinstance(v, int):                
            return False
    return True

def validate_song_lyrics(song:dict):
    issues = []
    lyrics = song["lyrics"]
    if "endpoint" in song.keys():
        end = song["endpoint"]
    i = 0
    for lyric in lyrics:
    #Validate Array Length
        if not len(lyric) == 2:
            issues.append((True, f"Invalid lyric discovered at index [{i}]"))
            continue
    
    #Validate Data Classes
        if not isinstance(lyric["bar"], float) and not isinstance(lyric["bar"], int) and not isinstance(lyric["text"], str):
            issues.append((True, f"Lyric at index [{i}] has an invalid component (TypeError)"))
            continue

    #Validate Length
        if end and lyric["bar"] > end:
            issues.append((False, f"The lyric at beat [{lyric['bar']}] appears after the end of the song"))

    #Validate Overlaps
        if i + 1 < len(lyrics) and lyric["bar"] == lyrics[i + 1]["bar"]:
            issues.append((False, f"The lyric at beat [{lyric['bar']}] appears at the same time as the next lyric"))
        i += 1

    return issues

def validate_song_events(song:dict):
    issues = []
    events = song["bgdata"]
    if "endpoint" in song.keys():
        end = song["endpoint"]
    i = 0
    for event in events:
    #Validate Array Length
        if not len(event) == 3:
            issues.append((True, f"Invalid event discovered at index [{i}]"))
            continue
    
    #Validate Data Classes
        if not isinstance(event[0], float) and not isinstance(event[0], int) and not isinstance(event[1], int) and not isinstance(event[2], float) and not isinstance(event[2], int):
            issues.append((True, f"Event at index [{i}] has an invalid component (TypeError)"))
            continue

    #Validate Length
        if end and event[0] > end:
            issues.append((False, f"The event at beat [{event[0]}] is triggered after the end of the song"))
        i += 1

    return issues

def validate_song_info(song:dict):
    keys = []
    for k in ["timesig", "genre", "name", "trackRef", "author", "year", "tempo", "description", "endpoint", "difficulty", "notes"]:
        if not k in song.keys():
            keys.append(k)
            continue
        if song[k] in ["", None, 0] and not k == "description":
            keys.append(k)
            continue
    if len(keys) > 0:
        return [(True, "Chart is missing the following required key(s): " + ', '.join(keys))]
    else:
        return []

def import_notes():
    file = sg.popup_get_file("Import Notes", no_window=True, file_types=[["Trombone Champ Charts", ".tmb"]])
    if not file:
        return
    try:
        with open(file, "r") as f:
            imp = json.loads(f.read())
    except:
        sg.popup_error("Unable to parse JSON")
        return

    if not "notes" in imp.keys() or imp["notes"] in [[], "", None]:
        sg.popup_error("There was no notes stored in this file")
        return

    sg.popup("Notes imported successfully")
    return imp["notes"]

def import_events():
    file = sg.popup_get_file("Import Events", no_window=True, file_types=[["Trombone Champ Charts", ".tmb"]])
    if not file:
        return
    try:
        with open(file, "r") as f:
            imp = json.loads(f.read())
    except:
        sg.popup_error("Unable to parse JSON")
        return

    if not "bgdata" in imp.keys() or imp["bgdata"] in [[], "", None]:
        sg.popup_error("There was no background events stored in this file")
        return

    sg.popup("Backgorund Events imported successfully")
    return imp["bgdata"]

def import_lyrics():
    file = sg.popup_get_file("Import Lyrics", no_window=True, file_types=[["Trombone Champ Charts", ".tmb"]])
    if not file:
        return
    try:
        with open(file, "r") as f:
            imp = json.loads(f.read())
    except:
        sg.popup_error("Unable to parse JSON")
        return

    if not "lyrics" in imp.keys() or imp["lyrics"] in [[], "", None]:
        sg.popup_error("There was no lyrics stored in this file")
        return
    cleanlyrics = []
    for l in imp["lyrics"]:
        try:
            cleanlyrics.append([l["bar"], l["text"]])
        except:
            sg.popup_error("Unable to import lyrics")
            return


    sg.popup("Lyrics imported successfully")
    return (imp["lyrics"], cleanlyrics)