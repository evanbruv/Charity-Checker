#plz save 5:07
#wont work w gibberish cuz of newslinks

import validators, time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, render_template, url_for, request


app = Flask(__name__)
@app.route('/', methods=['POST', 'GET'])


def indexfinal():
    if request.method == 'POST':

        #Input Constants
        orgName = request.form['content']
        urlName = orgName.replace(' ', '+')
        urlNameNews = orgName.replace(' ', '%20')

        #Functionality Constants
        options = webdriver.ChromeOptions()
        options.headless=True
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get('https://apps.irs.gov/app/eos/allSearch.do?ein1=&names=' + urlName + '&resultsPerPage=25&indexOfFirstRow=0&dispatchMethod=searchAll&city=&state=All+States&country=All+Countries&postDateFrom=&postDateTo=&exemptTypeCode=al&deductibility=all&sortColumn=orgName&isDescending=false&submitName=Search')
        irsHpb = driver.window_handles[0]
        driver.execute_script("window.open('');")
        charNavHpb = driver.window_handles[1]
        driver.execute_script("window.open('');")
        newsHpb = driver.window_handles[2]

        #General Constants
        credsToI = "According to the IRS website..."
        credsToII = "According to charitynavigator.org..."
        meaning = "What does this mean?"
        readFiveOh = "Read more about 501(c)3 Organizations"

        #Circumstance 1-3, does not exist on IRS site
        badOrgNotice = "\"" + str(orgName) + "\"" + " is not listed as a 501(c)3 by the IRS."
        badExplain = "Essentially, the organization you entered is not an actual established nonprofit organization and is not likely to be exempt from federal tax income."

        #Circumstances 4-6, does exist on IRS site
        goodOrgNotice = "\"" + str(orgName) + "\"" + " is listed as a 501(c)3 by the IRS."
        goodExplain = "Essentially, the organization you entered is an actual established nonprofit organization and can be exempt from federal tax income."
        goodReadData = "Read more about the Tax Return Copies, Pub 78 Data, Auto-Revocation Lists, Determination Letters, or e-Postcards of the organization you entered"

        #Circumstances 1 & 4, does not exist on charitynavigator.org
        noRatingsYetII = "\"" + str(orgName) + "\" did not share any stats yet."

        #Circumstances 2 & 5, no full info on charitynavigator.org
        notEnoughInfoII = "The organization you entered has not provided needed information for a complete rating."
        badCharNavUrlClickMe = "However, you can still see some of the organization's information here"

        #Circumstances 3 & 6, full info on charitynavigator.org
        goodCharNavUrlClickMe = "View more of your organization's stats"

        #Circumstance 1 ratings
        c1Rating = "Charity Checker rates \"" + str(orgName) + "\" 1 out of 6 stars"

        #Circumstance 2 ratings
        c2Rating = "Charity Checker rates \"" + str(orgName) + "\" 2 out of 6 stars"

        #Circumstance 3 ratings
        c3Rating = "Charity Checker rates \"" + str(orgName) + "\" 3 out of 6 stars"

        #Circumstance 4 ratings
        c4Rating = "Charity Checker rates \"" + str(orgName) + "\" 4 out of 6 stars"

        #Circumstance 5 ratings
        c5Rating = "Charity Checker rates \"" + str(orgName) + "\" 5 out of 6 stars"

        #Circumstance 6 ratings
        c6Rating = "Charity Checker rates \"" + str(orgName) + "\" 6 out of 6 stars"

        #Getting news links
        driver.switch_to_window(newsHpb)
        driver.get('https://news.google.com/search?q=' + urlNameNews + '&hl=en-US&gl=US&ceid=US%3Aen')
        news01 = driver.current_url
        newsTitleA = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/div/main/c-wiz/div[1]/div[1]/div/article/h3/a').text
        newsTitleB = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/div/main/c-wiz/div[1]/div[2]/div/article/h3/a').text
        newsTitleC = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/div/main/c-wiz/div[1]/div[3]/div/article/h3/a').text
        for a in driver.find_elements_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/div/main/c-wiz/div[1]/div[1]/div/article/h3/a'):
            newsLinkA = a.get_attribute('href')
        for a in driver.find_elements_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/div/main/c-wiz/div[1]/div[2]/div/article/h3/a'):
            newsLinkB = a.get_attribute('href')
        for a in driver.find_elements_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/div/main/c-wiz/div[1]/div[3]/div/article/h3/a'):
            newsLinkC = a.get_attribute('href')
        newsOffer = "Here are some recent news articles about \"" + str(orgName) + "\":"
        newsMore = "View more"

        #Checking for status on IRS site
        driver.switch_to_window(irsHpb)
        if len(driver.find_elements_by_xpath("//*[contains(text(), 'Search Tips')]")) > 1: #Does not exist on IRS site
            #Checking for status on charitynavigator.org
            driver.switch_to_window(charNavHpb)
            driver.get('https://www.charitynavigator.org/index.cfm?keyword_list=' + urlName + '&bay=search.results')
            time.sleep(3)
            if len(driver.find_elements_by_xpath("//*[contains(text(), 'Advanced Search')]")) > 1: #Does not exist on charitynavigator.org
                #Circumstance 1: Doesn't exist on irs site or charitynavigator.org
                return render_template('indexfinal.html', credsToI=credsToI, badOrgNotice=badOrgNotice, meaning=meaning, badExplain=badExplain, readFiveOh=readFiveOh, credsToII=credsToII, noRatingsYetII=noRatingsYetII, newsOffer=newsOffer, newsLinkA=newsLinkA, newsTitleA=newsTitleA, newsLinkB=newsLinkB, newsTitleB=newsTitleB, newsLinkC=newsLinkC, newsTitleC=newsTitleC, news01=news01, newsMore=newsMore, c1Rating=c1Rating)

            else: #Does exist on charitynavigator.org
                driver.find_element_by_xpath('//*[@id="searchresults"]/table[1]/tbody/tr[1]/td[1]/div/h3/a').click()
                time.sleep(1)
                if len(driver.find_elements_by_xpath("//*[contains(text(), 'our old design')]")) > 1: #Exists on charitynavigator.org, does not have full info
                    badCharNavUrl = driver.current_url
                    #Circumstance 2: Doesn't exist on irs site but has partial info on charitynavigator.org
                    return render_template('indexfinal.html', credsToI=credsToI, badOrgNotice=badOrgNotice, meaning=meaning, badExplain=badExplain, readFiveOh=readFiveOh, credsToII=credsToII, notEnoughInfoII=notEnoughInfoII, badCharNavUrl=badCharNavUrl, badCharNavUrlClickMe=badCharNavUrlClickMe, newsOffer=newsOffer, newsLinkA=newsLinkA, newsTitleA=newsTitleA, newsLinkB=newsLinkB, newsTitleB=newsTitleB, newsLinkC=newsLinkC, newsTitleC=newsTitleC, news01=news01, newsMore=newsMore, c2Rating=c2Rating)

                else: #Exists on charitynavigator.org, does have full info
                    overallRating1 = "Overall Rating (out of 100): " + driver.find_element_by_xpath("//*[@id='overall']/div[1]/table/tbody/tr/td/div/table/tbody/tr[2]/td[2]").text
                    financialRating1 = "Financial Rating (out of 100): " + driver.find_element_by_xpath("//*[@id='overall']/div[1]/table/tbody/tr/td/div/table/tbody/tr[3]/td[2]").text
                    antRating1 = "Accountability & Transparency Rating (out of 100): " + driver.find_element_by_xpath("//*[@id='overall']/div[1]/table/tbody/tr/td/div/table/tbody/tr[4]/td[2]").text
                    programExpenses1 = "Percent of Charity's total expenses spent on the programs/services it delivers: " + driver.find_element_by_xpath("//*[@id='overall']/div[10]/div/table/tbody/tr[1]/td[3]").text
                    adminExpenses1 = "Administrative Expenses: " + driver.find_element_by_xpath("//*[@id='overall']/div[10]/div/table/tbody/tr[2]/td[3]").text
                    fundraisingExpenses1 = "Fundraising Expenses: " + driver.find_element_by_xpath("//*[@id='overall']/div[10]/div/table/tbody/tr[3]/td[3]").text
                    goodCharNavUrl = driver.current_url
                    #Circumstance 3: Doesn't exist on irs site but has full info on charitynavigator.org
                    return render_template('indexfinal.html', credsToI=credsToI, badOrgNotice=badOrgNotice, meaning=meaning, badExplain=badExplain, readFiveOh=readFiveOh, credsToII=credsToII, overallRating1=overallRating1, financialRating1=financialRating1, antRating1=antRating1, programExpenses1=programExpenses1, adminExpenses1=adminExpenses1, fundraisingExpenses1=fundraisingExpenses1, goodCharNavUrl=goodCharNavUrl, goodCharNavUrlClickMe=goodCharNavUrlClickMe, newsOffer=newsOffer, newsLinkA=newsLinkA, newsTitleA=newsTitleA, newsLinkB=newsLinkB, newsTitleB=newsTitleB, newsLinkC=newsLinkC, newsTitleC=newsTitleC, news01=news01, newsMore=newsMore, c3Rating=c3Rating)

        #Checking for status on IRS site
        else: #Does show up on IRS site
            driver.find_element_by_xpath("""/html/body/div[3]/div[13]/div/div/div[1]/div[2]/div/ul/li/h3/a""").click()
            goodIrsInfoUrl = driver.current_url

            #Checking for status on charitynavigator.org
            driver.switch_to_window(charNavHpb)
            driver.get('https://www.charitynavigator.org/index.cfm?keyword_list=' + urlName + '&bay=search.results')
            time.sleep(3)
            if len(driver.find_elements_by_xpath("//*[contains(text(), 'Advanced Search')]")) > 1: #Does not exist on charitynavigator.org
                #Circumstance 4: Does exist on irs site but not charitynavigator.org
                return render_template('indexfinal.html', credsToI=credsToI, goodOrgNotice=goodOrgNotice, meaning=meaning, goodExplain=goodExplain, readFiveOh=readFiveOh, goodIrsInfoUrl=goodIrsInfoUrl, goodReadData=goodReadData, credsToII=credsToII, noRatingsYetII=noRatingsYetII, newsOffer=newsOffer, newsLinkA=newsLinkA, newsTitleA=newsTitleA, newsLinkB=newsLinkB, newsTitleB=newsTitleB, newsLinkC=newsLinkC, newsTitleC=newsTitleC, news01=news01, newsMore=newsMore, c4Rating=c4Rating)

            else: #Does exist on charitynavigator.org
                driver.find_element_by_xpath('//*[@id="searchresults"]/table[1]/tbody/tr[1]/td[1]/div/h3/a').click()
                time.sleep(1)
                if len(driver.find_elements_by_xpath("//*[contains(text(), 'our old design')]")) > 1: #Exists on charitynavigator.org, does not have full info
                    badCharNavUrl = driver.current_url
                    #Circumstance 5: Does exist on irs site but has partial info on charitynavigator.org
                    return render_template('indexfinal.html', credsToI=credsToI, goodOrgNotice=goodOrgNotice, meaning=meaning, goodExplain=goodExplain, readFiveOh=readFiveOh, goodIrsInfoUrl=goodIrsInfoUrl, goodReadData=goodReadData, credsToII=credsToII, notEnoughInfoII=notEnoughInfoII, badCharNavUrl=badCharNavUrl, badCharNavUrlClickMe=badCharNavUrlClickMe, newsOffer=newsOffer, newsLinkA=newsLinkA, newsTitleA=newsTitleA, newsLinkB=newsLinkB, newsTitleB=newsTitleB, newsLinkC=newsLinkC, newsTitleC=newsTitleC, news01=news01, newsMore=newsMore, c5Rating=c5Rating)

                else: #Exists on charitynavigator.org, does have full info
                    overallRating1 = "Overall Rating (out of 100): " + driver.find_element_by_xpath("//*[@id='overall']/div[1]/table/tbody/tr/td/div/table/tbody/tr[2]/td[2]").text
                    financialRating1 = "Financial Rating (out of 100): " + driver.find_element_by_xpath("//*[@id='overall']/div[1]/table/tbody/tr/td/div/table/tbody/tr[3]/td[2]").text
                    antRating1 = "Accountability & Transparency Rating (out of 100): " + driver.find_element_by_xpath("//*[@id='overall']/div[1]/table/tbody/tr/td/div/table/tbody/tr[4]/td[2]").text
                    programExpenses1 = "Percent of Charity's total expenses spent on the programs/services it delivers: " + driver.find_element_by_xpath("//*[@id='overall']/div[10]/div/table/tbody/tr[1]/td[3]").text
                    adminExpenses1 = "Administrative Expenses: " + driver.find_element_by_xpath("//*[@id='overall']/div[10]/div/table/tbody/tr[2]/td[3]").text
                    fundraisingExpenses1 = "Fundraising Expenses: " + driver.find_element_by_xpath("//*[@id='overall']/div[10]/div/table/tbody/tr[3]/td[3]").text
                    goodCharNavUrl = driver.current_url
                    #Circumstance 6: Does exist on irs site and has full info on charitynavigator.org
                    return render_template('indexfinal.html', credsToI=credsToI, goodOrgNotice=goodOrgNotice, meaning=meaning, goodExplain=goodExplain, readFiveOh=readFiveOh, goodIrsInfoUrl=goodIrsInfoUrl, goodReadData=goodReadData, credsToII=credsToII, overallRating1=overallRating1, financialRating1=financialRating1, antRating1=antRating1, programExpenses1=programExpenses1, adminExpenses1=adminExpenses1, fundraisingExpenses1=fundraisingExpenses1, goodCharNavUrl=goodCharNavUrl, goodCharNavUrlClickMe=goodCharNavUrlClickMe, newsOffer=newsOffer, newsLinkA=newsLinkA, newsTitleA=newsTitleA, newsLinkB=newsLinkB, newsTitleB=newsTitleB, newsLinkC=newsLinkC, newsTitleC=newsTitleC, news01=news01, newsMore=newsMore, c6Rating=c6Rating)

    else:
        return render_template('indexfinal.html')


if __name__ == "__main__":
    app.run(debug=True)
