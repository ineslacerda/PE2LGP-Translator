import lxml.html
import argparse

def remove_hidden(file):
    print(file)
    inputfile = open(file, "r", encoding='utf-8')
    file = open(file + "_aux.html", "w+", encoding='utf-8')
    # inputfile.read()

    html_file = ""
    for line in inputfile:
	    if "nbsp;" in line:
                line = ""
	    html_file += line		
	    # file.write(line)

    # file.seek(0)
	# tree = ET.parse(file)
	# root = tree.getroot()
    # print(html_file)
    root = lxml.html.fromstring(html_file)
    # print(root)

    html_file_final = html_file.split("<table>")[0]

    print(html_file_final)
    # file.write(html_file.split("<table>")[0])
    
    # table = root.findall(".//*[@class='label']")
    # print(table)
    for j in root.findall(".//td/table"): #processa as frases todas de uma vez
        html_file_final += "<table>"
        # file.write("<table>")
        index = 0
        while index <= 4:
            # print(index)
            html_file_final += "<tr class='ti-" + str(index) + "'>"
            # file.write("<tr class='ti-" + str(index) + "'>")
            for i in root.findall(".//*[@class='ti-" + str(index) + "']"):
                # print(i)
                for k in i.findall("td"):
                    if k.text:
                        html_file_final += lxml.html.tostring(k, encoding='UTF-8').decode('utf-8')
                        # file.write(lxml.html.tostring(k).decode('ascii'))

                    # print(k.text)
                    # print("class")
                    # if k.find_class("hidden") != "hidden":
                    #     print(k)
                # for n in range(100):
                #     col = "colspan=" + '"' + str(n) + '"'
                #     if i.findall("*[@" + col + "]"):
            html_file_final += "</tr>" 
            # file.write("</tr>")
            index += 1
        html_file_final += "</table>"
        # file.write("</table>")
        
        # table = j.findall(".//*[@class='hidden']")

    # print(table)

    html_file_final += html_file.split("</table>")[-1]

    file.write(html_file_final)

parser = argparse.ArgumentParser()

parser.add_argument('file', help='ficheiro do ELAN')

argss = parser.parse_args()

ficheiro_html = argss.file
print(ficheiro_html)

remove_hidden(ficheiro_html)