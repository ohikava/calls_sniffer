import re 


solAddress = r"[a-zA-Z0-9]{44}"
evmAddress = r"[a-zA-Z0-9]{42}"

def extract_token_address(row):
    solana = []
    eth = []
    tokens = row.replace("\n", " ").split(" ")
    for t in tokens:
        for p in t.split("/"):  
            if re.fullmatch(solAddress, p) :
                solana.append(p)
            elif re.fullmatch(evmAddress, p):
                eth.append(p)
            
    return {"solana": solana, "eth": eth}
