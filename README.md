# Table of Contents
1. [Introduction](README.md#introduction)
2. [Challenge summary](README.md#challenge-summary)
3. [Details of challenge](README.md#details-of-challenge)
4. [Input files](README.md#input-files)
5. [Output file](README.md#output-file)
6. [Percentile computation](README.md#percentile-computation)
7. [Example](README.md#example)
8. [Writing clean, scalable and well-tested code](README.md#writing-clean-scalable-and-well-tested-code)
9. [Repo directory structure](README.md#repo-directory-structure)
10. [Testing your directory structure and output format](README.md#testing-your-directory-structure-and-output-format)
11. [Instructions to submit your solution](README.md#instructions-to-submit-your-solution)
12. [FAQ](README.md#faq)

# Introduction
You’re a data engineer working for political consultants whose clients are cash-strapped political candidates. They've asked for help analyzing loyalty trends in campaign contributions, namely identifying areas of repeat donors and calculating how much they're spending.

The Federal Election Commission regularly publishes campaign contributions, and while you don’t want to pull specific donors from those files — because using that information for fundraising or commercial purposes is illegal — you want to identify areas (zip codes) that could be sources of repeat campaign contributions. 

# Challenge summary

For this challenge, we're asking you to take a file listing individual campaign contributions for multiple years, determine which ones came from repeat donors, calculate a few values and distill the results into a single output file, `repeat_donors.txt`.

For each recipient, zip code and calendar year, calculate these three values for contributions coming from repeat donors:

* total dollars received
* total number of contributions received 
* donation amount in a given percentile

The political consultants, who are primarily interested in donors who have contributed in multiple years, are concerned about possible outliers in the data. So they have asked that your program allow for a variable percentile. That way the program could calculate the median (or the 50th percentile) in one run and the 99th percentile in another.

Another developer has been placed in charge of building the graphical user
interface with a dashboard showing the latest metrics on repeat donors, among other things. 

Your role on the project is to work on the data pipeline that will hand off the information to the front-end. As the backend data engineer, you do **not** need to display the data or work on the dashboard but you do need to provide the information.

You can assume there is another process that takes what is written to the output file and sends it to the front-end. If we were building this pipeline in real life, we’d probably have another mechanism to send the output to the GUI rather than writing to a file. However, for the purposes of grading this challenge, we just want you to write the output to files.

# Details of challenge

You’re given two input files. 

1. `percentile.txt`, holds a single value -- the percentile value (1-100) that your program will be asked to calculate.

2. `itcont.txt`, has a line for each campaign contribution that was made on a particular date from a donor to a political campaign, committee or other similar entity. 

Out of the many fields listed on the pipe-delimited lines of `itcont.txt` file, you’re primarily interested in the contributor's name, zip code associated with the donor, amount contributed, date of the transaction and ID of the recipient. 

#### Identifying repeat donors
For the purposes of this challenge, if a donor had previously contributed to any recipient listed in the `itcont.txt` file in any prior calendar year, that donor is considered a repeat donor. Also, for the purposes of this challenge, you can assume two contributions are from the same donor if the names and zip codes are identical.

#### Calculations
Each line of `itcont.txt` should be treated as a record. Your code should process each line as if that record was sequentially streaming into your program.  In other words, your program processes every line of `itcont.txt` in the same order as it is listed in the file.

For each record that you identify as coming from a donor who has contributed to a campaign in a prior calendar year, calculate the running percentile of contributions from repeat donors, total number of transactions from repeat donors and total amount of donations streaming in from repeat donors so far for that calendar year, recipient and zip code. 

Write the calculated fields out onto a pipe-delimited line and then print it to an output file named `repeat_donors.txt` in the same order as the donation appeared in the input file.

## Input files

The Federal Election Commission provides data files stretching back years and is [regularly updated](http://classic.fec.gov/finance/disclosure/ftpdet.shtml).

For the purposes of this challenge, we’re interested in individual contributions. While you're welcome to run your program using the data files found at the FEC's website, you should not assume that we'll be testing your program on any of those data files or that the lines will be in the same order as what can be found in those files. Our test data files, however, will conform to the data dictionary [as described by the FEC](http://classic.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml).

Also, while there are many fields in the file that may be interesting, below are the ones that you’ll need to complete this challenge:

* `CMTE_ID`: identifies the flier, which for our purposes is the recipient of this contribution
* `NAME`: name of the donor
* `ZIP_CODE`:  zip code of the contributor (we only want the first five digits/characters)
* `TRANSACTION_DT`: date of the transaction
* `TRANSACTION_AMT`: amount of the transaction
* `OTHER_ID`: a field that denotes whether contribution came from a person or an entity 

### Input file considerations

Here are some considerations to keep in mind:

1. While the data dictionary has the `ZIP_CODE` occupying nine characters, for the purposes of the challenge, we only consider the first five characters of the field as the zip code
2. Because the data set doesn't contain a unique donor id, you should use the combination of `NAME` and `ZIP_CODE` (again, first five digits) to identify a unique donor
3. For the purposes of this challenge, you can assume the input file follows the data dictionary noted by the FEC for the 2015-current election years, although you should not assume the year field holds any particular value
4. The transactions noted in the input file are not in any particular order, and in fact, can be out of order chronologically
5. Because we are only interested in individual contributions, we only want records that have the field, `OTHER_ID`, set to empty. If the `OTHER_ID` field contains any other value, you should completely ignore and skip the entire record 
6. Other situations you can completely ignore and skip an entire record:

* If `TRANSACTION_DT` is an invalid date (e.g., empty, malformed)
* If `ZIP_CODE` is an invalid zip code (i.e., empty, fewer than five digits)
* If the `NAME` is an invalid name (e.g., empty, malformed)
* If any lines in the input file contains empty cells in the `CMTE_ID` or `TRANSACTION_AMT` fields

 Except for the considerations noted above with respect to `CMTE_ID`, `NAME`, `ZIP_CODE`, `TRANSACTION_DT`, `TRANSACTION_AMT`, `OTHER_ID`, data in any of the other fields (whether the data is valid, malformed, or empty) should not affect your processing. That is, as long as the previously noted considerations apply, you should process the record as if it was a valid, newly arriving transaction. (For instance, campaigns sometimes retransmit transactions as amendments, however, for the purposes of this challenge, you can ignore that distinction and treat all of the lines as if they were new)


## Output file

For the  output file that your program will create, `repeat_donors.txt`, the fields on each line should be separated by a `|`

The output should contain the same number of lines or records as the input data file, `itcont.txt`,  minus any records that were ignored as a result of the 'Input file considerations' and any records you determine did not originate from a repeat donor. 

Each line of this file should contain these fields:

* recipient of the contribution (or `CMTE_ID` from the input file)
* 5-digit zip code of the contributor (or the first five characters of the `ZIP_CODE` field from the input file)
* 4-digit year of the contribution
* running percentile of contributions received from repeat donors to a recipient streamed in so far for this zip code and calendar year. Percentile calculations should be rounded to the whole dollar (drop anything below $.50 and round anything from $.50 and up to the next dollar) 
* total amount of contributions received by recipient from the contributor's zip code streamed in so far in this calendar year from repeat donors
* total number of transactions received by recipient from the contributor's zip code streamed in so far this calendar year from repeat donors

## Percentile computation

The first line of `percentile.txt` contains the percentile you should compute for these given input pair. For the percentile computation use the **nearest-rank method** [as described by Wikipedia](https://en.wikipedia.org/wiki/Percentile).

# Example

Suppose your input files contained only the following few lines. Note that the fields we are interested in are in **bold** below but will not be like that in the input file. There's also an extra newline between records below, but the input file won't have that.

**`percentile.txt`**
> **30**

**`itcont.txt`**

> **C00629618**|N|TER|P|201701230300133512|15C|IND|**PEREZ, JOHN A**|LOS ANGELES|CA|**90017**|PRINCIPAL|DOUBLE NICKEL ADVISORS|**01032017**|**40**|**H6CA34245**|SA01251735122|1141239|||2012520171368850783

> **C00177436**|N|M2|P|201702039042410894|15|IND|**DEEHAN, WILLIAM N**|ALPHARETTA|GA|**300047357**|UNUM|SVP, SALES, CL|**01312017**|**384**||PR2283873845050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029337

> **C00384818**|N|M2|P|201702039042412112|15|IND|**ABBOTT, JOSEPH**|WOONSOCKET|RI|**028956146**|CVS HEALTH|VP, RETAIL PHARMACY OPS|**01122017**|**250**||2017020211435-887|1147467|||4020820171370030285

> **C00384516**|N|M2|P|201702039042410893|15|IND|**SABOURIN, JAMES**|LOOKOUT MOUNTAIN|GA|**028956146**|UNUM|SVP, CORPORATE COMMUNICATIONS|**01312017**|**230**||PR1890575345050|1147350||P/R DEDUCTION ($115.00 BI-WEEKLY)|4020820171370029335

> **C00177436**|N|M2|P|201702039042410895|15|IND|**JEROME, CHRISTOPHER**|LOOKOUT MOUNTAIN|GA|**307502818**|UNUM|EVP, GLOBAL SERVICES|**10312017**|**384**||PR2283905245050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029342

> **C00384516**|N|M2|P|201702039042412112|15|IND|**ABBOTT, JOSEPH**|WOONSOCKET|RI|**028956146**|CVS HEALTH|EVP, HEAD OF RETAIL OPERATIONS|**01122018**|**333**||2017020211435-910|1147467|||4020820171370030287

> **C00384516**|N|M2|P|201702039042410894|15|IND|**SABOURIN, JAMES**|LOOKOUT MOUNTAIN|GA|**028956146**|UNUM|SVP, CORPORATE COMMUNICATIONS|**01312018**|**384**||PR2283904845050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029339

The single line on `percentile.txt` tells us that we need to compute the 30th percentile for the stream in `itcont.txt`. If we were to pick the relevant fields from each line, here is what we would record for each line.

**`itcont.txt`**
 
    1.
    CMTE_ID: C00629618
    NAME: PEREZ, JOHN A
    ZIP_CODE: 90017
    TRANSACTION_DT: 01032017
    TRANSACTION_AMT: 40
    OTHER_ID: H6CA34245

    2.
    CMTE_ID: C00177436
    NAME: DEEHAN, WILLIAM N
    ZIP_CODE: 30004
    TRANSACTION_DT: 01312017
    TRANSACTION_AMT: 384
    OTHER_ID: empty

    3. 
    CMTE_ID: C00384818
    NAME: ABBOTT, JOSEPH
    ZIP_CODE: 02895
    TRANSACTION_DT: 01122017
    TRANSACTION_AMT: 250
    OTHER_ID: empty

    4.
    CMTE_ID: C00384516
    NAME: SABOURIN, JAMES
    ZIP_CODE: 02895
    TRANSACTION_DT: 01312017
    TRANSACTION_AMT: 230
    OTHER_ID: empty
  
    5.
    CMTE_ID: C00177436
    NAME: JEROME, CHRISTOPHER
    ZIP_CODE: 30750
    TRANSACTION_DT: 10312017
    TRANSACTION_AMT: 384
    OTHER_ID: empty

    6.
    CMTE_ID: C00384516
    NAME: ABBOTT, JOSEPH 
    ZIP_CODE: 02895
    TRANSACTION_DT: 01122018
    TRANSACTION_AMT: 333
    OTHER_ID: empty

    7.
    CMTE_ID: C00384516
    NAME: SABOURIN, JAMES
    ZIP_CODE: 02895
    TRANSACTION_DT: 01312018
    TRANSACTION_AMT: 384
    OTHER_ID: empty


In processing the `itcont.txt` file line by line, we would ignore the first record because the `OTHER_ID` field contains data and is not empty. 

The next four records don't include any contributions from repeat donors so we ignore them.

But the sixth record includes a donation from `ABBOTT, JOSEPH` with a `ZIP_CODE` of `02895` on Jan. 12, 2018. That same donor contributed in Jan. 12, 2017. That means this contributor is a repeat donor.

So now, we would look for any contributions from repeat donors for recipient `C00384516` and zip of `02895` for the year `2018`. We would then find that the sixth record would be the only one that would qualify. So we would emit

* the total number of contributions from repeat donors is `1`
* the total dollar amount of contributions is `333`
* the 30th percentile contribution is `333` 

The seventh record also is for a repeat donor because `SABOURIN, JAMES`, who contributed Jan. 31, 2018, also contributed Jan. 31, 2017.

When we look for any contributions from repeat donors for recipient, `C00384516`, zip of `02895` for the year `2018`, we would find that the sixth and seventh records qualify. So we would emit

* the total number of contributions from repeat donors is `2`
* the total dollar amount of contributions is `333` + `384` or `717`
* the 30th percentile contribution is `333`

Processing all of the input lines in `itcont.txt`, the entire contents of `repeat_donors.txt` would be:

    C00384516|02895|2018|333|333|1
    C00384516|02895|2018|333|717|2
    

## Writing clean, scalable and well-tested code

As a data engineer, it’s important that you write clean, well-documented code that scales for large amounts of data. For this reason, it’s important to ensure that your solution works well for a large number of records, rather than just the above example.

It's also important to use software engineering best practices like unit tests, especially since data is not always clean and predictable. For more details about the implementation, please refer to the FAQ below. If further clarification is necessary, email us at <cc@insightdataengineering.com> but please do so only after you have read through the Readme and FAQ one more time and cannot find the answer to your question.

Before submitting your solution you should summarize your approach, dependencies and run instructions (if any) in your `README`.

You may write your solution in any mainstream programming language such as C, C++, C#, Clojure, Erlang, Go, Haskell, Java, Python, Ruby, or Scala. Once completed, submit a link to a Github repo with your source code.

In addition to the source code, the top-most directory of your repo must include the `input` and `output` directories, and a shell script named `run.sh` that compiles and runs the program(s) that implement the required features.

If your solution requires additional libraries, environments, or dependencies, you must specify these in your `README` documentation. See the figure below for the required structure of the top-most directory in your repo, or simply clone this repo.

## Repo directory structure

The directory structure for your repo should look like this:

    ├── README.md 
    ├── run.sh
    ├── src
    │   └── donation-analytics.py
    ├── input
    │   └── percentile.txt
    │   └── itcont.txt
    ├── output
    |   └── repeat_donors.txt
    ├── insight_testsuite
        └── run_tests.sh
        └── tests
            └── test_1
            |   ├── input
            |   │   └── percentile.txt
            |   │   └── itcont.txt
            |   |__ output
            |   │   └── repeat_donors.txt
            ├── your-own-test_1
                ├── input
                │   └── your-own-input-for-itcont.txt
                |── output
                    └── repeat_donors.txt

**Don't fork this repo** and don't use this `README` instead of your own. The content of `src` does not need to be a single file called `donation-analytics.py`, which is only an example. Instead, you should include your own source files and give them expressive names.

## Testing your directory structure and output format

To make sure that your code has the correct directory structure and the format of the output files are correct, we have included a test script called `run_tests.sh` in the `insight_testsuite` folder.

The tests are stored simply as text files under the `insight_testsuite/tests` folder. Each test should have a separate folder with an `input` folder for `percentile.txt` and `itcont.txt` and an `output` folder for `repeat_donors.txt`.

You can run the test with the following command from within the `insight_testsuite` folder:

    insight_testsuite~$ ./run_tests.sh 

On a failed test, the output of `run_tests.sh` should look like:

    [FAIL]: test_1
    [Thu Mar 30 16:28:01 PDT 2017] 0 of 1 tests passed

On success:

    [PASS]: test_1
    [Thu Mar 30 16:25:57 PDT 2017] 1 of 1 tests passed



One test has been provided as a way to check your formatting and simulate how we will be running tests when you submit your solution. We urge you to write your own additional tests. `test_1` is only intended to alert you if the directory structure or the output for this test is incorrect.

Your submission must pass at least the provided test in order to pass the coding challenge.

## Instructions to submit your solution
* To submit your entry please use the link you received in your coding challenge invite email
* You will only be able to submit through the link one time 
* Do NOT attach a file - we will not admit solutions which are attached files 
* Use the submission box to enter the link to your GitHub repo or Bitbucket ONLY
* Link to the specific repo for this project, not your general profile
* Put any comments in the README inside your project repo, not in the submission box
* We are unable to accept coding challenges that are emailed to us 

# FAQ

Here are some common questions we've received. If you have additional questions, please email us at `cc@insightdataengineering.com` and we'll answer your questions as quickly as we can (during PST business hours), and update this FAQ. Again, only contact us after you have read through the Readme and FAQ one more time and cannot find the answer to your question.

### Why are you asking us to assume the data is streaming in? 
As a data engineer, you may want to take into consideration future needs. For instance, the team working on the dashboard may want to re-use the streaming functionality used to create `repeat_donors.txt` file in the future to show a running percentile value and total dollar amount of contributions as they arrive in real-time. It might prove useful in assessing the success of a candidate's fundraising efforts at any moment in time.

### What do I do when the data is listed out of order?
Because donations could appear in any order in the input file, there could be a case where you don't know a contributor is a repeat donor until you encounter the second donation. 

In some cases, the second donation that came later in the file may have a transaction date that is for a previous calendar year. In that case, you should only identify the later donation as coming from a repeat donor and output the requested calculations for that calendar year, zip code and recipient. In this case, there would be no need to revise any lines you may have already outputted earlier.

##### Example

**`percentile.txt`**
> **30**

**`itcont.txt`**

> **C00384516**|N|M2|P|201702039042410894|15|IND|**SABOURIN, JOE**|LOOKOUT MOUNTAIN|GA|**028956146**|UNUM|SVP, CORPORATE COMMUNICATIONS|**01312016**|**484**||PR2283904845050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029339

> **C00384516**|N|M2|P|201702039042410894|15|IND|**SABOURIN, JOE**|LOOKOUT MOUNTAIN|GA|**028956146**|UNUM|SVP, CORPORATE COMMUNICATIONS|**01312015**|**384**||PR2283904845050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029339

> **C00384516**|N|M2|P|201702039042410893|15|IND|**SABOURIN, JOE**|LOOKOUT MOUNTAIN|GA|**028956146**|UNUM|SVP, CORPORATE COMMUNICATIONS|**01312017**|**230**||PR1890575345050|1147350||P/R DEDUCTION ($115.00 BI-WEEKLY)|4020820171370029335

**`repeat_donors.txt`**

    C00384516|02895|2017|230|230|1

### The FEC website describes the TRANSCTION_AMT field as NUMBER(14, 2). What does that mean? 

NUMBER(14,2) means the field is capable of holding a number with a maximum precision of 14 and maximum scale of 2. For instance, both 10000.99 and 10000 would be valid transaction amounts.

### Which Github link should I submit?
You should submit the URL for the top-level root of your repository. For example, this repo would be submitted by copying the URL `https://github.com/InsightDataScience/donation-analytics` into the appropriate field on the application. **Do NOT try to submit your coding challenge using a pull request**, which would make your source code publicly available.

### Do I need a private Github repo?
No, you may use a public repo, there is no need to purchase a private repo. You may also submit a link to a Bitbucket repo if you prefer.

### May I use R, Matlab, or other analytics programming languages to solve the challenge?
It's important that your implementation scales to handle large amounts of data. While many of our Fellows have experience with R and Matlab, applicants have found that these languages are unable to process data in a scalable fashion, so you must consider another language.

### May I use distributed technologies like Hadoop or Spark?
Your code will be tested on a single machine, so using these technologies will negatively impact your solution. We're not testing your knowledge on distributed computing, but rather on computer science fundamentals and software engineering best practices. 

### What sort of system should I use to run my program on (Windows, Linux, Mac)?
You may write your solution on any system, but your source code should be portable and work on all systems. Additionally, your `run.sh` must be able to run on either Unix or Linux, as that's the system that will be used for testing. Linux machines are the industry standard for most data engineering teams, so it is helpful to be familiar with this. If you're currently using Windows, we recommend installing a virtual Unix environment, such as VirtualBox or VMWare, and using that to develop your code. Otherwise, you also could use tools, such as Cygwin or Docker, or a free online IDE such as Cloud9.

### How fast should my program run?
While there are no strict performance guidelines to this coding challenge, we will consider the amount of time your program takes when grading the challenge. Therefore, you should design and develop your program in the optimal way (i.e. think about time and space complexity instead of trying to hit a specific run time value). 

### Can I use pre-built packages, modules, or libraries?
This coding challenge can be completed without any "exotic" packages. While you may use publicly available packages, modules, or libraries, you must document any dependencies in your accompanying README file. When we review your submission, we will download these libraries and attempt to run your program. If you do use a package, you should always ensure that the module you're using works efficiently for the specific use-case in the challenge, since many libraries are not designed for large amounts of data.

### Will you email me if my code doesn't run?
Unfortunately, we receive hundreds of submissions in a very short time and are unable to email individuals if their code doesn't compile or run. This is why it's so important to document any dependencies you have, as described in the previous question. We will do everything we can to properly test your code, but this requires good documentation. More so, we have provided a test suite so you can confirm that your directory structure and format are correct.

### Can I use a database engine?
This coding challenge can be completed without the use of a database. However, if you use one, it must be a publicly available one that can be easily installed with minimal configuration.

### Do I need to use multi-threading?
No, your solution doesn't necessarily need to include multi-threading - there are many solutions that don't require multiple threads/cores or any distributed systems, but instead use efficient data structures.

### What should the format of the output be?
In order to be tested correctly, you must use the format described above. You can ensure that you have the correct format by using the testing suite we've included.

### Should I check if the files in the input directory are text files or non-text files(binary)?
No, for simplicity you may assume that all of the files in the input directory are text files, with the format as described above.

### Can I use an IDE like Eclipse or IntelliJ to write my program?
Yes, you can use whatever tools you want - as long as your `run.sh` script correctly runs the relevant target files and creates the `repeat_donors.txt` file in the `output` directory.

### What should be in the input directory?
You can put any text file you want in the directory since our testing suite will replace it. Indeed, using your own input files would be quite useful for testing. The file size limit on Github is 100 MB so you won't be able to include the larger sample input files in your `input` directory.

### How will the coding challenge be evaluated?
Generally, we will evaluate your coding challenge with a testing suite that provides a variety of inputs and checks the corresponding output. This suite will attempt to use your `run.sh` and is fairly tolerant of different runtime environments. Of course, there are many aspects (e.g. clean code, documentation) that cannot be tested by our suite, so each submission will also be reviewed manually by a data engineer.

### How long will it take for me to hear back from you about my submission?
We receive hundreds of submissions and try to evaluate them all in a timely manner. We try to get back to all applicants **within two or three weeks** of submission, but if you have a specific deadline that requires expedited review, please email us at `cc@insightdataengineering.com`.
