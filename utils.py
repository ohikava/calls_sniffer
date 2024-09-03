import re 
solAddress = r"[a-zA-Z0-9]{44}"
def extractTokenAddress(row):
    res = []
    tokens = row.replace("\n", " ").split(" ")
    for t in tokens:
        for p in t.split("/"):  
            if re.fullmatch(solAddress, p):
                res.append(p)
            
    return res 