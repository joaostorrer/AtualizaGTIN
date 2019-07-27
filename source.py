from selenium import webdriver
import pandas as pd

arquivoExcel = pd.read_excel("GTIN.xlsx")

browser = webdriver.Chrome()
browser.get('https://www.gs1.org/services/check-digit-calculator')


def get13Digits(cd_material):
    return '0' * (13 - len(str(cd_material))) + str(cd_material)


def getGtin(cd_material):
    input = browser.find_elements_by_xpath("//*[@id='digit']")[0]
    input.send_keys(cd_material)
    calculate = browser.find_elements_by_xpath("//*[@id='edit-submit']")[0]
    calculate.click()
    gtin = browser.find_elements_by_xpath("/html/body/div[2]/section/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div[1]/div/div[2]/span[2]/div/div[1]")[0]
    check_digit = str(gtin.text)
    clear = browser.find_elements_by_xpath("//*[@id='reset-digit']")[0]
    clear.click()
    return str(cd_material)[1:] + check_digit


if __name__ == "__main__":
    for i in range(0,194):
        aux = get13Digits(arquivoExcel.iloc[i,0])
        arquivoExcel.iloc[i,1] = getGtin(aux)

    print(arquivoExcel.head())
    arquivoExcel.to_excel("GTINFinal.xlsx")