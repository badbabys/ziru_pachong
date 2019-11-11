import requests
from  bs4 import BeautifulSoup

html_file = open('ziru_tongzhou.html', 'w', encoding='UTF-8')

html_file.write('''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>自如通州</title>
    <link href="https://cdn.bootcss.com/bootstrap/4.0.0/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<h1 class="text-center">通州区价格1800以下</h1>
<table class="table table-striped table-hover mx-auto text-center">
    <thead>
        <tr>
            <th>图片</th>
            <th>地址</th>
            <th>空间</th>
            <th>楼层</th>
            <th>距离</th>
        </tr>
    </thead>
    <tbody>
''')
headers = {'Referer': 'http://www.ziroom.com/z/', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}

def tongzhou(url):
    # url = r"http://www.ziroom.com/z/d23008625-r0/?cp=0TO1800"
         # r "http://www.ziroom.com/z/d23008625-r0-p1/?sort=3&cp=0TO1800"
    #返回响应
    response = requests.get(url,headers = headers)
    #打印状态
    print(response.status_code)
    # print(response.status_code)
    #获取页面
    html = response.text
    #清洗页面
    bs = BeautifulSoup(html,"lxml")
    #找到覆盖的数据信息 的div
    div = bs.find('div', class_ = "Z_list-box")
    # print(div)

    for fang in div.find_all('div',class_="item"):
        try:
            jpg = fang.find('img',class_="lazy")['data-original']
            if str(jpg).endswith('.jpg'):
                print(jpg)
                jpg = 'http:' + str(jpg)
                name = fang.find('h5').text
                distance = fang.find('div', class_="desc")
                array_flo_add = str(distance.text).replace("\n", "").strip().split("\t")
                flo_spa = array_flo_add[0].strip().split("|")
                floor = flo_spa[0]
                space = flo_spa[-1]
                distance_add = array_flo_add[-1].strip()
                html_file.write('''
                            <tr>
                                <td><img src="{}", width="150" height="100"></td>
                                <td text-align="center">{}</td>
                                <td text-align="center">{}</td>
                                <td text-align="center">{}</td>
                                <td text-align="center">{}</td>
                            </tr>
                        '''.format(jpg, name,floor,space, distance_add))
            else :
                continue
        except AttributeError as e:
            pass

    page = bs.find("a", class_="next")
    new_url = page['href']
    print(new_url)
    if new_url:
        tongzhou("http:" + new_url)
    else:
        raise 0
#路径
url = r"http://www.ziroom.com/z/d23008625-r0/?cp=0TO1800"
      # r"http://www.ziroom.com/z/d23008625-r0-p2/?cp=0TO1800"
tongzhou(url)


html_file.write("""
     </tbody>
</table>
</body>
</html>
""")
html_file.close()
print('write_finished!')
