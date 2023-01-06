import PySimpleGUI as sg
import json

def finalize_song(values:dict, song:dict):
    missing = []
    if not song:
        song == {}
    for v in ["timesig", "genre", "name", "trackRef", "author", "year", "tempo", "endpoint", "difficulty", "description"]:
        if not v + "_box" in values.keys() or values[v + "_box"] == None or values[v + "_box"] == "":
            missing.append(v)
        if v in ["timesig", "year", "difficulty"]:
            try:
                song[v] = int(values[v + "_box"])
            except:
                continue
        if v in ["genre", "name", "trackRef", "author", "description"]:
            try:
                song[v] = str(values[v + "_box"])
            except:
                continue
        if v in ["tempo", "endpoint"]:
            try:
                song[v] = float(values[v + "_box"])
            except:
                continue
    
    if len(missing) > 0:
        popevent = sg.PopupYesNo("The following required values are not filled in:" ,"- "+ "\n- ".join(missing) + "\nContinue saving anyway?")
        if  popevent == "No":
            return
    return song

def update_duration_from_tempo_bpm(values):
    if values["tempo_box"] and values["endpoint_box"]:
        try:
            mins, secs = divmod(round(60/float(values["tempo_box"])*float(values["endpoint_box"])), 60)
            if mins > 0:
                dur = f"{mins}m {secs}s"
            else:
                dur = f"{secs}s"
            return dur
        except:
            return "N/A"
    return

def update_timeseconds_from_beat(values):
    if values["tempo_box"] and values["bgdata_table_field_2"]:
        try:
            return round(60/float(values["tempo_box"])*float(values["bgdata_table_field_2"]), 2)
        except:
            return "N/A"
    
def update_all_timeseconds_from_tempo(values:dict, song:dict):
    if values["tempo_box"] and "bgdata" in song.keys():
        newdata = []
        try:
            for v in song["bgdata"]:
                newtiming = round(60/float(values["tempo_box"])*float(v[2]), 2)
                newdata.append([newtiming, v[1], v[2]])        
            return newdata
        except:
            return None
    return None

def update_mod_from_end(values):
    if values["notes_table_field_2"] and values["notes_table_field_4"]:
        try:
            return float(values["notes_table_field_4"]) - float(values["notes_table_field_4"])
        except:
            return "N/A"

def update_end_from_mod_and_start(values):
    if values["notes_table_field_2"] and values["notes_table_field_3"]:
        try:
            return float(values["notes_table_field_2"]) + float(values["notes_table_field_3"])
        except:
            return "N/A"

def populate_edit_boxes(window:sg.Window, event:str, song:dict):
    row, col = event[2]
    if row == None or row < 0:
        return
    key = event[0].replace("_table", "")
    data = song[key][row]
    if key in ["notes", "bgdata"]:
        i = 0
        for v in data:
            try:
                window.Element(event[0] + "_field_" + str(i)).update(v)
            except:
                continue
            i += 1
    elif key == "lyrics":
            try:
                window.Element("lyrics_table_field_0").update(data["bar"])
                window.Element("lyrics_table_field_1").update(data["text"])
            except:
                return
    output = {"row": row, "data": data}
    return output

def update_edit_boxes(data:dict, tablename:str, window:sg.Window, values:dict, song:dict, new:bool=False):
    print(data)
    newrow = []
    if not tablename in song.keys():
        song[tablename] = []
    match tablename:
        case "notes":
            count = 0
            newtable = list(song[tablename])
            for n in ["notes_table_field_0", "notes_table_field_1", "notes_table_field_2", "notes_table_field_3", "notes_table_field_4"]:
                try:
                    newrow.append(float(values[n]))
                except (KeyError, ValueError):
                    sg.PopupError("Please enter a value in every field!")                    
                    return


        case "bgdata":
            newtable = list(song[tablename])           
            try:
                newrow = ([float(values["bgdata_table_field_0"]), int(values["bgdata_table_field_1"]), int(values["bgdata_table_field_2"])])
            except (KeyError, ValueError):
                    sg.PopupError("Please enter a value in every field!")
                    return
            except:
                return

        case "lyrics":
            newtable = []
            for t in song["lyrics"]:
                newtable.append([float(t["bar"]), t["text"]])
            try:
                newrow = ([float(values["lyrics_table_field_0"]), values["lyrics_table_field_1"]])
            except (KeyError, ValueError):
                    sg.PopupError("Please enter a value in every field!")
            except:
                return
        case _:
            return
    if new:
        if newrow.count(None) == len(newrow):
            return
        else:
            newtable.append(newrow)
    else:
        newtable[data["row"]] = newrow

    if tablename == "notes":
        if new:
            song["notes"].append(newrow)
        else:
            song["notes"][data["row"]] = newrow
        song[tablename].sort(key=sort_by_index_0)
        newtable.sort(key=sort_by_index_0)
    elif tablename == "lyrics":
        if new:
            song["lyrics"].append({"bar": newrow[0], "text": newrow[1]})
        else:
            song["lyrics"][data["row"]] = {"bar": newrow[0], "text": newrow[1]}
        song[tablename].sort(key=sort_by_bar)
        newtable.sort(key=sort_by_index_0)
    elif tablename == "bgdata":
        if new:
            song["bgdata"].append(newrow)
        else:
            song["bgdata"][data["row"]] = newrow
        song[tablename].sort(key=sort_by_index_2)
        newtable.sort(key=sort_by_index_2)
    window.Element(tablename + "_table").update(newtable)
    if not song == None:
        clear_edit_boxes(tablename, window, values)
        return song
    return

def clear_edit_boxes(tablename, window:sg.Window, values):
    for n in [tablename + "_table_field_0", tablename + "_table_field_1", tablename + "_table_field_2", tablename + "_table_field_3", tablename + "_table_field_4"]:
        if n in values.keys():
            window.Element(n).update("")            

def sort_by_index_0(element):
    return element[0]

def sort_by_index_2(element):
    return element[2]

def sort_by_bar(element):
    return element["bar"]

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

def do_load(window:sg.Window, file:str):
    for e in ["duration_box", "notes_table", "notes_table_field_0", "notes_table_field_1", "notes_table_field_2", "notes_table_field_3", "notes_table_field_4", "lyrics_table", "lyrics_table_field_0", "lyrics_table_field_1", "bgdata_table", "bgdata_table_field_0", "bgdata_table_field_1", "bgdata_table_field_2"]:
        window.Element(e).update(None)
    try:
        with open(file, "r", encoding="utf-8") as f:
            song = json.loads(f.read())
    except:
        sg.popup("File could not be loaded!", grab_anywhere=True, keep_on_top=True)
        return None
    else:
        compare = ["timesig", "genre", "description", "name", "trackRef", "author", "year", "tempo", "endpoint", "difficulty"]
        for k in song.keys():
            if k in compare:
                window.Element(k + "_box").update(song[k])
                window.Element(k + "_box").SetTooltip(song[k])
                compare.remove(k)
            elif k in ["note_color_start", "note_color_end"]:
                color = rgb_to_hex((round(song[k][0] * 255), round(song[k][1] * 255), round(song[k][2] * 255)))
                window.Element(k + "_box").update(button_color=[f'#{color}'])
            elif k == "notes":
                l = (song[k])
                l.sort(key = sort_by_index_0)
                window.Element(k + "_table").update(l)
            elif k == "bgdata":
                l = (song[k])
                l.sort(key = sort_by_index_2)
                window.Element(k + "_table").update(l)
            elif k == "lyrics":
                notes = []
                for v in song[k]:
                    try:
                        notes.append([v["bar"], v["text"]])
                    except:
                        print("Failed to load note: " + str(v))
                window.Element(k + "_table").update(notes)
        for k in compare:
             window.Element(k + "_box").update("MISSING!")
        if "tempo" in song.keys() and "endpoint" in song.keys():
            mins, secs = divmod(round(60/song["tempo"]*song["endpoint"]), 60)
            if mins > 0:
                dur = f"{mins}m {secs}s"
            else:
                dur = f"{secs}s"
            window.Element("duration_box").update(dur)
        return song