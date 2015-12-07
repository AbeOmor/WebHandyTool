def getConfig():
    return {
        "string_search": {
            #Exact Search = 1, Similar Search = 2
                "type": 1,
                "proximity": 1
        },
        "depth": 2,
        "download": {
            # change file_type to any thing you wish (*.pdf,*.png etc.) and
            # all the option are from wget library, only use options specified below.
            # -r recursive
            # np no-parent
            "file_types": None,
            "option": "-rnp"
        }
    }
