Time Series Analysis
================

## Analysing time series with R

The following graph represnets airline passengers each month from 1949
to 1961. This is a pre-loaded dataset in R.

``` r
data = AirPassengers
plot(data, ylab = "Passengers in thousands", xlab = "Months")
library(forecast)
```

    ## Warning: package 'forecast' was built under R version 3.6.3

    ## Registered S3 method overwritten by 'quantmod':
    ##   method            from
    ##   as.zoo.data.frame zoo

![](time-series_files/figure-gfm/unnamed-chunk-1-1.png)<!-- -->

Let’s select a lag of 3 (order) and plot our data with the moving
average line

``` r
movavg = ma(data, order = 3)
plot(data)
lines(movavg, lwd = 2, col = "blue")
```

![](time-series_files/figure-gfm/unnamed-chunk-2-1.png)<!-- -->

Also we can compare R built in smoothing functions: Holt-Winters and ETS

``` r
etsdata = ets(data, allow.multiplicative.trend = TRUE)
hwdata = HoltWinters(data, seasonal = "multiplicative")
plot(hwdata$fitted[,1], col = 'red', ylab = 'Smoothed Passangers')
lines(etsdata$fitted, col = 'blue')
```

![](time-series_files/figure-gfm/unnamed-chunk-3-1.png)<!-- -->

The smoothing paramers for the models were as follows:

``` r
etsdata$par[1:3]
```

    ##       alpha        beta       gamma 
    ## 0.730713737 0.012342052 0.000102091

``` r
c(hwdata$alpha, hwdata$beta, hwdata$gamma)
```

    ##      alpha       beta      gamma 
    ## 0.27559247 0.03269295 0.87072922

We can also de-seasonalize the graph:

``` r
stl(data, "periodic") %>% seasadj() %>% plot()
```

![](time-series_files/figure-gfm/unnamed-chunk-5-1.png)<!-- -->

Or de-trend to see only seasonal fluctuations:

``` r
lm(data~c(1:length(data))) %>% resid() %>% plot(type = 'l')
```

![](time-series_files/figure-gfm/unnamed-chunk-6-1.png)<!-- -->

We can also predict our values with a 95% confidence interval by using
the forecast package with ETS:

``` r
ff = forecast(data, h = 12, level = 95, allow.multiplicative.trend = TRUE)
ff$method
```

    ## [1] "ETS(M,Md,M)"

``` r
ff$model$par[1:3]
```

    ##       alpha        beta       gamma 
    ## 0.730713737 0.012342052 0.000102091

``` r
plot(ff)
```

![](time-series_files/figure-gfm/unnamed-chunk-7-1.png)<!-- -->

``` r
accuracy(ff)[5]
```

    ## [1] 2.838148

And Holt-Winters model:

``` r
fh = hw(data, h = 12, seasonal = "multiplicative", level = 95)
fh$method
```

    ## [1] "Holt-Winters' multiplicative method"

``` r
fh$model$par[1:3]
```

    ##      alpha       beta      gamma 
    ## 0.31461094 0.00705355 0.59772031

``` r
plot(fh)
```

![](time-series_files/figure-gfm/unnamed-chunk-8-1.png)<!-- -->

``` r
accuracy(fh)[5]
```

    ## [1] 2.914411

Both forecasts work the same if same alpha, beta and gamma arguments are
passed, the only difference is how both functions optimize for
minimizing error. However, both forecasts showed less than 3% error.

``` r
forecast(data, h = 12, level = 95, alpha = 0.3146, beta = 0.0070, gamma = 0.5977) %>% plot()
```

![](time-series_files/figure-gfm/unnamed-chunk-9-1.png)<!-- -->

Optimizing a smoothing coefficient can be done by simply iterating
through all possible variables and comparing errors, for example we will
try to find an optimal gamma coefficient only by checking for MAPE while
comparing our forecast results to a test set.

``` r
train = window(data, end = c(1957, 12))
test = window(data, start = c(1958, 1))

gamma = seq(0.01, 0.99, by = 0.01)
MAPE = NA

for (i in seq_along(gamma)) {
     train_ets = ets(train, model = "MAM", gamma = gamma[i])
     train_f = forecast(train_ets, h = 36)
     MAPE[i] = accuracy(train_f, test) [2,5]
}

error = data.frame(gamma, MAPE)
minerr = error[error$MAPE == min(error$MAPE),]

plot(error, type = 'l')
points(minerr, pch = 19, col = 'red')
```

![](time-series_files/figure-gfm/unnamed-chunk-10-1.png)<!-- -->

``` r
minerr
```

    ##    gamma     MAPE
    ## 97  0.97 4.001255

Now let’s plot our new gamma forecast

``` r
forecast(train, h = 36, gamma = minerr$gamma, level = 95) %>% plot()
lines(test, col = 'red', lty = 2)
```

![](time-series_files/figure-gfm/unnamed-chunk-11-1.png)<!-- -->

And check for the model improvement

``` r
new_forecast = forecast(train, h = 36, gamma = minerr$gamma, level = 95)
old_forecast = forecast(train, h = 36, level = 95)

print("New model MAPE")
```

    ## [1] "New model MAPE"

``` r
accuracy(new_forecast, test) [2, 5]
```

    ## [1] 4.001255

``` r
print("Old model MAPE")
```

    ## [1] "Old model MAPE"

``` r
accuracy(old_forecast, test) [2, 5]
```

    ## [1] 7.940007

``` r
if (accuracy(new_forecast, test) [2, 5] < accuracy(old_forecast, test) [2, 5] ) {
    print("Success, we have improved the model!")
} else {
    print("We have not improved the model :( ")
}
```

    ## [1] "Success, we have improved the model!"
