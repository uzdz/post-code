import requests
import xlwt
from bs4 import BeautifulSoup

home_url = "https://worldpostalcode.com"
list_data = list()


# 检查是否有codes
def check_codes(currentSoup):
    codes = currentSoup.find(name='div', attrs={"class": "codes"})
    return codes is not None


# 检查是否有codes
def check_regions(currentSoup):
    regions = currentSoup.find(name='div', attrs={"class": "regions"})
    return regions is not None


def get_regions_list(currentSoup):
    # 获取region
    regions = currentSoup.find(name='div', attrs={"class": "regions"})
    a_links = regions.findAll("a")
    list_next_url = []

    for link in a_links:
        list_next_url.append(link["href"])

    # print(list_next_url)
    return list_next_url


def output_word(data, output_path):
    wb = xlwt.Workbook()
    # 添加一个表
    ws = wb.add_sheet('post')

    for max_x, max_y in enumerate(data):
        print(max_y)
        for min_x, min_y in enumerate(max_y):

            if isinstance(min_y, tuple):
                for x, y in enumerate(min_y):
                    ws.write(max_x, min_x + x, y)
            else:
                ws.write(max_x, min_x, min_y)

    # 保存excel文件
    wb.save(output_path + "/post.xls")


def analysis_code(currentSoup, con):
    # 获取container
    container = currentSoup.findAll(name='div', attrs={"class": "container"})
    for group in list(container):
        current_con = con.copy()
        final_tuple = (group.find(name='div', attrs={"class": "place"}).text,
                       group.find(name='div', attrs={"class": "code"}).text)
        current_con.append(final_tuple)
        list_data.append(current_con)


def analysis(url, con):

    if con is None:
        con = list()
    else:
        list_url = url.split("/")
        if url.endswith("/"):
            con.append(list_url[-2])
        else:
            con.append(list_url[-1])

    response = requests.get(home_url + url + "/")
    response.encoding = response.apparent_encoding
    current_soup = BeautifulSoup(response.text, 'html.parser')

    bool_codes = check_codes(current_soup)
    bool_regions = check_regions(current_soup)
    if bool_codes is False and bool_regions:
        for next_regions in get_regions_list(current_soup):
            to_con = con.copy()
            analysis(next_regions, to_con)
    elif bool_codes is True:
        to_con = con.copy()
        analysis_code(current_soup, to_con)
    else:
        print("到底了，什么东西都没有了...")


if __name__ == '__main__':
    print("请输入XLS输出本机地址：")
    output_path = input()

    print("请输入爬取邮政编码的短地址：")
    output_post_url = input()

    analysis(output_post_url, None)

    output_word(list_data, output_path)

