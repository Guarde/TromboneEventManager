import PySimpleGUI as sg
import json, os
import layouts, helpers, tools

def main_window(): #Name, trackRef, Author, Year, BPM, Endpoint, (Duration), Difficulty, note start color. note end color
    sg.theme("DarkGrey5")
    window = sg.Window("TromboneChamp Event Manager", layouts.layout_full, enable_close_attempted_event=True, finalize=True)
    loaded_file = None
    loaded_song = None
    loaded_data_lyrics = None
    loaded_data_notes = None
    loaded_data_bgdata = None

    sg.popup("Welcome! Please load a file to get started!")
    new_file = sg.popup_get_file("Open File", no_window=True, file_types=[["Trombone Champ Charts", ".tmb"]])
    if new_file:
        loaded_file = new_file
        loaded_song = helpers.do_load(window, loaded_file)
        print(loaded_file)
        window.Element("status_bar").update(loaded_file)
    else:
        return

    while True: 
        event, values = window.read()
        print(event)
        if not loaded_file and event in (sg.WINDOW_CLOSE_ATTEMPTED_EVENT, "Exit") :
            break
        elif loaded_file and event in (sg.WINDOW_CLOSE_ATTEMPTED_EVENT, 'Exit'):
            popevent = sg.PopupYesNo('Save your progress before exiting?', title="Exit Program", grab_anywhere=True, keep_on_top=True)
            match popevent:
                case "Yes":
                    if not loaded_file:
                        loaded_file = sg.popup_get_file("Open File", no_window=True, file_types=[["Trombone Champ Charts", ".tmb"]])
                    if loaded_file:
                        s = helpers.finalize_song(values, loaded_song)
                        try:
                            with open(loaded_file, "x", encoding="utf-8") as f:
                                json.dump(s, f)
                        except FileExistsError:                    
                            with open(loaded_file, "w", encoding="utf-8") as f:
                                json.dump(s, f)
                    sg.popup_ok("Progress Saved")
                    break
                case None:
                    continue
                case "No":
                    break
                case _:
                    break
        
        if len(event) > 2 and event[0] in ["bgdata_table", "notes_table", "lyrics_table"]:
            match event[0]:
                case "lyrics_table":
                    loaded_data_lyrics = helpers.populate_edit_boxes(window, event, loaded_song)
                case "notes_table":
                    loaded_data_notes = helpers.populate_edit_boxes(window, event, loaded_song)
                case "bgdata_table":
                    loaded_data_bgdata = helpers.populate_edit_boxes(window, event, loaded_song)
                case _:
                    continue
        if event ==  "About...":
            sg.popup("\"TromboneChamp File Manager\" version 1.0.0 by Guardie", "<insert github link>", grab_anywhere=True, keep_on_top=True)
        if event ==  "Load":
            new_file = sg.popup_get_file("Open File", no_window=True, file_types=[["Trombone Champ Charts", ".tmb"]])
            if new_file:
                loaded_file = new_file
                loaded_song = helpers.do_load(window, loaded_file)
                if not loaded_song:
                    window.Element("status_bar").update("Unable to load file!")
                    continue
                window.Element("status_bar").update(loaded_file)
        if event ==  "Reload":
            if loaded_file:
                loaded_song = helpers.do_load(window, loaded_file)
                if not loaded_song:
                    window.Element("status_bar").update("Unable to load file!")
                    continue
                window.Element("status_bar").update(loaded_file)
        if event ==  "Save":
            s = helpers.finalize_song(values, loaded_song)
            if not s:
                continue
            if not loaded_file:
                loaded_file = sg.popup_get_file("Open File", no_window=True, file_types=[["Trombone Champ Charts", ".tmb"]])
            if loaded_file:
                try:
                    with open(loaded_file, "x", encoding="utf-8") as f:
                        json.dump(s, f)
                except FileExistsError:                    
                    with open(loaded_file, "w", encoding="utf-8") as f:
                        json.dump(s, f)
            sg.popup_ok("Progress Saved")
            window.Element("status_bar").update(loaded_file)
        if event ==  "Save As...":
            s = helpers.finalize_song(values, loaded_song)
            if not s:
                continue
            new_file = sg.popup_get_file('Save File As...', no_window=True, default_extension = ".tmb", file_types=[["Trombone Champ Charts", ".tmb"]], save_as=True)
            if new_file:
                loaded_file = new_file
                try:
                    with open(loaded_file, "x", encoding="utf-8") as f:
                        json.dump(s, f)
                except FileExistsError:                    
                    with open(loaded_file, "w", encoding="utf-8") as f:
                        json.dump(s, f)
                sg.popup_ok("Progress Saved")
                window.Element("status_bar").update(loaded_file)
        if event == "editbutton_done_bgdata" and loaded_data_bgdata and loaded_song:
            newsong = helpers.update_edit_boxes(loaded_data_bgdata, "bgdata", window, values, loaded_song)
            if newsong:
                loaded_song = newsong
                
                loaded_data_bgdata = None
        if event == "editbutton_done_lyrics" and loaded_data_lyrics and loaded_song:
            newsong = helpers.update_edit_boxes(loaded_data_lyrics, "lyrics", window, values, loaded_song)
            if newsong:
                loaded_song = newsong
                loaded_data_lyrics = None
        if event == "editbutton_done_notes" and loaded_data_notes and loaded_song:
            newsong = helpers.update_edit_boxes(loaded_data_notes, "notes", window, values, loaded_song)
            if newsong:
                loaded_song = newsong
                loaded_data_notes = None
        if event == "editbutton_new_bgdata" and loaded_song:
            newsong = helpers.update_edit_boxes(loaded_data_bgdata, "bgdata", window, values, loaded_song, True)
            if newsong:
                loaded_song = newsong
                loaded_data_bgdata = None
        if event == "editbutton_new_lyrics" and loaded_song:
            newsong = helpers.update_edit_boxes(loaded_data_lyrics, "lyrics", window, values, loaded_song, True)
            if newsong:
                loaded_song = newsong
                loaded_data_lyrics = None
        if event == "editbutton_new_notes" and loaded_song:
            newsong = helpers.update_edit_boxes(loaded_data_notes, "notes", window, values, loaded_song, True)
            if newsong:
                loaded_song = newsong
                loaded_data_notes = None
        if event in ["tempo_box", "bgdata_table_field_2"]:
            window.Element("bgdata_table_field_0").update(helpers.update_timeseconds_from_beat(values))
        if event == "tempo_box":
            newtable = helpers.update_all_timeseconds_from_tempo(values, loaded_song)
            if newtable:
                window.Element("bgdata_table").update(newtable)
                loaded_song["bgdata"] = newtable
        if event in ["tempo_box", "endpoint_box"]:
            window.Element("duration_box").update(helpers.update_duration_from_tempo_bpm(values))
        if event in ["timesig_box", "genre_box", "name_box", "trackRef_box", "author_box", "year_box", "tempo_box", "endpoint_box", "difficulty_box", "description_box"]:
            key = event.replace("_box", "")
            loaded_song[key] = values[event]
        if event in ["notes_table_field_2", "notes_table_field_3"]:
            newend = helpers.update_end_from_mod_and_start(values)
            if newend:
                window.Element("notes_table_field_4").update(newend)
        if event == "notes_table_field_4":
            newpitch = helpers.update_mod_from_end(values)
            if newpitch:
                window.Element("notes_table_field_3").update(newpitch)
        if event == "Validate Chart" and loaded_song:
            report = "\n".join(tools.validate_song(loaded_song))
            sg.PopupScrolled(report, title = "Validation Report")
        if event == "Import Notes" and loaded_song:
            notes = tools.import_notes()
            if notes:
                loaded_song["notes"] = notes
                window.Element("notes_table").update(notes)
                helpers.clear_edit_boxes("notes", window)
        if event == "Import Events" and loaded_song:
            bgdata = tools.import_events()
            if bgdata:
                loaded_song["bgdata"] = bgdata
                window.Element("bgdata_table").update(bgdata)
                helpers.clear_edit_boxes("bgdata", window)
        if event == "Import Lyrics" and loaded_song:
            lyrics, cleanlyrics = tools.import_lyrics()
            if lyrics:
                loaded_song["lyrics"] = lyrics
                window.Element("lyrics_table").update(cleanlyrics)
                helpers.clear_edit_boxes("lyrics", window)
        
    window.close()

main_window()