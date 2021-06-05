from html.parser import HTMLParser
import json
from datetime import datetime


class MyHTMLParser(HTMLParser):
    # 读取 html 标签
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []
        self.curStartTag = ''
        self.tagA = 'a'

    # 开始标记
    def handle_starttag(self, tag, attrs):
        # print('handle_starttag tag: <%s>' % tag)
        # print('handle_starttag attrs: <%s>' % attrs)
        self.curStartTag = tag

        if tag == self.tagA:
            if len(attrs) != 0:
                for (variable, value) in attrs:
                    if variable == "href" or variable == "icon":
                        self.data.append(value)

    # 结束标记
    # def handle_endtag(self, tag):
        # print('handle_endtag tag: </%s>' % tag)

    # 数据
    def handle_data(self, data):
        if data and self.curStartTag == self.tagA:
            res = data.replace('\n', '').replace('\r', '').replace(' ', '')
            if res:
                # print('handle_data data: ', res)
                self.data.append(res)

    # 注释
    # def handle_comment(self, data):
    #     print('handle_comment: ', data)

    # 这个方法被用于处理 &name; 形式的命名字符引用（例如 &gt;）
    # def handle_entityref(self, name):
    #     print('handle_entityref: &%s;' % name)

    # 这个方法被用来处理 &#NNN; 和 &#xNNN; 形式的十进制和十六进制字符引用
    # def handle_charref(self, name):
    #     print('handle_charref: &#%s;' % name)


def ArrayToJson(list):
    listLen = len(list)
    if listLen == 0:
        return

    result = []

    for i in range(0, listLen, 3):
        urlIndex = i
        iconIndex = i + 1
        titleIndex = i + 2

        if urlIndex >= listLen:
            urlIndex = listLen - 1

        if iconIndex >= listLen:
            iconIndex = listLen - 1

        if titleIndex >= listLen:
            titleIndex = listLen - 1

        item = {
            'url': list[urlIndex],
            'icon': list[iconIndex],
            'title': list[titleIndex]
        }
        result.append(item)

    return result


def getYMD(y='', m='', d=''):
    year = y or datetime.now().year
    month = m or datetime.now().month
    day = d or datetime.now().day

    return '_%s_%s_%s' % (year, month, day)


def HTMLtoJSON():
    htmlData = ''
    date = getYMD()
    openFilePath = 'analysis\\assets\\bookmarks' + date + '.html'
    openWriteArrFilePath = 'analysis\\dist\\arr_bookmarks' + date + '.json'
    openWriteJsonFilePath = 'analysis\\dist\\json_bookmarks' + date + '.json'

    # 打开 html 文件
    with open(openFilePath, encoding='utf-8') as f:
        htmlData = f.read()
        f.close()

    if htmlData:
        # 读取 html 标签
        parser = MyHTMLParser()
        parser.feed(htmlData)
        parser.close()

        with open(openWriteArrFilePath, 'w', encoding='utf-8') as wr:
            wr.write(json.dumps(parser.data, indent=2, ensure_ascii=False))
            print('TXT 写入结束')
            wr.close()

        res = ArrayToJson(parser.data)

        if res:
            with open(openWriteJsonFilePath, 'w', encoding='utf-8') as wr:
                wr.write(json.dumps(res, indent=4, ensure_ascii=False))
                print('JSON 写入结束')
                wr.close()


if __name__ == "__main__":
    HTMLtoJSON()
