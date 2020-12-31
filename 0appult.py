import validators, time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, render_template, url_for, request
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':

        #Input Constants
        orgName = request.form['content']
        urlName = orgName.replace(' ', '+')
        urlNameNews = orgName.replace(' ', '%20')

        #Functionality Constants
        options = webdriver.ChromeOptions()
        ua = UserAgent(verify_ssl=False)
        userAgent = ua.random
        options.add_argument(f'user-agent={userAgent}')
        options.add_argument("start-maximized")
        options.headless=True
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        
        #Setting up IRS headles browsing page
        driver.get("https://apps.irs.gov/app/eos/")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, """//*[@id="eos-search-by-select"]""")))
        driver.find_element_by_xpath("//select[@name='searchBy']/option[text()='Organization Name']").click()
        textBox = driver.find_element_by_id('names')
        textBox.send_keys(orgName)
        driver.find_element_by_xpath("""//*[@id="s"]""").click()
        time.sleep(1)
        irsHbp = driver.window_handles[0]
        
        #Setting up other two headless browsing pages
        driver.execute_script("window.open('');")
        charNavHbp = driver.window_handles[1]
        driver.execute_script("window.open('');")
        newsHbp = driver.window_handles[2]

        #General Constants
        credsToI = "According to the IRS website..."
        credsToII = "According to charitynavigator.org..."
        symbolsAlert = "Search terms in the Name field can only include letters, numbers, @, /, \, &, %, (), *, hyphens, spaces, apostrophes, periods, commas, and quotation marks."
        meaning = "What does this mean?"
        readFiveOh = "Read more about 501(c)3 Organizations"
        ccSummary = "Charity Checker's \"" + str(orgName) + "\" summary:"
        c1Explain = "\"" + str(orgName) + "\" is not a certified or valid nonprofit and it does not exist on charitynavigator.org, please make sure you are entering the correct name."
        c2Explain = "\"" + str(orgName) + "\" is a certified and valid nonprofit, but it does not exist on charitynavigator.org so it's stats are unclear."
        c3Explain = "\"" + str(orgName) + "\" is not a certified or valid nonprofit, but it does exist on charitynavigator.org"
        c4Explain = "\"" + str(orgName) + "\" is not a certified and valid nonprofit, but it has great ratings." 
        c5Explain = "\"" + str(orgName) + "\" is a certified and valid nonprofit, but does not have any ratings yet."         
        c6Explain = "\"" + str(orgName) + "\" is a certified and valid nonprofit with great ratings."

        #Circumstance 1, 3, 4, does not exist on IRS site
        badOrgNotice = "\"" + str(orgName) + "\"" + " is not listed as a 501(c)3 by the IRS."
        badExplain = "Essentially, the organization you entered is not an actual established nonprofit organization and is not likely to be exempt from federal tax income."

        #Circumstances 2, 5, 6, does exist on IRS site
        goodOrgNotice = "\"" + str(orgName) + "\"" + " is listed as a 501(c)3 by the IRS."
        goodExplain = "Essentially, the organization you entered is an actual established nonprofit organization and can be exempt from federal tax income."
        goodReadData = "Read more about the Tax Return Copies, Pub 78 Data, Auto-Revocation Lists, Determination Letters, or e-Postcards of the organization you entered"

        #Circumstances 1 & 2, does not exist on charitynavigator.org
        noRatingsYetII = "\"" + str(orgName) + "\" did not share any stats yet."

        #Circumstances 3 & 5, no full info on charitynavigator.org
        notEnoughInfoII = "The organization you entered has not provided needed information for a complete rating."
        badCharNavUrlClickMe = "However, you can still see some of the organization's information here"

        #Circumstances 4 & 6, full info on charitynavigator.org
        goodCharNavUrlClickMe = "View more of your organization's stats"

        #Getting news links
        driver.switch_to_window(newsHbp)
        news01 = 'https://news.google.com/search?q=' + urlNameNews + '&hl=en-US&gl=US&ceid=US%3Aen'
        driver.get(news01)
        newsOffer = "Here is a recent news article about \"" + str(orgName) + "\":"
        newsMore = "View more"
        noNews = "No recent news article about \"" + str(orgName) + "\" was found"
        newsLook = "But you can search for older news articles about your organization here"
        if len(driver.find_elements_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/div/main/c-wiz/div[1]/div[1]/div/article/h3/a')) >= 1:
            global newsTitleA, newsLinkA
            newsTitleA = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/div/main/c-wiz/div[1]/div[1]/div/article/h3/a').text
            newsLinkA = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/div/main/c-wiz/div[1]/div[1]/div/article/h3/a').get_attribute('href')

        #Checking for status on IRS site
        driver.switch_to_window(irsHbp)
        if len(driver.find_elements_by_xpath("//*[contains(text(), 'Your search did not return any results. Please try again.')]")) == 1: #Does not exist on IRS site
            #Checking for status on charitynavigator.org
            driver.switch_to_window(charNavHbp)
            driver.get('https://www.charitynavigator.org/index.cfm?keyword_list=' + urlName + '&bay=search.results')
            time.sleep(3)
            if len(driver.find_elements_by_xpath("//*[contains(text(), 'Advanced Search')]")) > 1: #Does not exist on charitynavigator.org
                #Circumstance 1: Doesn't exist on irs site or charitynavigator.org, now determining news links
                driver.switch_to_window(newsHbp)
                if len(driver.find_elements_by_xpath("//*[contains(text(), 'No results found.')]")) == 1:
                    return render_template('index.html', credsToI=credsToI, badOrgNotice=badOrgNotice, meaning=meaning, badExplain=badExplain, readFiveOh=readFiveOh, credsToII=credsToII, noRatingsYetII=noRatingsYetII, noNews=noNews, newsLook=newsLook, ccSummary=ccSummary, c1Explain=c1Explain)
                else:
                    return render_template('index.html', credsToI=credsToI, badOrgNotice=badOrgNotice, meaning=meaning, badExplain=badExplain, readFiveOh=readFiveOh, credsToII=credsToII, noRatingsYetII=noRatingsYetII, newsOffer=newsOffer, newsLinkA=newsLinkA, newsTitleA=newsTitleA, news01=news01, newsMore=newsMore, ccSummary=ccSummary, c1Explain=c1Explain)

            else: #Does exist on charitynavigator.org
                driver.find_element_by_xpath('//*[@id="searchresults"]/table[1]/tbody/tr[1]/td[1]/div/h3/a').click()
                time.sleep(1)
                if len(driver.find_elements_by_xpath("//*[contains(text(), 'our old design')]")) > 1: #Exists on charitynavigator.org, does not have full info
                    badCharNavUrl = driver.current_url
                    #Circumstance 3: Doesn't exist on irs site but has partial info on charitynavigator.org, now determining news links
                    driver.switch_to_window(newsHbp)
                    if len(driver.find_elements_by_xpath("//*[contains(text(), 'No results found.')]")) == 1:
                        return render_template('index.html', credsToI=credsToI, badOrgNotice=badOrgNotice, meaning=meaning, badExplain=badExplain, readFiveOh=readFiveOh, credsToII=credsToII, notEnoughInfoII=notEnoughInfoII, badCharNavUrl=badCharNavUrl, badCharNavUrlClickMe=badCharNavUrlClickMe, noNews=noNews, newsLook=newsLook, ccSummary=ccSummary, c3Explain=c3Explain)
                    else:
                        return render_template('index.html', credsToI=credsToI, badOrgNotice=badOrgNotice, meaning=meaning, badExplain=badExplain, readFiveOh=readFiveOh, credsToII=credsToII, notEnoughInfoII=notEnoughInfoII, badCharNavUrl=badCharNavUrl, badCharNavUrlClickMe=badCharNavUrlClickMe, newsOffer=newsOffer, newsLinkA=newsLinkA, newsTitleA=newsTitleA, news01=news01, newsMore=newsMore, ccSummary=ccSummary, c3Explain=c3Explain)

                else: #Exists on charitynavigator.org, does have full info
                    overallRating1 = "Overall Rating (out of 100): " + driver.find_element_by_xpath("//*[@id='overall']/div[1]/table/tbody/tr/td/div/table/tbody/tr[2]/td[2]").text
                    financialRating1 = "Financial Rating (out of 100): " + driver.find_element_by_xpath("//*[@id='overall']/div[1]/table/tbody/tr/td/div/table/tbody/tr[3]/td[2]").text
                    antRating1 = "Accountability & Transparency Rating (out of 100): " + driver.find_element_by_xpath("//*[@id='overall']/div[1]/table/tbody/tr/td/div/table/tbody/tr[4]/td[2]").text
                    programExpenses1 = "Percent of Charity's total expenses spent on the programs/services it delivers: " + driver.find_element_by_xpath("//*[@id='overall']/div[10]/div/table/tbody/tr[1]/td[3]").text
                    adminExpenses1 = "Administrative Expenses: " + driver.find_element_by_xpath("//*[@id='overall']/div[10]/div/table/tbody/tr[2]/td[3]").text
                    fundraisingExpenses1 = "Fundraising Expenses: " + driver.find_element_by_xpath("//*[@id='overall']/div[10]/div/table/tbody/tr[3]/td[3]").text
                    goodCharNavUrl = driver.current_url
                    #Circumstance 4: Doesn't exist on irs site but has full info on charitynavigator.org, now determining news links
                    driver.switch_to_window(newsHbp)
                    if len(driver.find_elements_by_xpath("//*[contains(text(), 'No results found.')]")) == 1:
                        return render_template('index.html', credsToI=credsToI, badOrgNotice=badOrgNotice, meaning=meaning, badExplain=badExplain, readFiveOh=readFiveOh, credsToII=credsToII, overallRating1=overallRating1, financialRating1=financialRating1, antRating1=antRating1, programExpenses1=programExpenses1, adminExpenses1=adminExpenses1, fundraisingExpenses1=fundraisingExpenses1, goodCharNavUrl=goodCharNavUrl, goodCharNavUrlClickMe=goodCharNavUrlClickMe, noNews=noNews, newsLook=newsLook, ccSummary=ccSummary, c4Explain=c4Explain)
                    else:
                        return render_template('index.html', credsToI=credsToI, badOrgNotice=badOrgNotice, meaning=meaning, badExplain=badExplain, readFiveOh=readFiveOh, credsToII=credsToII, overallRating1=overallRating1, financialRating1=financialRating1, antRating1=antRating1, programExpenses1=programExpenses1, adminExpenses1=adminExpenses1, fundraisingExpenses1=fundraisingExpenses1, goodCharNavUrl=goodCharNavUrl, goodCharNavUrlClickMe=goodCharNavUrlClickMe, newsOffer=newsOffer, newsLinkA=newsLinkA, newsTitleA=newsTitleA, news01=news01, newsMore=newsMore, ccSummary=ccSummary, c4Explain=c4Explain)

        #Invalid characters in IRS name field
        elif len(driver.find_elements_by_xpath("//*[contains(text(), 'You have entered invalid characters in the Name field.')]")) == 1:
            return render_template('index.html', symbolsAlert=symbolsAlert)

        #Checking for status on IRS site
        else: #Does show up on IRS site
            driver.find_element_by_xpath("""/html/body/div[2]/div[2]/div/div/div[1]/div/div[2]/div/ul/li/h3/a""").click()
            goodIrsInfoUrl = driver.current_url

            #Checking for status on charitynavigator.org
            driver.switch_to_window(charNavHbp)
            driver.get('https://www.charitynavigator.org/index.cfm?keyword_list=' + urlName + '&bay=search.results')
            time.sleep(3)
            if len(driver.find_elements_by_xpath("//*[contains(text(), 'Advanced Search')]")) > 1: #Does not exist on charitynavigator.org
                #Circumstance 2: Does exist on irs site but not charitynavigator.org, now determining news links
                driver.switch_to_window(newsHbp)
                if len(driver.find_elements_by_xpath("//*[contains(text(), 'No results found.')]")) == 1:
                    return render_template('index.html',  credsToI=credsToI, goodOrgNotice=goodOrgNotice, meaning=meaning, goodExplain=goodExplain, readFiveOh=readFiveOh, goodIrsInfoUrl=goodIrsInfoUrl, goodReadData=goodReadData, credsToII=credsToII, noRatingsYetII=noRatingsYetII, noNews=noNews, newsLook=newsLook, ccSummary=ccSummary, c2Explain=c2Explain)
                else:
                    return render_template('index.html',  credsToI=credsToI, goodOrgNotice=goodOrgNotice, meaning=meaning, goodExplain=goodExplain, readFiveOh=readFiveOh, goodIrsInfoUrl=goodIrsInfoUrl, goodReadData=goodReadData, credsToII=credsToII, noRatingsYetII=noRatingsYetII, newsOffer=newsOffer, newsLinkA=newsLinkA, newsTitleA=newsTitleA, news01=news01, newsMore=newsMore, ccSummary=ccSummary, c2Explain=c2Explain)

            else: #Does exist on charitynavigator.org
                driver.find_element_by_xpath('//*[@id="searchresults"]/table[1]/tbody/tr[1]/td[1]/div/h3/a').click()
                time.sleep(1)
                if len(driver.find_elements_by_xpath("//*[contains(text(), 'our old design')]")) > 1: #Exists on charitynavigator.org, does not have full info
                    badCharNavUrl = driver.current_url
                    #Circumstance 5: Does exist on irs site but has partial info on charitynavigator.org, now determining news links
                    if len(driver.find_elements_by_xpath("//*[contains(text(), 'No results found.')]")) == 1:
                        return render_template('index.html', credsToI=credsToI, goodOrgNotice=goodOrgNotice, meaning=meaning, goodExplain=goodExplain, readFiveOh=readFiveOh, goodIrsInfoUrl=goodIrsInfoUrl, goodReadData=goodReadData, credsToII=credsToII, notEnoughInfoII=notEnoughInfoII, badCharNavUrl=badCharNavUrl, badCharNavUrlClickMe=badCharNavUrlClickMe, noNews=noNews, newsLook=newsLook, ccSummary=ccSummary, c5Explain=c5Explain)
                    else:
                        return render_template('index.html', credsToI=credsToI, goodOrgNotice=goodOrgNotice, meaning=meaning, goodExplain=goodExplain, readFiveOh=readFiveOh, goodIrsInfoUrl=goodIrsInfoUrl, goodReadData=goodReadData, credsToII=credsToII, notEnoughInfoII=notEnoughInfoII, badCharNavUrl=badCharNavUrl, badCharNavUrlClickMe=badCharNavUrlClickMe, newsOffer=newsOffer, newsLinkA=newsLinkA, newsTitleA=newsTitleA, news01=news01, newsMore=newsMore, ccSummary=ccSummary, c5Explain=c5Explain)

                else: #Exists on charitynavigator.org, does have full info
                    overallRating1 = "Overall Rating (out of 100): " + driver.find_element_by_xpath("//*[@id='overall']/div[1]/table/tbody/tr/td/div/table/tbody/tr[2]/td[2]").text
                    financialRating1 = "Financial Rating (out of 100): " + driver.find_element_by_xpath("//*[@id='overall']/div[1]/table/tbody/tr/td/div/table/tbody/tr[3]/td[2]").text
                    antRating1 = "Accountability & Transparency Rating (out of 100): " + driver.find_element_by_xpath("//*[@id='overall']/div[1]/table/tbody/tr/td/div/table/tbody/tr[4]/td[2]").text
                    programExpenses1 = "Percent of Charity's total expenses spent on the programs/services it delivers: " + driver.find_element_by_xpath("//*[@id='overall']/div[10]/div/table/tbody/tr[1]/td[3]").text
                    adminExpenses1 = "Administrative Expenses: " + driver.find_element_by_xpath("//*[@id='overall']/div[10]/div/table/tbody/tr[2]/td[3]").text
                    fundraisingExpenses1 = "Fundraising Expenses: " + driver.find_element_by_xpath("//*[@id='overall']/div[10]/div/table/tbody/tr[3]/td[3]").text
                    goodCharNavUrl = driver.current_url
                    #Circumstance 6: Does exist on irs site and has full info on charitynavigator.org, now determining news links
                    if len(driver.find_elements_by_xpath("//*[contains(text(), 'No results found.')]")) == 1:
                        return render_template('index.html', credsToI=credsToI, goodOrgNotice=goodOrgNotice, meaning=meaning, goodExplain=goodExplain, readFiveOh=readFiveOh, goodIrsInfoUrl=goodIrsInfoUrl, goodReadData=goodReadData, credsToII=credsToII, overallRating1=overallRating1, financialRating1=financialRating1, antRating1=antRating1, programExpenses1=programExpenses1, adminExpenses1=adminExpenses1, fundraisingExpenses1=fundraisingExpenses1, goodCharNavUrl=goodCharNavUrl, goodCharNavUrlClickMe=goodCharNavUrlClickMe, noNews=noNews, newsLook=newsLook, ccSummary=ccSummary, c6Explain=c6Explain)
                    else:
                        return render_template('index.html', credsToI=credsToI, goodOrgNotice=goodOrgNotice, meaning=meaning, goodExplain=goodExplain, readFiveOh=readFiveOh, goodIrsInfoUrl=goodIrsInfoUrl, goodReadData=goodReadData, credsToII=credsToII, overallRating1=overallRating1, financialRating1=financialRating1, antRating1=antRating1, programExpenses1=programExpenses1, adminExpenses1=adminExpenses1, fundraisingExpenses1=fundraisingExpenses1, goodCharNavUrl=goodCharNavUrl, goodCharNavUrlClickMe=goodCharNavUrlClickMe, newsOffer=newsOffer, newsLinkA=newsLinkA, newsTitleA=newsTitleA, news01=news01, newsMore=newsMore, ccSummary=ccSummary, c6Explain=c6Explain)

    else:
        return render_template('index.html')


#Integrates the "About Charity Checker" Page
@app.route('/aboutcc', methods=['POST', 'GET'])
def aboutcc():
    if request.method == 'POST':
        return redirct(url_for('index'))
    return render_template('aboutcc.html')


if __name__ == "__main__":
    app.run(debug=True)
