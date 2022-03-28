import requests
import execjs

url = "https://fanyi.baidu.com/v2transapi?from=en&to=zh"


def get_sign(word):
    with open("test5.js", "r", encoding="utf8") as f:
        jscode = f.read()
    sign = execjs.compile(jscode).call("e", word)
    return sign


def request(word):
    sign = get_sign(word)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "Cookie": "BIDUPSID=C1D60FBAFF280D92DEA75430FB219DFC; PSTM=1605330633; BAIDUID=C1D60FBAFF280D92A9F88C3BF0F07F3A:FG=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BDUSS=pWODkzTnZSczZUT2JUTWhpbUs0bWJkTFJ2SVZyMmZGa0VQbDBJdGo5VDE4RFZnRVFBQUFBJCQAAAAAAAAAAAEAAAAsVqassszV8dfmAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPVjDmD1Yw5ga1; BDUSS_BFESS=pWODkzTnZSczZUT2JUTWhpbUs0bWJkTFJ2SVZyMmZGa0VQbDBJdGo5VDE4RFZnRVFBQUFBJCQAAAAAAAAAAAEAAAAsVqassszV8dfmAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPVjDmD1Yw5ga1; BAIDUID_BFESS=E5C05BC9E40BD15758E69386EDD517FD:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; __yjs_duid=1_df897e8d50f3f0e9d8eedf62c5c43d211614259579733; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1614345635,1614345643,1614347940,1614401883; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1614401883; ab_sr=1.0.0_NGQ3NjQ4NTAzNGNjNDFhNTQ5ZDVmMDNlYTc1YTQyNmJlM2U1NjI3N2RmZGUyYjc2ZGNiZTUxOWQxNTBmZGYwMzQxNDBmNWU0NTQ3MDg5ZTVhODJhNjg5ZTQ0NGE5MmUx; __yjsv5_shitong=1.0_7_bb0b3e2f7db4e875eaf788202e0f3d2218c5_300_1614401882856_27.226.159.239_63467023"
    }

    form_data = {
        "from": "en" if word[0] in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
                                    "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y",
                                    "z", ] else "zh",
        "to": "zh" or "en",
        "query": word,
        "transtype": "realtime",
        "simple_means_flag": 3,
        "sign": sign,
        "token": "9a20246ac075f19baf61fd6ea99bd648",
        "domain": "common"
    }
    response = requests.post(url, headers=headers, data=form_data)
    print(response.json()["trans_result"]["data"][0])

if __name__ == '__main__':
    
    request("cat")
