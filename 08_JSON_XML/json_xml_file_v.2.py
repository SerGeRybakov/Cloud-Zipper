import xml.etree.ElementTree as ET
import json


def get_json(file_path):
    json_desc_lst = []
    with open(file_path, encoding="utf-8") as f:
        file = json.load(f)
    for dic in file["rss"]["channel"]["items"]:
        json_desc_lst.append(dic["description"])
    json_top_10 = get_top_10(json_desc_lst)
    return json_top_10


def get_xml(file_path):
    xml_desc_lst = []
    parser = ET.XMLParser(encoding="utf-8")
    file = ET.parse(file_path, parser)
    xml_lst = file.findall("channel/item/description")
    for i in xml_lst:
        xml_desc_lst.append(i.text)
    xml_top_10 = get_top_10(xml_desc_lst)
    return xml_top_10


def get_top_10(lst):
    word_dict = {}
    for line in lst:
        line = prepare_line(line)
        line_set = set(line)
        for word in line_set:
            counter = 0
            counter += line.count(word)
            if word not in word_dict.keys():
                word_dict[word] = counter
            else:
                word_dict[word] += counter

    values_list = list(set(word_dict.values()))
    values_list.sort(reverse=True)
    top_10_nums = tuple(values_list[:10])
    top_10 = []
    for num in enumerate(top_10_nums):
        for keys, values in word_dict.items():
            if num[1] == values:
                top_10.append(f'{num[0] + 1} место: "{keys}" - {num[1]} раз')
    return top_10_nums, top_10


def prepare_line(line: str) -> list:
    line = line.lower()
    line = line.replace(",", "")
    line = line.replace("'", "")
    line = line.replace('"', "")
    line = line.replace('.', "")
    line = line.strip().split()
    trash = []
    for word in line:
        if len(word) < 7:
            trash.append(word)

    for wordy in trash:
        if wordy in line:
            line.remove(wordy)
    return line


def main():
    json_top = get_json("newsafr.json")
    xml_top = get_xml("newsafr.xml")

    print(f"Топ-10 самых часто встречающихся слов в файле 'newsafr.json':")
    for place in enumerate(json_top[1][:10]):
        print(place[0] + 1, "место", place[1][7:])
    print()

    print(f"Топ-10 самых часто встречающихся слов в файле 'newsafr.xml':")
    for place in enumerate(xml_top[1][:10]):
        print(place[0] + 1, "место", place[1][7:])
    print()


if __name__ == '__main__':
    main()
