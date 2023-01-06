import PySimpleGUI as sg
menubar =   [ 
                ["&File", 
                    ["&Load", "&Reload", "&Save", "&Save As...", "---", "&Exit"]],
                ["&Tools", 
                    [
                    "&Import", ["&Import Notes", "&Import Lyrics", "&Import Events"],
                    "&Validate Chart",]],
                ["&Help", ["&About..."]]
            ]    

layout_songinfo =   [[sg.Frame("Description", [[sg.Multiline("", expand_x=True, expand_y=True, key="description_box", no_scrollbar=True, background_color="#546273", text_color="#FFFFFF")]], size=[232, 120], expand_y=True)],
                        [sg.Col([[sg.Push(), sg.Text("Name")], 
                        [sg.Push(), sg.Text("trackRef")],
                        [sg.Push(), sg.Text("Author")],
                        [sg.Push(), sg.Text("Genre")], 
                        [sg.Push(), sg.Text("Year")], 
                        [sg.Push(), sg.Text("Tempo")],
                        [sg.Push(), sg.Text("Difficulty")], 
                        [sg.Push(), sg.Text("Duration")], 
                        [sg.Push(), sg.Text("Endpoint")],
                        [sg.Push(), sg.Text("Time Signature")],
                        [sg.VPush()],
                        [sg.Push(), sg.Text("Note Start Color")], 
                        [sg.VPush()],
                        [sg.Push(), sg.Text("Note End Color")], 
                        [sg.VPush()]]),
                    sg.Col([[sg.Input("", key="name_box", size=(15,1))], 
                        [sg.Input("", key="trackRef_box", size=(15,1))],
                        [sg.Input("", key="author_box", size=(15,1))],
                        [sg.Input("", key="genre_box", size=(15,1))], 
                        [sg.Input("", key="year_box", size=(15,1))], 
                        [sg.Input("", key="tempo_box", size=(15,1), enable_events=True)],
                        [sg.Input("", key="difficulty_box", size=(15,1))], 
                        [sg.Input("", key="duration_box", size=(15,1), disabled=True, disabled_readonly_background_color="#bbbbbb")], 
                        [sg.Input("", key="endpoint_box", size=(15,1), enable_events=True)],
                        [sg.Input("", key="timesig_box", size=(15,1))], 
                        [sg.Button("",key="note_color_start_box", size=(2,1))], 
                        [sg.Button("", key="note_color_end_box", size=(2,1))]])]]

layout_status = [[sg.StatusBar("", size=[80, 1], key="status_bar", justification="r")]]

layout_list_notes = [[sg.Table([], ["Beat", "Length", "Start Pitch", "Pitch Modulation", "End_Pitch"], justification="c", col_widths=[5, 5, 7, 12, 7], auto_size_columns=False, expand_y=True, expand_x=True, key="notes_table", enable_click_events=True, select_mode="browse")],
                    [sg.Col([
                        [sg.Button("Apply", size = [6, 1], key="editbutton_done_notes")], 
                        [sg.Button("New", size = [6, 1], key="editbutton_new_notes")]]), 
                    sg.Col([
                        [sg.Text("Beat")], 
                        [sg.Input(size = [6, 1], key="notes_table_field_0")]]), 
                    sg.Col([
                        [sg.Text("Length")], 
                        [sg.Input(size = [6, 1], key="notes_table_field_1")]]), 
                    sg.Col([
                        [sg.Text("Start")], 
                        [sg.Input(size = [5, 1], key="notes_table_field_2", enable_events=True)]]), 
                    sg.Col([
                        [sg.Text("Modulation")], 
                        [sg.Input(size = [10, 1], key="notes_table_field_3", enable_events=True)]]), 
                    sg.Col([
                        [sg.Text("End")], 
                        [sg.Input(expand_x=True, key="notes_table_field_4", enable_events=True)]]), 
                        sg.Push()]
                    ]

layout_list_lyrics = [[sg.Table([], ["Beat", "Text"], justification="c", col_widths=[5, 35], auto_size_columns=False, expand_y=True, expand_x=True, key="lyrics_table", enable_click_events=True, select_mode="browse")],
                    [sg.Col([
                        [sg.Button("Apply", size = [6, 1], key="editbutton_done_lyrics")], 
                        [sg.Button("New", size = [6, 1], key="editbutton_new_lyrics")]]), 
                    sg.Col([
                        [sg.Text("Beat")], 
                        [sg.Input(size = [8, 1], key="lyrics_table_field_0")]]), 
                    sg.Col([
                        [sg.Text("Text")], 
                        [sg.Input(expand_x=True, key="lyrics_table_field_1")]])]
                    ]
layout_list_events = [[sg.Table([], ["Time in Seconds", "Event ID", "Time in Beats"], justification="c", col_widths=[17, 6, 17], auto_size_columns=False, expand_y=True, expand_x=True, key="bgdata_table", enable_click_events=True, select_mode="browse")],
                    [sg.Col([
                        [sg.Button("Apply", size = [6, 1], key="editbutton_done_bgdata")], 
                        [sg.Button("New", size = [6, 1], key="editbutton_new_bgdata")]]), 
                    sg.Col([
                        [sg.Text("Time in Seconds")], 
                        [sg.Input(size = [14, 1], key="bgdata_table_field_0", disabled=True, disabled_readonly_background_color="#bbbbbb")]]), 
                    sg.Col([
                        [sg.Text("Event ID")], 
                        [sg.Input(size = [8, 1], key="bgdata_table_field_1")]]), 
                    sg.Col([
                        [sg.Text("Time in Beats")], 
                        [sg.Input(expand_x=True, key="bgdata_table_field_2", enable_events=True)]])]
                    ]

layout_tabs = [[sg.Tab("Notes", layout_list_notes), sg.Tab("Lyrics", layout_list_lyrics), sg.Tab("Events", layout_list_events, expand_x=True)]]

layout_list = [[sg.TabGroup(layout_tabs, size=[425, 423])]]

layout_full = [[sg.MenubarCustom(menubar, k="-CUST MENUBAR-")],
                [sg.Col(layout_list, size=[440, 460]), sg.Col(layout_songinfo, size=[250, 460], vertical_alignment="top")],
                [sg.Col(layout_status, expand_x=True)]]

layout_issuetracker = [[]]