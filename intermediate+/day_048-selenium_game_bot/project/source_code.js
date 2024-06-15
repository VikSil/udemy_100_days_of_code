<script>
function eventFire(el, etype){
  if (el.fireEvent) {
    (el.fireEvent('on' + etype));
  } else {
    var evObj = document.createEvent('Events');
    evObj.initEvent(etype, true, false);
    el.dispatchEvent(evObj);
  }
}

function l(what) {return document.getElementById(what);}

Game=l('game');
Version=0.1251;
l('version').innerHTML='running v.'+Version;
Loaded=0;

function Beautify(what)//turns 9999999 into 9,999,999
{
	var str='';
	what=Math.floor(what);
	what=(what+'').split('').reverse();
	for (var i in what)
	{
		if (i%3==0 && i>0) str=','+str;
		str=what[i]+str;
	}
	return str;
}

//CookieSave='<?php echo ($_COOKIE['CookieClickerSave']?('1|'.$_COOKIE['CookieClickerSave']):'0'); ?>';

var str='';
var pics=['cursor','grandma','mine','factory','lab','shipment','goldengrandma','grandmaiconinvert','grandmaiconlustful','portal','skellington','kaleigrandma','factorygrandma','minegrandma','shipmentgrandma','portalgrandma','pledgedgrandma','pledgeicon','timemachine','timegrandma'];
for (var i in pics) {str+='<img src="'+pics[i]+'.png"/>';}
l('hiddenLoader').innerHTML=str;

Cookies=0;
CookiesDisplay=0;
Clicking=0;
Hovering=0;
T=0;

Cursors=0;
Grandmas=0;
Factories=0;
Mines=0;
Shipments=0;
Labs=0;
Portals=0;
Times=0;

Pledge=0;

NumbersOn=1;
Flashing=1;

StoreToRebuild=0;

function ToggleNumbers()
{
	if (NumbersOn) {NumbersOn=0;l('toggleNumbers').innerHTML='Numbers Off';}
	else if (!NumbersOn) {NumbersOn=1;l('toggleNumbers').innerHTML='Numbers On';}
}
function ToggleFlash()
{
	if (Flashing) {Flashing=0;l('toggleFlash').innerHTML='Flashing Off';}
	else if (!Flashing) {Flashing=1;l('toggleFlash').innerHTML='Flashing On';}
}


importSave=function()
{
	var save=prompt('Please paste in the text that was given to you on save export.','');
	if (save && save!='') ImportResponse('1|'+save);
	Save();
}
exportSave=function()
{
	var save=prompt('Copypaste this text and keep it somewhere safe! (yes, it\'s easy to edit - but remember : cheated cookies taste terrible!)',MakeSaveString());
}

ImportResponse=function(response)
{
	var r=response.split('|');
	if (response!='0' && response)
	{
		if (r[0]=='1')
		{
			Cookies=parseInt(r[2]);
			Pledge=0;
			Cursors=Math.min(1000,parseInt(r[3]));Buyables['Cursor'].price=parseInt(r[4]);
			Grandmas=Math.min(1000,parseInt(r[5]));Buyables['Grandma'].price=parseInt(r[6]);
			Factories=Math.min(1000,parseInt(r[7]));Buyables['Factory'].price=parseInt(r[8]);
			Mines=Math.min(1000,parseInt(r[9]));Buyables['Mine'].price=parseInt(r[10]);
			Shipments=Math.min(1000,parseInt(r[11]));Buyables['Shipment'].price=parseInt(r[12]);
			Labs=Math.min(1000,parseInt(r[13]));Buyables['Alchemy lab'].price=parseInt(r[14]);
			if (r[15]) {Portals=Math.min(1000,parseInt(r[15]));Buyables['Portal'].price=parseInt(r[16]);}
			if (r[17]) {Times=Math.min(1000,parseInt(r[17]));Buyables['Time machine'].price=parseInt(r[18]);}
			Buyables['Grandma'].func(0);
			Buyables['Factory'].func(0);
			Buyables['Mine'].func(0);
			Buyables['Shipment'].func(0);
			Buyables['Alchemy lab'].func(0);
			Buyables['Portal'].func(0);
			Buyables['Time machine'].func(0);
			StoreToRebuild=1;
		}
	}
	new Pop('credits','Imported.');
}



Reset=function()
{
	if (confirm('Do you REALLY want to start over?'))
	{
		document.cookie='CookieClickerSave=0; expires=Fri, 3 Aug 2001 20:47:11 UTC;';
		ResetResponse();
	}
	//ajax('backend.php?q=reset',ResetResponse);
}
ResetResponse=function()
{
	location.reload(true);
}

MakeSaveString=function()
{
	var str='';
	str+=Version+'|'+parseInt(Cookies)+'|'+
	parseInt(Cursors)+'|'+parseInt(Buyables['Cursor'].price)+'|'+
	parseInt(Grandmas)+'|'+parseInt(Buyables['Grandma'].price)+'|'+
	parseInt(Factories)+'|'+parseInt(Buyables['Factory'].price)+'|'+
	parseInt(Mines)+'|'+parseInt(Buyables['Mine'].price)+'|'+
	parseInt(Shipments)+'|'+parseInt(Buyables['Shipment'].price)+'|'+
	parseInt(Labs)+'|'+parseInt(Buyables['Alchemy lab'].price)+'|'+
	parseInt(Portals)+'|'+parseInt(Buyables['Portal'].price)+'|'+
	parseInt(Times)+'|'+parseInt(Buyables['Time machine'].price);
	return str;
}

SaveTimer=30*60;
Save=function()
{
	var str=MakeSaveString();
	//ajax('backend.php?q=save|'+str,SaveResponse);
	
	var now=new Date();//we storin dis for 5 years, people
	now.setFullYear(now.getFullYear()+5);//mmh stale cookies
	str='CookieClickerSave='+escape(str)+'; expires='+now.toUTCString()+';';
	document.cookie=str;//aaand save
	//alert(document.cookie);
	if (document.cookie.indexOf('CookieClickerSave')<0) Pop('credits','<span style="color:#f00;">Error while saving.<br>Export your save instead!</span>');
	else Pop('credits','Saved');
	
	SaveTimer=30*60;
}
SaveResponse=function(response)
{
	var r=response.split('|');
	if (r[0]=='1' && parseFloat(r[1])>Version)
	{
		l('alert').style.visibility='visible';
		l('alert').innerHTML='New version available ('+r[1]+').<br>Please refresh to see it!';
	}
	if (r[0]=='1') new Pop('credits','Saved');
	else new Pop('credits','<span style="color:#f00;">Error while saving</span>');
}

Load=function()
{
	var str='0';
	if (document.cookie.indexOf('CookieClickerSave')>=0) str='1|'+unescape(document.cookie.split('CookieClickerSave=')[1]);//get cookie here
	//ajax('backend.php?q=load',LoadResponse);
	LoadResponse(str);
	l('comment').innerHTML='Loading cookie...';
	//LoadResponse(CookieSave);
}

LoadResponse=function(response)
{
	var r=response.split('|');
	if (response!='0' && response)
	{
		if (r[0]=='1')
		{
			Cookies=parseInt(r[2]);
			Pledge=0;
			Cursors=Math.min(1000,parseInt(r[3]));Buyables['Cursor'].price=parseInt(r[4]);
			Grandmas=Math.min(1000,parseInt(r[5]));Buyables['Grandma'].price=parseInt(r[6]);
			Factories=Math.min(1000,parseInt(r[7]));Buyables['Factory'].price=parseInt(r[8]);
			Mines=Math.min(1000,parseInt(r[9]));Buyables['Mine'].price=parseInt(r[10]);
			Shipments=Math.min(1000,parseInt(r[11]));Buyables['Shipment'].price=parseInt(r[12]);
			Labs=Math.min(1000,parseInt(r[13]));Buyables['Alchemy lab'].price=parseInt(r[14]);
			if (r[15]) {Portals=Math.min(1000,parseInt(r[15]));Buyables['Portal'].price=parseInt(r[16]);}
			if (r[17]) {Times=Math.min(1000,parseInt(r[17]));Buyables['Time machine'].price=parseInt(r[18]);}
			Buyables['Grandma'].func(0);
			Buyables['Factory'].func(0);
			Buyables['Mine'].func(0);
			Buyables['Shipment'].func(0);
			Buyables['Alchemy lab'].func(0);
			Buyables['Portal'].func(0);
			Buyables['Time machine'].func(0);
			StoreToRebuild=1;
		}
	}
	new Pop('credits','Loaded.');
	Loaded=1;
k
}

ClickCookie=function()
{
	var howmany=(Pledge>0?Math.ceil(Cursors*1.5):1);
	Cookies+=howmany;
	if (Pops.length<260 && NumbersOn) new Pop('cookie','+'+howmany);
	Clicking=1;
}
HoverCookie=function()
{
	Hovering=1;
}

AddCookie=function(howmany,el)
{
	Cookies+=howmany;
	if (el && Pops.length<250 && NumbersOn) new Pop(el,'+'+howmany);
}

RebuildStore=function()
{
	var str='';
	for (var i in Buyables)
	{
		var amount=0;
		if (Buyables[i].name=='Cursor') amount=Cursors;
		else if (Buyables[i].name=='Grandma') amount=Grandmas;
		else if (Buyables[i].name=='Factory') amount=Factories;
		else if (Buyables[i].name=='Mine') amount=Mines;
		else if (Buyables[i].name=='Shipment') amount=Shipments;
		else if (Buyables[i].name=='Alchemy lab') amount=Labs;
		else if (Buyables[i].name=='Portal') amount=Portals;
		else if (Buyables[i].name=='Time machine') amount=Times;
		str+='<div id="buy'+Buyables[i].name+'" onclick="Buy(\''+Buyables[i].name+'\');" style="'+(Buyables[i].name=='Elder Pledge'?'display:none;':'')+(Buyables[i].name=='Time machine'?'font-size:90%;':'')+'background-image:url('+Buyables[i].pic+'.png);"><b>'+Buyables[i].name+' - <moni></moni> '+Beautify(Buyables[i].price)+'</b>'+Buyables[i].desc+''+(amount>0?('<div class="amount">'+amount+'</div>'):'')+'</div>';
	}
	l('store').innerHTML=str;
	StoreToRebuild=0;
}
Buyables=[];
Buyable=function(name,desc,pic,price,func)
{
	this.name=name;
	this.desc=desc;
	this.pic=pic;
	this.price=price;
	this.func=func;
	Buyables[name]=this;
	
	this.Buy=function()
	{
		if (Cookies>=this.price && Loaded)
		{
			Cookies-=this.price;
			this.price=Math.ceil(this.price*1.1);
			this.func(1);
			//Buyables[this.name]=0;
			StoreToRebuild=1;
		}
	}
	StoreToRebuild=1;
}
Buy=function(what)
{
	Buyables[what].Buy();
}

new Buyable('Cursor','Autoclicks every 5 seconds.','cursoricon',15,function(){Cursors++;});
new Buyable('Grandma','A nice grandma to bake more cookies.','grandmaicon',100,function(buy)
{
	if (buy) Grandmas++;
	var str='';
	for (var i=0;i<Grandmas;i++)
	{
		var x=Math.floor(Math.random()*20+(i%10)*24);
		var y=Math.floor(Math.random()*20+Math.floor(i/10)*24);
		var cl=0;
		if (Labs && Math.random()<0.2) cl='goldengrandma';
		if (Factories && Math.random()<0.2) cl='factorygrandma';
		if (Mines && Math.random()<0.2) cl='minegrandma';
		if (Shipments && Math.random()<0.2) cl='shipmentgrandma';
		if (Portals && Pledge<=0 && Math.random()<0.2) cl='portalgrandma';
		if (Times && Math.random()<0.2) cl='timegrandma';
		if (Pledge && Math.random()<0.2) cl='pledgedgrandma';
		str+='<div class="'+(cl?cl+' ':'')+'grandma" style="left:'+x+'px;top:'+y+'px;"></div>';
	}
	l('grandmas').innerHTML=str;
});
new Buyable('Factory','Produces large quantities of cookies.','factoryicon',500,function(buy)
{
	if (buy) Factories++;
	if (buy && Factories==1) Buyables['Grandma'].func();
	var str='';
	for (var i=0;i<Factories;i++)
	{
		var x=Math.floor(Math.random()*20+(i%10)*32);
		var y=Math.floor(Math.random()*20+Math.floor(i/10)*24);
		str+='<div class="factory" style="right:'+x+'px;top:'+y+'px;"></div>';
	}
	l('factories').innerHTML=str;
});
new Buyable('Mine','Mines out cookie dough and chocolate chips.','mineicon',2000,function(buy)
{
	if (buy) Mines++;
	if (buy && Mines==1) Buyables['Grandma'].func();
	var str='';
	for (var i=0;i<Mines;i++)
	{
		var x=Math.floor(Math.random()*20+(i%10)*16);
		var y=Math.floor(Math.random()*20+Math.floor(i/10)*16);
		str+='<div class="mine" style="left:'+x+'px;top:'+y+'px;"></div>';
	}
	l('mines').innerHTML=str;
});
new Buyable('Shipment','Brings in fresh cookies from the cookie planet.','shipmenticon',7000,function(buy)
{
	if (buy) Shipments++;
	if (buy && Shipments==1) Buyables['Grandma'].func();
	var str='';
	for (var i=0;i<Shipments;i++)
	{
		var x=Math.floor(Math.random()*20+(i%10)*24);
		var y=Math.floor(Math.random()*20+Math.floor(i/10)*24);
		str+='<div class="shipment" style="right:'+x+'px;top:'+y+'px;"></div>';
	}
	l('shipments').innerHTML=str;
});
new Buyable('Alchemy lab','Turns gold into cookies!','labicon',50000,function(buy)
{
	if (buy) Labs++;
	if (buy && Labs==1) Buyables['Grandma'].func();
	var str='';
	for (var i=0;i<Labs;i++)
	{
		var x=Math.floor(Math.random()*20+(i%10)*24);
		var y=Math.floor(Math.random()*20+Math.floor(i/10)*16);
		str+='<div class="lab" style="right:'+x+'px;top:'+y+'px;"></div>';
	}
	l('labs').innerHTML=str;
});
new Buyable('Portal','Opens a door to the Cookieverse.','portalicon',1000000,function(buy)
{
	if (buy) Portals++;
	if (buy && Portals==1) Buyables['Grandma'].func();
	var str='';
	for (var i=0;i<Portals;i++)
	{
		var x=Math.floor(Math.random()*20+(i%10)*24);
		var y=Math.floor(Math.random()*20+Math.floor(i/10)*24);
		str+='<div class="portal" style="right:'+x+'px;top:'+y+'px;"></div>';
	}
	l('portals').innerHTML=str;
});
new Buyable('Time machine','<span style="font-size:80%;">Brings cookies from the past, before they were even eaten.</span>','timemachineicon',123456789,function(buy)
{
	if (buy) Times++;
	if (buy && Times==1) Buyables['Grandma'].func();
	var str='';
	for (var i=0;i<Times;i++)
	{
		var x=Math.floor(Math.random()*20+(i%10)*24);
		var y=Math.floor(Math.random()*20+Math.floor(i/10)*24);
		str+='<div class="time" style="right:'+x+'px;top:'+y+'px;"></div>';
	}
	l('times').innerHTML=str;
});

new Buyable('Elder Pledge','<span style="font-size:80%;">Puts an end to the Ancients\' wrath, at least for a while.</span>','pledgeicon',666666,function(buy)
{
	if (buy) {Pledge*=2;Pledge+=30*60*10;}
	if (buy) Buyables['Grandma'].func();
	l('buyElder Pledge').style.display='none';
});


Pops=[];
Pop=function(el,str)
{
	this.el=el;
	this.str=str;
	this.life=0;
	this.offx=Math.floor(Math.random()*20-10);
	this.offy=Math.floor(Math.random()*20-10);
	Pops.push(this);
}


Main=function()
{
	var str='';
	if (StoreToRebuild)
	{
		RebuildStore();
		StoreToRebuild=0;
	}
	
	for (var i in Pops)
	{
		var rect=l(Pops[i].el).getBoundingClientRect();
		var x=Math.floor((rect.left+rect.right)/2+Pops[i].offx)-100;
		var y=Math.floor((rect.top+rect.bottom)/2-Math.pow(Pops[i].life/100,0.5)*100+Pops[i].offy)-10;
		var opacity=1-(Math.max(Pops[i].life,80)-80)/20;
		str+='<div class="pop" style="position:absolute;left:'+x+'px;top:'+y+'px;opacity:'+opacity+';">'+Pops[i].str+'</div>';
		Pops[i].life+=2;
		if (Pops[i].life>=100) Pops.splice(i,1);
	}
	l('pops').innerHTML=str;
	
	var str='';
	for (var i=0;i<Cursors;i++)
	{
		var rot=-Math.floor((360/Cursors)*i);
		var x=Math.floor(64+Math.sin((Math.PI*2/Cursors)*i)*64)-16;
		var y=Math.floor(64+Math.cos((Math.PI*2/Cursors)*i)*64)-16;
		if ((T)%150==Math.ceil((150/Cursors)*i)) y+=2;
		str+='<div class="cursor" style="left:'+x+'px;top:'+y+'px;transform:rotate('+rot+'deg);-webkit-transform:rotate('+rot+'deg);-moz-transform:rotate('+rot+'deg);-ms-transform:rotate('+rot+'deg);"></div>';
	}
	l('cookie').innerHTML=str;
	
	var grandmaGain=Math.ceil(4+(Factories?1:0)+(Mines?2:0)+(Shipments?3:0)+(Labs?4:0)+(Portals?(Pledge?5+Portals*0.5:5):0)+(Times?6:0));
	var cursorGain=(Pledge>0?Math.ceil(Cursors*1.5):1);
	
	if (Times && T%Math.ceil(150/Times)==0) AddCookie(123456,'times');
	if (Portals && T%Math.ceil(150/Portals)==0) AddCookie(6666,'portals');
	if (Labs && T%Math.ceil(150/Labs)==0) AddCookie(500,'labs');
	if (Shipments && T%Math.ceil(150/Shipments)==0) AddCookie(100,'shipments');
	if (Mines && T%Math.ceil(150/Mines)==0) AddCookie(50,'mines');
	if (Factories && T%Math.ceil(150/Factories)==0) AddCookie(20,'factories');
	if (Grandmas && T%Math.ceil(150/Grandmas)==0) AddCookie(grandmaGain,'grandmas');
	if (Cursors && T%Math.ceil(150/Cursors)==0) eventFire(l('cookie'),'mouseup');
	
	
	var cps=0;
	cps+=Times*123456/5;
	cps+=Portals*6666/5;
	cps+=Labs*500/5;
	cps+=Shipments*100/5;
	cps+=Mines*50/5;
	cps+=Factories*20/5;
	cps+=Grandmas*grandmaGain/5;
	cps+=Cursors*cursorGain/5;
	
	var floater=Math.round(cps*10-Math.floor(cps)*10);
	cps=Beautify(cps)+(floater?('.'+floater):'');
	l('cps').innerHTML='cookies/second : '+cps;
	
	
	for (var i in Buyables)
	{
		if (Cookies>=Buyables[i].price) l('buy'+Buyables[i].name).className=''; else l('buy'+Buyables[i].name).className='grayed';
	}
	
	CookiesDisplay+=(Cookies-CookiesDisplay)*0.5;
	l('money').innerHTML=Beautify(Math.round(CookiesDisplay));
	
	var str='';
	if (Cookies<5) str='You feel like making cookies.<br>But nobody wants to eat your cookies.';
	else if (Cookies<25) str='Your cookies are popular<br>with your dog.';
	else if (Cookies<50) str='Your cookies are popular<br>with your family.';
	else if (Cookies<100) str='Your cookies are popular<br>in the neighborhood.';
	else if (Cookies<500) str='Your cookies are renowned<br>in the whole town!';
	else if (Cookies<2000) str='Your cookies are worth<br>a lot of money.';
	else if (Cookies<5000) str='Your cookies bring<br>all the boys to the yard.';
	else if (Cookies<10000) str='People come from very far away<br>to get a taste of your cookies.';
	else if (Cookies<17000) str='Kings and queens from all over the world<br>are enjoying your cookies.';
	else if (Cookies<30000) str='Your cookies have been named<br>a part of the world wonders.';
	else if (Cookies<60000) str='Your cookies have been placed<br>under government surveillance.';
	else if (Cookies<100000) str='The whole planet is<br>enjoying your cookies!';
	else if (Cookies<150000) str='Creatures from neighboring planets<br>wish to try your cookies.';
	else if (Cookies<250000) str='Elder gods from the whole cosmos<br>have awoken to taste your cookies.';
	else if (Cookies<400000) str='Your cookies have achieved sentience.';
	else if (Cookies<1000000) str='The universe has now turned into<br>cookie dough, to the molecular level.';
	else if (Cookies<1000000000) str='A local news station runs<br>a 10-minute segment about your cookies. Success!<br><span style="font-size:50%;">(you win a cookie)</span>';
	else str='it\'s time to stop playing<br><span style="font-size:50%;">(more fun milestones in the next update I promise)</span>';
	l('comment').innerHTML=str;
	
	
	if (Pledge>0) Pledge--;
	
	if (Cookies>=1000000 && Pledge<=0 && Flashing)
	{
		var r=(Cookies-1000000)/2000000;
		var r2=Math.max(0,(Cookies-100000000)/400000000);
		var icon='grandmaicon';
		if (Cookies>=2000000)
		{
			l('buyElder Pledge').style.display='block';
			if (Math.random()<0.02) icon='grandmaiconinvert';
			else if (Math.random()<0.02) icon='grandmaiconlustful';
		}
		if (Cookies>=10000000 && Math.random()<0.02) icon='skellington';
		if (Cookies>=1000000000) l('whole').style.background='url(kaleigrandma.png) '+Math.floor(T*0.2)+'px -'+Math.floor(T*0.1)+'px';
		else if (Math.random()<r)
		{
			l('whole').style.background='url('+icon+'.png) '+Math.floor(Math.random()*4)+'px '+Math.floor(Math.random()*4)+'px';
			l('whole').style.backgroundSize=Math.floor(r2*Math.random()*64+64)+'px '+Math.floor(r2*Math.random()*64+64)+'px ';
		}
	}//sorry
	else l('whole').style.background='#ccc';
	
	if (T%30==0 && Loaded) document.title=Beautify(Cookies)+' cookies - Cookie Clicker';
	Clicking=0;
	Hovering=0;
	
	SaveTimer--;
	if (SaveTimer==0 && Loaded) Save();
	
	T++;
	setTimeout(Main,1000/30);
}


Load();

</script>