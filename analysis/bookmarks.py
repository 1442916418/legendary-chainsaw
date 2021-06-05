from html.parser import HTMLParser
import json


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []
        self.name = ''
        self.url = ''
        self.icon = ''

    # 开始标记
    def handle_starttag(self, tag, attrs):
        # print('handle_starttag tag: <%s>' % tag)
        # print('handle_starttag attrs: <%s>' % attrs)
        if tag == "a":
            if len(attrs) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == "href" or variable == "icon":
                        self.data.append(value)

    # 结束标记
    # def handle_endtag(self, tag):
        # print('handle_endtag tag: </%s>' % tag)

    # 数据
    def handle_data(self, data):
        if data:
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
    if len(list) == 0:
        return

    result = []

    for i in range(0, 10, 2):
        item = {
            'url': list[i],
            'icon': list[i + 1],
            'title': list[i + 2]
        }
        result.append(item)

    return result


if __name__ == "__main__":
    htmlData = ''

    with open('D:\\code\\A_2\\python\\analysis\\bookmarks.txt', encoding='utf-8') as f:
        htmlData = f.read()

    if htmlData:
        parser = MyHTMLParser()
        parser.feed(htmlData)
        parser.close()

        res = ArrayToJson(parser.data)

        if res:
            with open('D:\\code\\A_2\\python\\analysis\\new_bookmarks.json', 'w+') as wr:
                # wr.write(res)
                json.dump(res, wr, ensure_ascii=False)
                print('写入结束')
                wr.close()
