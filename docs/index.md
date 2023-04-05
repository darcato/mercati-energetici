# Async python library for Italian energy markets

Unofficial wrapper of the GME ([Gestore dei Mercati Energetici S.p.A.](https://mercatoelettrico.org/It/Default.aspx)) APP API. It allows to retrieve prices and volumes traded on the Italian energy markets (electricity, gas and environmental) in a simple and asynchronous way.

## Disclaimer

This library is not affiliated with GME ([Gestore dei Mercati Energetici S.p.A.](https://mercatoelettrico.org/It/Default.aspx)) in any way. It is provided as is, without any warranty. By using this library, you agree to the terms of use of GME API, which can be obtained with ``get_general_conditions()`` or can be found [here](https://www.mercatoelettrico.org/it/tools/AccessoDati.aspx). Please, be aware that all the data belongs to GME and can't be used for profit. Also, be aware of the disclaimer from GME retrivable with ``get_disclaimer()``.
