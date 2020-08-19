
async def duration(time):
    if time.endswith("s"):
        return time.replace("s", "")
    
    if time.endswith("m"):
        fixtime = time.replace("m", "")
        newtime = int(fixtime) * 60
        return int(newtime)

    if time.endswith("h"):
        fixtime = time.replace("h", "")
        newtime = int(fixtime) * 3600
        return int(newtime)
    
    if time.endswith("d"):
        fixtime = time.replace("d", "")
        newtime = int(fixtime) * 86400
        return int(newtime)
    else:
        return Exception