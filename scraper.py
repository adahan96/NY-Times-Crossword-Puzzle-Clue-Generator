from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json

class Clue:
  def __init__(self, text, direction,number,answer):
    self.text = text
    self.direction = direction
    self.number = number
    self.answer = answer

class Cell:
  def __init__(self, letter, is_black,number,loc_i,loc_j):
    self.letter = letter
    self.is_black = is_black
    self.number = number
    self.loc_i = loc_i
    self.loc_j = loc_j

def runScraper():
    driver_path = "./chromedriver.exe"
    driver = webdriver.Chrome()
    #driver.fullscreen_window()
    #driver.fullscreen_window()
    driver.get('https://www.nytimes.com/crosswords/game/mini/')
    driver.implicitly_wait(100)
    ok_button = driver.find_element_by_class_name('buttons-modalButton--1REsR')
    ok_button.click()

    reveal_button = driver.find_element_by_css_selector(".Toolbar-expandedMenu--2s4M4").find_elements_by_css_selector(".Tool-button--39W4J.Tool-tool--Fiz94.Tool-texty--2w4Br")[1]
    reveal_button.click()

    puzzle_button = driver.find_element_by_xpath('//*[@id="root"]/div/div/div[4]/div/main/div[2]/div/div/ul/div[2]/li[2]/ul/li[3]')
    puzzle_button.click()

    reveal_reveal = driver.find_elements_by_class_name('buttons-modalButton--1REsR')[1]
    reveal_reveal.click()

    exit_button = driver.find_element_by_class_name('ModalBody-closeX--2Fmp7')
    exit_button.click()
    #driver.get("https://www.sinanerdinc.com/")


    ####CLUE
    clue_list = driver.find_elements_by_class_name('ClueList-list--2dD5-')

    clue_obj_list = []
    for idx, val in enumerate(clue_list):
        clues = val.text
        clues = clues.splitlines()

        clue_index = 0
        while clue_index < len(clues):
            clue_obj = Clue(clues[clue_index+1],idx,clues[clue_index],None)
            clue_obj_list.append(clue_obj)
            clue_index+=2

    # 0,1 2 3


    ### CELL

    table = driver.find_element_by_css_selector('*[role=\'table\']')
    g = table.find_elements_by_tag_name('g')

    cell_obj_list = []
    for i in range(0,5):
        for j in range(0,5):
            black = None
            cell_values = g[5*i+j]
            text = cell_values.text
            if text is "":
                black = True
            else:
                black = False
            loc_i = i
            loc_j = j
            try:
                text_with_num = text.splitlines()
                text_number = text_with_num[0]
                cell_text = text_with_num[1]
                cell_obj = Cell(cell_text,black,text_number,loc_i,loc_j)
                cell_obj_list.append(cell_obj)
            except:
                cell_text = text
                cell_obj = Cell(cell_text, black, -1, loc_i, loc_j)
                cell_obj_list.append(cell_obj)


    #cells = driver.find_elements_by_xpath('//*[@id="xwd-board"]/g[1]')

    ### construct answers

    for index in range(0,len(clue_obj_list)):
        direction = clue_obj_list[index].direction
        number = clue_obj_list[index].number
        for cell_index in range(0,len(cell_obj_list)):
            if cell_obj_list[cell_index].number == number:
                loc_i = cell_obj_list[cell_index].loc_i
                loc_j = cell_obj_list[cell_index].loc_j
                constructed_answer = cell_obj_list[cell_index].letter
                if clue_obj_list[index].direction == 0: # across
                    for index2 in range(loc_j+1,5):
                        to_be_added = 5*loc_i+index2
                        if cell_obj_list[to_be_added].is_black == False:
                            constructed_answer += cell_obj_list[to_be_added].letter
                        else:
                            break
                elif clue_obj_list[index].direction == 1: # down
                    for index2 in range(loc_i+1,5):
                        to_be_added = 5*index2+loc_j
                        if cell_obj_list[to_be_added].is_black == False:
                            constructed_answer += cell_obj_list[to_be_added].letter
                        else:
                            break

                for index3 in range(0,len(clue_obj_list)):
                    if clue_obj_list[index3].number == number and clue_obj_list[index3].direction == direction :
                        clue_obj_list[index3].answer = constructed_answer

    ###### JSON

    data = {}
    data['clues'] = []
    data['cells'] = []


    for clue in clue_obj_list:
        clue_json = {}
        clue_json['text'] = clue.text
        clue_json['direction'] = clue.direction
        clue_json['number'] = clue.number
        clue_json['answer'] = clue.answer
        data['clues'].append(clue_json)

    for cell in cell_obj_list:
        cell_json = {}
        cell_json['letter'] = cell.letter
        cell_json['isBlack'] = cell.is_black
        cell_json['number'] = cell.number
        cell_json['i'] = cell.loc_i
        cell_json['j'] = cell.loc_j
        data['cells'].append(cell_json)


    driver.close(),

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

