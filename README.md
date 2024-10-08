“Stock prices move around wildly over very short periods of time. This does not mean that the values of the underlying companies have changed very much during that same period. In effect, the stock market acts very much like a crazy guy named Mr. Market.”
— Joel Greenblatt

## Intro 
Nifty Sensex Trends is a very simple and basic code to find average points nifty and sensex
gained for last 2y, 5y, 10y and max. 

TL;DR: 
Just look at nifty.txt and sensex.txt for results. 


## Average Nifty 50 Gains 
Between First Monday after monthly expiry (last Thursday of month) and the corresponding monthly expiry. 

TL;DR:
Just look at 'options-avg-gains-monthly-expiry.log' for raw data and 'options-avg-gains-monthly-expiry.ods' for summarised data color coded. 

## Fun Fact

  - July and November came out as the most profitable months across both the tests 
  - June and December come next 
  - April follows. 

So long story short, one does not have to actively trade throughout the year. If one trades with the right capital during these months, 
they can make enough capital for the whole year. Having said that, one needs to look at the trend of market before taking such decisions
(micro level local data and all). All these tests tell us possibilities and probabilities, which probability manifests in a given year 
can not be said or predicted. So - look before you leap. 

## Disclaimer

The code provided is for informational and educational purposes only. The author is not a financial advisor and does 
not hold any responsibility for any investment decisions or trades made based on the use of this code. Users should 
perform their own research and consult with a qualified financial advisor before making any investment decisions. 
The author will not be liable for any financial losses or damages arising from the use of this code.

## Project Setup 

### Windows 11
```powershell
# Refer to https://github.com/pyenv-win/pyenv-win?tab=readme-ov-file#quick-start
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
# Restart powershell and run the following command to verify
pyenv --version
pyenv install 3.10.14
# Set local python version
pyenv local 3.10.14
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Mac
```bash
brew install pyenv
pyenv install 3.10.14
pyenv local 3.10.14
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Linux 
```bash
# https://stackoverflow.com/questions/77550543/ubuntu-22-04-2-command-pyenv-not-found
curl https://pyenv.run | bash
pyenv install 3.10.14
pyenv local 3.10.14
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
