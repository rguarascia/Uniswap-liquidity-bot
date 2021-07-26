#!/usr/bin/env python

import requests
import json
import logging


def getTokenAPI(token):
    url = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"

    payload = "{\"query\":\"query tokens($value: String, $id: String) {\\n    asSymbol: tokens(where: { symbol_contains: $value }, orderBy: totalValueLockedUSD, orderDirection: desc) {\\n      id\\n      symbol\\n      name\\n      totalValueLockedUSD\\n    }\\n    asName: tokens(where: { name_contains: $value }, orderBy: totalValueLockedUSD, orderDirection: desc) {\\n      id\\n      symbol\\n      name\\n      totalValueLockedUSD\\n    }\\n    asAddress: tokens(where: { id: $id }, orderBy: totalValueLockedUSD, orderDirection: desc) {\\n      id\\n      symbol\\n      name\\n      totalValueLockedUSD\\n    }\\n  }\",\"variables\":{\"value\":\""+token + "\",\"id\":\""+token+"\"}}"

    headers = {
        'authority': 'api.thegraph.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'accept': '*/*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
        'content-type': 'application/json',
        'origin': 'https://info.uniswap.org',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://info.uniswap.org/',
        'accept-language': 'en-US,en;q=0.9'
    }

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
    headers = {
        'authority': 'api.thegraph.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'accept': '*/*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
        'content-type': 'application/json',
        'origin': 'https://info.uniswap.org',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://info.uniswap.org/',
        'accept-language': 'en-US,en;q=0.9'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    body = json.loads(response.text)

    filtered = list(filter(lambda x: x["token1"]['symbol']
                           == pool, body['data']['pool']))

    if(not filtered):
        if (pool == "ETH"):
            pool = "WETH"
            filtered = list(filter(lambda x: x["token1"]['symbol']
                                   == pool, body['data']['pool']))

    if(not filtered):
        return False

    filtered = sorted(filtered, key=lambda k: float(k.get(
        'totalValueLockedUSD', 0)), reverse=True)

    return filtered
