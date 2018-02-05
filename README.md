# TRADE BITCOIN USING SIMPLE GOOGLE TREND STRATEGY

## Explanation
Please read this paper first: https://www.nature.com/articles/srep01684?message-global=remove&utm_source=buffer&utm_medium=twitter&utm_campaign=Buffer:%252BWardPlunet%252Bon%252Btwitter&buffer_share=23ec0&error=cookies_not_supported

This strategy (version 1) can be summarized as the following:

* When the relative change of google trend data for `bitcoin` is positive: BUY
* When the relative change of google trend data for `bitcoin` is negative: SELL

The only parameters is the `delta_t`, which is used to compute the relative change of google trends data.

<<<<<<< HEAD
The script also includes a improved version which can be summarized as the following:

* When the relative change **ratio**, r, is positive: BUY using f(r) percentage of the available cash
* When the relative change **ratio**, r, is negive: SELL f(r) percentage of the available BTC

f(r) is a shifted sigmoid function with parameter `scale`.

## Result
[Imgur](https://i.imgur.com/Y7sUq96.png)
=======
```
THIS IS JUST A SIMPLE DEMO. NOT A TRADING ALGO. NO STATISTICAL TEST HAS BEEN DONE.
```

>>>>>>> 375e6343b28ea7d929fbe1e958bb4d6976d1a06c
