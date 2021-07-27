#!/usr/bin/env python

import requests
import json

headers = {
    'content-type': 'application/json',
}


def getTokenAPI(token):
    """
    getTokenAPI calls the uniswap tokens query
    :param token: the symbol of the token (ex. ETH, USDC, etc) 
    """
    url = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"

    payload = "{\"query\":\"query tokens($value: String, $id: String) {\\n    asSymbol: tokens(where: { symbol_contains: $value }, orderBy: totalValueLockedUSD, orderDirection: desc) {\\n      id\\n      symbol\\n      name\\n      totalValueLockedUSD\\n    }\\n    asName: tokens(where: { name_contains: $value }, orderBy: totalValueLockedUSD, orderDirection: desc) {\\n      id\\n      symbol\\n      name\\n      totalValueLockedUSD\\n    }\\n    asAddress: tokens(where: { id: $id }, orderBy: totalValueLockedUSD, orderDirection: desc) {\\n      id\\n      symbol\\n      name\\n      totalValueLockedUSD\\n    }\\n  }\",\"variables\":{\"value\":\""+token + "\",\"id\":\""+token+"\"}}"

    response = requests.request("POST", url, headers=headers, data=payload)

    body = json.loads(response.text)

    return list(filter(lambda x: x["symbol"]
                       == token, body['data']['asSymbol']))


def getPoolAPI(token, id, pool):
    """
    getPoolAPI calls the uniswap pool query
    :param token: the address of the token 
    :param id: the symbol for the token
    """
    url = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"

    payload = "{\"query\":\" query pools($tokens: [Bytes]!, $id: String) {\\n    pool: pools(where: { token0_in: $tokens }) {\\n      id\\n      feeTier,\\n      totalValueLockedUSD,\\n      token0 {\\n        id\\n        symbol\\n        name\\n      }\\n      token1 {\\n        id\\n        symbol\\n        name\\n      }\\n    }\\n  }\",\"variables\":{\"tokens\":[\""+token+"\"],\"id\":\""+id+"\"}}"

    response = requests.request("POST", url, headers=headers, data=payload)

    body = json.loads(response.text)

    filtered = list(filter(lambda x: x["token1"]['symbol']
                           == pool, body['data']['pool']))

    if(not filtered):
        if (pool == "ETH"):  # Sometimes ETH is called WETH in the API, so check for that toos
            pool = "WETH"
            filtered = list(filter(lambda x: x["token1"]['symbol']
                                   == pool, body['data']['pool']))
        else:
            return False

    return sorted(filtered, key=lambda k: float(k.get(
        'totalValueLockedUSD', 0)), reverse=True)
