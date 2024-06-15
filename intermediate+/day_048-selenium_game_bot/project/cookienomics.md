# Cookienomics

## Goal

The goal of the project is to maximise the effciency of the gameplay towards the highest cookies per second rate after five minutes of gameplay. The game starts with a rate of zero cookies per second. The player robot can exibit clicking behaviour to accrue cookies that are equivalent to in-game currency. Clicking behaviour does not change the cookie rate. The accrued cookies can be used to acquire artifacts that will increase cookie rate and automatically generate cookies.

This documents details the game mechanics and optimal solution for those mechanics. 

## Number of cookies

### Actual cookies

Cookies are stored in the `Cookies` variable. This is the amount that is increased in each cycle and decreased when artifacts are bought.

### Displayed cookies

Is a separate variable `CookiesDisplay`. This is displayed in 'money' div in HTML, but other than display it is meaningless. It will display a slightly lesser amount than the actual `Cookies`, but due to the refresh rate of 3 times per second this difference is negligable.

```
	CookiesDisplay+=(Cookies-CookiesDisplay)*0.5;
	l('money').innerHTML=Beautify(Math.round(CookiesDisplay));
```

## Cookie acquisition

`Cookies` is increased by `ClickCookie` and `AddCookie` functions:
* `ClickCookie` adds one cookie - this triggered when the user clicks on the cookie with a mouse
* `AddCookie` adds the number of cookies passed to the function. The number is dependent on the purchased artifacts and is calculated by the `Main` function (detailed below)


## Artifacts

There are six early game artifacts to be considered. Other artifacts exist within the game, but their price level prohibits their acquisition within the first five minutes of the game. Source code in this document is simplified to reflect this.

### Artifact initial price and cookie rate

Artifacts, their initial price and associated cookie rate is summarised in below table:

| Artifact | Initial Price | Cookie rate |
|--|--|--|
| Cursor | 15 | 1 |
| Grandma | 100 | 4 (base) + 1 for owning at least one of each other type of artifact, except Clicker |
| Factory | 500 | 20 |
| Mine | 2000 | 50 |
| Shipment | 7000 | 100 |
| Lab | 50 000 | 500 |

With each acquired unit of an artifact the price to acquire additional units of the same artifact is increased by 10% rounded up to the nearest integer. 

```
this.Buy=function()
{
    if (Cookies>=this.price)
    {
        Cookies-=this.price;
        this.price=Math.ceil(this.price*1.1);
    }
}
```
Cookie rates associted with artifacts does not change throughout the first five minutes of the game.


## Cookie rate

### Displayed rate

Displayed rate is calculated as one fifth of the sum total of cookie rates associated with each unit of all artifacts. 

```
	var grandmaGain=Math.ceil(4+(Factories?1:0)+(Mines?2:0)+(Shipments?3:0)+(Labs?4:0));

	var cps=0;
	cps+=Labs*500/5;
	cps+=Shipments*100/5;
	cps+=Mines*50/5;
	cps+=Factories*20/5;
	cps+=Grandmas*grandmaGain/5;
	cps+=Cursors/5;
	
	var floater=Math.round(cps*10-Math.floor(cps)*10); // floating point
	cps=Beautify(cps)+(floater?('.'+floater):'');
	l('cps').innerHTML='cookies/second : '+cps;
```

### Actual rate

The `Cookies` variable is updated within the `Main` function, which is triggered recursively every  33,(3) miliseconds, i.e. 30 times per second, or 9000 times within 5 minutes.

```
setTimeout(Main,1000/30);
```
On each run `Main` function will:
* refresh number of artifacts and artifact acquisition price
* recaclualte cookie rate according to the number of artifacts
* increment timer `T` by 1
* update `Cookies` variable in accordance to to timer `T` and number of artifacts

Conditionals for increasing `Cookies` variable are:
```
	if (Labs && T%Math.ceil(150/Labs)==0) AddCookie(500,'labs');
	if (Shipments && T%Math.ceil(150/Shipments)==0) AddCookie(100,'shipments');
	if (Mines && T%Math.ceil(150/Mines)==0) AddCookie(50,'mines');
	if (Factories && T%Math.ceil(150/Factories)==0) AddCookie(20,'factories');
	if (Grandmas && T%Math.ceil(150/Grandmas)==0) AddCookie(grandmaGain,'grandmas');
	if (Cursors && T%Math.ceil(150/Cursors)==0) eventFire(l('cookie'),'mouseup');
```

This means that:
* The cookie rate can be increased at most 30 times per second - once for each execution of `Main function`
* Higher number of artifacts will cause more frequent update of `Cookies` variable up to 150 artifacts, e.g. 
	* T is incremented on every execution of `Main`, thus it will be increased by 150 in 5 seconds
	* Let's assume 1 artifact:
		* if T mod ceiling(150/1) == 0 
		* if T mod ceiling(150) == 0
		* if T mod 150 == 0 <-- will update `Cookies` every 5 seconds
	* Let's assume 2 artifacts of the same kind
		* if T mod ceiling(150/2) == 0 
		* if T mod ceiling(75) == 0
		* if T mod 75 == 0 <-- will update `Cookies` every 2.5 seconds
	* Let's assume 150 artifacts of the same kind
		* if T mod ceiling(150/150) == 0 
		* if T mod ceiling(1) == 0
		* if T mod 1 == 0 <-- will update `Cookies` every time `Main` is executed
	* Let's assume 151 artifacts of the same kind
		* if T mod ceiling(150/151) == 0 
		* if T mod ceiling(0.99) == 0
		* if T mod 1 == 0 <-- will update `Cookies` every time `Main` is executed

However, the rate of increase of artifact acquisition price prohibits acquisition of 150 artifacts of the same kind within 5 minutes of gameplay. 



