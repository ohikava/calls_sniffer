import re 
import requests
import tls_client

solAddress = r"[a-zA-Z0-9]{44}"
evmAddress = r"[a-zA-Z0-9]{42}"

def extractTokenAddress(row):
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


headers = {
            "Content-Type": "application/json"
        }
session = tls_client.Session(client_identifier="chrome_103")

def filterNonTokens(CA, net="SOLANA"):
    if net == "SOLANA":
        url = f"https://gmgn.ai/defi/quotation/v1/tokens/security/sol/{CA}"


        response = session.get(url, headers=headers)
        body = response.json()
        is_token = bool(body.get("data", {}).get("goplus", {}).get("liquidity", None))
    elif net == "ETH":

        url = f"https://gmgn.ai/defi/quotation/v1/tokens/security/eth/{CA}"
        
        response = session.get(url, headers=headers)
        print(response.status_code)

        body = response.json()
        is_token = bool(body.get("data", {}).get("goplus", {}))

        
    
    return is_token


# assert not filterNonTokens("8mrvnssRhjcSeSBFQbbHMTUJGRexj5tFaZgEx2HrMRjz")
# assert filterNonTokens("ECMYTGjvXWR3mb5RFEh3F1mAqFBe5EEe53A2n1F1sbpg")