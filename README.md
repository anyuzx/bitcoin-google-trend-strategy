# TRADE BITCOIN USING SIMPLE GOOGLE TREND STRATEGY

## Explanation
Please read this paper first: https://goo.gl/yQteFm

This strategy (version 1) can be summarized as the following:

* When the relative change of google trend data for `bitcoin` is positive: BUY
* When the relative change of google trend data for `bitcoin` is negative: SELL

The only parameters is the `delta_t`, which is used to compute the relative change of google trends data.

-----

The script also includes two improved versions. Version 2 can be summarized as the following:

* When the relative change **ratio**, r, is positive: BUY using f(r) percentage of the available cash
* When the relative change **ratio**, r, is negive: SELL f(r) percentage of the available BTC

f(r) is a shifted sigmoid function with parameter `scale`.

Version 3 is similar to version 2. But the parameters are separated in BULL and BEAR market. BULL/BEAR are determined by the derivative of the google trends data after applied a savgol fitering.

## Result
![Imgur](https://i.imgur.com/983CgUf.png)

There is also a jupyter notebook for illustration.

```
THIS IS JUST A SIMPLE DEMO. NOT A TRADING ALGO. NO STATISTICAL TEST HAS BEEN DONE.
```
