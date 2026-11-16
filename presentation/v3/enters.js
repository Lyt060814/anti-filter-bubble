/* ---------- per-slide initialisers (v3) ---------- */
const enter={},leave={};
enter[1]=()=>{sil.on=true;sil.t0=performance.now();if(STATIC)drawSil(0);else requestAnimationFrame(silLoop)};
leave[1]=()=>{sil.on=false};

/* 2: two feeds with the same topic share; group labels appear inside the topic */
enter[2]=()=>{
  const topic=[...Array(100).keys()].filter(i=>(i*37+11)%100<30);
  const pick=[topic[4],topic[17],topic[9],topic[25]];
  [['g2a',2,0],['g2b',4,.15]].forEach(([id,nr,dd])=>{
    const g=$('#'+id);g.innerHTML='';
    for(let i=0;i<100;i++){const s=document.createElement('div');s.className='zsq';s.style.width=s.style.height='34px';
      s.style.left=(i%10)*40+'px';s.style.top=Math.floor(i/10)*40+'px';g.appendChild(s);
      if(topic.includes(i))later(.6+dd+(i%10)*.04,()=>s.classList.add('t'));
      const k=pick.indexOf(i);if(k>=0&&k<nr)later(3+dd+k*.3,()=>s.classList.add('r'))}
  });
};

/* 4: interest (x) against skew (y) */
enter[4]=()=>{
  const s=$('#c4');s.innerHTML='';const L=120,R=1080,T=40,B=600;
  el('line',{x1:L,x2:R+30,y1:B,y2:B,stroke:BONE,'stroke-width':2.5},s);el('line',{x1:L,x2:L,y1:B,y2:T-10,stroke:BONE,'stroke-width':2.5},s);
  el('path',{d:`M${R+14} ${B-10} L${R+34} ${B} L${R+14} ${B+10}`,stroke:BONE,'stroke-width':2.5,fill:'none'},s);
  el('path',{d:`M${L-10} ${T+4} L${L} ${T-16} L${L+10} ${T+4}`,stroke:BONE,'stroke-width':2.5,fill:'none'},s);
  el('text',{x:R+30,y:B+44,fill:BONE,'font-size':30,'text-anchor':'end','font-style':'italic'},s,'Interest →');
  el('text',{x:L-24,y:T+30,fill:BONE,'font-size':30,'text-anchor':'end','font-style':'italic',transform:`rotate(-90 ${L-24} ${T+30})`},s,'');
  el('text',{x:L+18,y:T+4,fill:BONE,'font-size':30,'font-style':'italic'},s,'Skew');
  const pts=[[300,500,ASH,'Casual viewer',.6],[880,500,BONE,'Topic fan, all sides',1],[300,170,ASH,'Little of the topic, one side',1.4],[880,170,ROSE,'Viewpoint cocoon',1.8]];
  pts.forEach(([x,y,c,lab,d])=>{
    el('circle',{cx:x,cy:y,r:16,fill:c,class:'pop',style:`--d:${d}s;transform-origin:${x}px ${y}px`},s);
    el('text',{x:x,y:y-34,fill:c,'font-size':32,'text-anchor':'middle','font-style':'italic',class:'fade',style:`--d:${d+.2}s`},s,lab);
  });
  el('text',{x:880,y:548,fill:BONE,'font-size':26,'text-anchor':'middle','font-family':'PM',class:'fade',style:'--d:2.6s'},s,'FEED A');
  el('text',{x:880,y:218,fill:ROSE,'font-size':26,'text-anchor':'middle','font-family':'PM',class:'fade',style:'--d:2.6s'},s,'FEED B');
  el('path',{d:'M880 430 V236',stroke:ROSE,'stroke-width':3,'stroke-dasharray':'8 8',class:'draw',pathLength:1,style:'--d:2.8s'},s);
  el('text',{x:900,y:350,fill:ROSE,'font-size':28,'font-style':'italic',class:'fade',style:'--d:3.2s'},s,'same interest,');
  el('text',{x:900,y:386,fill:ROSE,'font-size':28,'font-style':'italic',class:'fade',style:'--d:3.2s'},s,'twice the odds');
  el('rect',{x:L,y:B+70,width:R-L,height:16,fill:'rgba(184,154,104,.35)',class:'wipe',style:'--d:3.6s'},s);
  el('text',{x:L,y:B+124,fill:SEP,'font-size':30,'font-style':'italic',class:'fade',style:'--d:3.9s'},s,'A cocoon check reads only this axis');
};

/* 5: concentric layers */
enter[5]=()=>{
  const svg=$('#s5s');svg.innerHTML='';const cx=470,cy=640,PA='#b0213f',IN='#0a0a0b';
  const defs=el('defs',{},svg);const pat=el('pattern',{id:'hat5',width:14,height:14,patternUnits:'userSpaceOnUse',patternTransform:'rotate(45)'},defs);el('line',{x1:0,y1:0,x2:0,y2:14,stroke:'rgba(10,10,11,.22)','stroke-width':3},pat);
  el('circle',{cx,cy,r:310,fill:'url(#hat5)',stroke:IN,'stroke-width':3,'stroke-dasharray':'14 10',class:'rise',style:'--d:1.8s;transform-origin:'+cx+'px '+cy+'px'},svg);
  el('circle',{cx,cy,r:180,fill:'rgba(226,58,90,.2)',stroke:PA,'stroke-width':5,class:'pop',style:'--d:2.8s;transform-origin:'+cx+'px '+cy+'px'},svg);
  el('circle',{cx,cy,r:62,fill:IN,class:'pop',style:'--d:3.2s;transform-origin:'+cx+'px '+cy+'px'},svg);
  el('text',{x:cx,y:cy+9,fill:'#e8e0cc','text-anchor':'middle','font-size':24,'font-family':'PM',class:'fade',style:'--d:3.4s'},svg,'YOU');
  el('text',{x:cx,y:cy-238,fill:'#3b362c','text-anchor':'middle','font-size':24,'font-family':'PM','letter-spacing':4,class:'fade',style:'--d:2.2s'},svg,'PLATFORM');
  el('text',{x:cx,y:cy-110,fill:PA,'text-anchor':'middle','font-size':24,'font-family':'PM','letter-spacing':4,class:'fade',style:'--d:3s'},svg,'PERSONAL');
  [150,210,330,30].forEach((deg,i)=>{
    const a=deg*Math.PI/180,c=Math.cos(a),sn=Math.sin(a),d=3.8+i*.25,p=r=>[cx+c*r,cy+sn*r];
    const [x1,y1]=p(66),[x2,y2]=p(172);
    el('path',{d:'M'+x1+' '+y1+' L'+x2+' '+y2,stroke:PA,'stroke-width':6,'stroke-linecap':'round',class:'draw',pathLength:1,style:'--d:'+d+'s'},svg);
    const nx=-sn*18,ny=c*18;
    el('path',{d:'M'+(x2+nx)+' '+(y2+ny)+' L'+(x2-nx)+' '+(y2-ny),stroke:PA,'stroke-width':6,'stroke-linecap':'round',class:'fade',style:'--d:'+(d+1)+'s'},svg);
  });
};

/* 6: four kinds of evidence */
enter[6]=()=>{
  const w=$('#w6');
  const cards=[['READ THE LOGS','What each user was actually shown','RQ1 · RQ2'],['PROBE THE MODEL','OneRec-1.7B, trained on these logs: edit a history, see what it recommends','RQ2'],['SIMULATE','Run that response forward for months; try every way out','RQ2 · RQ4'],['COUNT','How many videos a user needs to tell a tilt from chance','RQ3']];
  w.innerHTML=cards.map(([h,t,rq],i)=>`<div class="card rise" style="--d:${1.8+i*.35}s;left:${i*420}px;top:0;width:390px;height:380px"></div>
    <div class="abs rise" style="--d:${1.9+i*.35}s;left:${i*420+30}px;top:30px;width:330px">
      <div class="mono rose" style="font-size:20px;letter-spacing:4px">${String(i+1).padStart(2,'0')} · ${h}</div>
      <div style="font:600 34px/1.22 var(--serif);margin-top:14px;height:210px">${t}</div>
      <div class="mono sep" style="font-size:24px;letter-spacing:3px">${rq}</div></div>`).join('');
};

/* 8: prevalence, engagement, supply vs shown */
enter[8]=()=>{
  const c=$('#c8a');
  c.innerHTML='<div class="big rose" style="font-size:118px;opacity:0" data-b>1 in 5</div><div class="dotg" style="position:relative;width:240px;height:240px;margin:22px 0 26px"></div><div class="lab" style="font-size:32px;line-height:1.2;width:480px;opacity:0" data-t>issue videos shown carry an opposing narrative<br><span class="ash mono" style="font-size:20px">18.4% · issues are 7.9% of all that is shown</span></div>';
  const b=c.querySelector('[data-b]'),t=c.querySelector('[data-t]'),g=c.querySelector('.dotg');
  tw(.9,.4,u=>{b.style.opacity=u;b.style.transform='translateY('+(30*(1-u))+'px)'});tw(.8,1.6,u=>t.style.opacity=u);
  for(let i=0;i<100;i++){const s=document.createElement('span');s.style.left=(i%10)*24+'px';s.style.top=Math.floor(i/10)*24+'px';g.appendChild(s);
    if(i<18){if(STATIC)s.classList.add('r');else later(1+i*.06,()=>s.classList.add('r'))}}
  const s=$('#c8b');s.innerHTML='';
  el('text',{x:0,y:24,fill:ASH,'font-size':19,'font-family':'PM','letter-spacing':3},s,'ODDS AGAINST OTHER ISSUE VIDEOS');
  const base=150,sc=170;
  const rows=[['commented on',1.85,ROSE],['shared',1.33,BONE],['marked "not interested"',1.74,SEP]];
  el('line',{x1:base,x2:base,y1:50,y2:50+rows.length*100,stroke:ASH,'stroke-width':2,'stroke-dasharray':'4 6'},s);
  el('text',{x:base,y:50+rows.length*100+26,fill:ASH,'font-size':20,'text-anchor':'middle','font-family':'CG','font-style':'italic'},s,'1× = same as others');
  rows.forEach(([lab,v,col],i)=>{const y=60+i*100;
    el('text',{x:0,y:y+20,fill:BONE,'font-size':26,'font-style':'italic','font-family':'CG'},s,lab);
    const r=el('rect',{x:0,y:y+34,width:0,height:34,fill:col},s);const t=el('text',{x:0,y:y+62,fill:col,'font-size':30},s,'');
    tw(1.1,1.6+i*.35,u=>{const w=(1+(v-1)*u)*sc*u;r.setAttribute('width',w);t.setAttribute('x',w+12);t.textContent='×'+(1+(v-1)*u).toFixed(2)})});
  const q=$('#c8c');q.innerHTML='';
  el('text',{x:0,y:24,fill:ASH,'font-size':19,'font-family':'PM','letter-spacing':3},q,'GENDER GROUP LABELS');
  const bb=360,sy=34;
  [['on offer',4.1,BONE,90],['shown',6.2,ROSE,300]].forEach(([lab,v,col,x],i)=>{
    const r=el('rect',{x,y:bb,width:120,height:0,fill:col},q);const t=el('text',{x:x+60,y:bb-12,fill:col,'font-size':40,'text-anchor':'middle'},q,'');
    tw(1.2,2.6+i*.5,u=>{const h=v*sy*u;r.setAttribute('y',bb-h);r.setAttribute('height',h);t.setAttribute('y',bb-h-14);t.textContent=(v*u).toFixed(1)+'%'});
    el('text',{x:x+60,y:bb+40,fill:BONE,'font-size':28,'text-anchor':'middle','font-style':'italic'},q,lab)});
  el('line',{x1:40,x2:500,y1:bb,y2:bb,stroke:ASH,'stroke-width':2},q);
};

/* 9: the probe */
enter[9]=()=>{
  const s=$('#c9a');s.innerHTML='';
  el('text',{x:10,y:30,fill:ASH,'font-size':19,'font-family':'PM','letter-spacing':3},s,"A REAL USER'S HISTORY");
  const swap=[2,5,7,10,13,15,18,21,24,27];
  for(let i=0;i<30;i++){const x=10+(i%10)*56,y=56+Math.floor(i/10)*56;
    const r=el('rect',{x,y,width:46,height:46,rx:3,fill:'rgba(236,229,211,.22)'},s);
    if(swap.includes(i))later(1+swap.indexOf(i)*.12,()=>r.setAttribute('fill',ROSE))}
  el('text',{x:10,y:260,fill:ROSE,'font-size':28,'font-style':'italic','font-family':'CG',class:'fade',style:'--d:1.6s'},s,'swap in 10 group-label videos');
  el('path',{d:'M290 290 V350 M272 330 L290 352 L308 330',stroke:ASH,'stroke-width':3,fill:'none',class:'draw',pathLength:1,style:'--d:2s'},s);
  el('rect',{x:120,y:370,width:340,height:84,fill:'none',stroke:BONE,'stroke-width':2.5,class:'fade',style:'--d:2.2s'},s);
  el('text',{x:290,y:424,fill:BONE,'font-size':36,'text-anchor':'middle','font-style':'italic','font-family':'CG',class:'fade',style:'--d:2.2s'},s,'OneRec-1.7B');
  el('path',{d:'M460 412 H560 M540 394 L562 412 L540 430',stroke:ASH,'stroke-width':3,fill:'none',class:'draw',pathLength:1,style:'--d:2.5s'},s);
  el('text',{x:580,y:402,fill:BONE,'font-size':28,'font-style':'italic','font-family':'CG',class:'fade',style:'--d:2.7s'},s,'what it would');
  el('text',{x:580,y:436,fill:BONE,'font-size':28,'font-style':'italic','font-family':'CG',class:'fade',style:'--d:2.7s'},s,'recommend next');
  el('text',{x:10,y:520,fill:ASH,'font-size':20,'font-family':'PM',class:'fade',style:'--d:3s'},s,'200 held-out users · exact scores for 2,000 videos');
  const b=$('#c9b');b.innerHTML='';const x0=380,sc=320;
  el('rect',{x:x0-.12*sc,y:6,width:.24*sc,height:300,fill:'rgba(141,136,125,.16)',stroke:ASH,'stroke-dasharray':'6 6','stroke-width':1.5,class:'fade',style:'--d:2.8s'},b);
  el('text',{x:x0,y:336,fill:ASH,'font-size':21,'text-anchor':'middle','font-style':'italic','font-family':'CG',class:'fade',style:'--d:2.9s'},b,'range of chance');
  el('line',{x1:x0,x2:x0,y1:6,y2:306,stroke:ASH,'stroke-width':2},b);
  const rows=[['Topic','after 10 issue videos',1.01,BONE],['Narrative','after 10 group-label videos',.67,ROSE],['Random split','of other issue videos',.01,ASH]];
  rows.forEach(([w,lab,v,col],i)=>{const y=22+i*100;
    el('text',{x:0,y:y+24,fill:BONE,'font-size':32,'font-style':'italic','font-family':'CG'},b,w);
    el('text',{x:0,y:y+56,fill:ASH,'font-size':22,'font-family':'CG'},b,lab);
    const r=el('rect',{x:x0,y:y+6,width:0,height:44,fill:col},b);const t=el('text',{x:x0+12,y:y+40,fill:col,'font-size':40},b,'');
    tw(1.1,1+i*.45,u=>{const w_=Math.max(2,v*sc*u);r.setAttribute('width',w_);t.setAttribute('x',x0+w_+14);t.textContent=i==2?'≈ 0':'+'+(v*u).toFixed(2)})});
};

/* 10: formation over 90 days */
enter[10]=()=>{
  const b=$('#c10');b.innerHTML='';const L=90,R=1220,T=30,B=520;
  const X=d=>L+(R-L)*d/90,YV=v=>B-(B-T)*v/.9,YM=m=>B-(B-T)*m/.6;
  el('line',{x1:L,x2:R,y1:B,y2:B,stroke:ASH,'stroke-width':2},b);el('line',{x1:L,x2:L,y1:T,y2:B,stroke:ROSE,'stroke-width':2},b);el('line',{x1:R,x2:R,y1:T,y2:B,stroke:BONE,'stroke-width':1.5,'stroke-dasharray':'4 6'},b);
  [[0,'×1'],[.4,'×1.5'],[.78,'×2.2']].forEach(([v,l])=>el('text',{x:L-14,y:YV(v)+8,fill:ROSE,'font-size':26,'text-anchor':'end'},b,l));
  el('text',{x:L-14,y:T-6,fill:ROSE,'font-size':20,'text-anchor':'end','font-family':'PM'},b,'ODDS');
  [0,.3,.6].forEach(m=>el('text',{x:R+12,y:YM(m)+8,fill:BONE,'font-size':26},b,Math.round(m*100)+'%'));
  el('text',{x:R+12,y:T-6,fill:BONE,'font-size':20,'font-family':'PM'},b,'TOPIC');
  [0,30,60,90].forEach(d=>el('text',{x:X(d),y:B+40,fill:ASH,'font-size':26,'text-anchor':'middle'},b,'day '+d));
  const path=(s,key,Y)=>'M'+s.d.map((d,j)=>X(d).toFixed(1)+' '+Y(s[key][j]).toFixed(1)).join(' L');
  el('path',{d:path(FORM.fan,'m',YM),stroke:BONE,'stroke-width':3,'stroke-dasharray':'12 9',fill:'none',class:'fade',style:'--d:1.2s'},b);
  el('path',{d:path(FORM.casual,'V',YV),stroke:ASH,'stroke-width':3,fill:'none',pathLength:1,class:'draw',style:'--d:1.6s'},b);
  el('path',{d:path(FORM.fan,'V',YV),stroke:ROSE,'stroke-width':7,fill:'none',pathLength:1,class:'draw',style:'--d:2s','stroke-linejoin':'round'},b);
  el('text',{x:R-12,y:YM(.30)+44,fill:BONE,'font-size':30,'text-anchor':'end','font-style':'italic','font-family':'CG',class:'fade',style:'--d:1.6s'},b,'topic share: flat at 30%');
  el('text',{x:R-12,y:YV(.79)-18,fill:ROSE,'font-size':32,'text-anchor':'end','font-style':'italic','font-family':'CG',class:'fade',style:'--d:3.6s'},b,'topic fan: twice the odds by day 89');
  el('text',{x:R-12,y:YV(.09)-16,fill:ASH,'font-size':26,'text-anchor':'end','font-style':'italic','font-family':'CG',class:'fade',style:'--d:3.8s'},b,'casual viewer, same taste: barely moves');
  el('circle',{cx:X(24),cy:YV(.39),r:11,fill:ROSE,class:'pop',style:'--d:3.3s;transform-origin:'+X(24)+'px '+YV(.39)+'px'},b);
  el('text',{x:X(24)-18,y:YV(.39)-16,fill:BONE,'font-size':28,'text-anchor':'end','font-style':'italic','font-family':'CG',class:'fade',style:'--d:3.4s'},b,'half-way by day 24');
};

/* 11: days to collect each sample */
enter[11]=()=>{
  countups($('#s11'));
  const s=$('#c11');s.innerHTML='';const L=0,R=860,X=d=>L+(R-L)*d/120;
  const bars=[['your own feed',9,ROSE,'9 days'],['a feed without personalisation',114,SEP,'114 days ≈ 4 months'],['a reference the platform publishes',6,BONE,'6 days · 310 videos']];
  bars.forEach(([lab,d,col,val],i)=>{const y=10+i*130;
    el('text',{x:0,y:y+30,fill:BONE,'font-size':32,'font-style':'italic','font-family':'CG',class:'fade',style:'--d:'+(1.6+i*.6)+'s'},s,lab);
    const r=el('rect',{x:L,y:y+48,width:0,height:36,fill:col},s);const t=el('text',{x:L+12,y:y+76,fill:col,'font-size':30,'font-family':'PM'},s,'');
    tw(1.3,1.8+i*.6,u=>{const w=X(d)*u;r.setAttribute('width',Math.max(2,w));if(d>60){t.setAttribute('x',16);t.setAttribute('fill',INK)}else t.setAttribute('x',w+14);t.textContent=val})});
  [[7,'1 week'],[30,'1 month'],[120,'4 months']].forEach(([d,l])=>{el('line',{x1:X(d),x2:X(d),y1:410,y2:422,stroke:ASH,'stroke-width':2},s);el('text',{x:X(d),y:452,fill:ASH,'font-size':22,'text-anchor':d===120?'end':'middle','font-family':'CG'},s,l)});
  el('line',{x1:L,x2:R,y1:410,y2:410,stroke:ASH,'stroke-width':1.5},s);
};

/* 12: skew removed against topic kept */
enter[12]=()=>{
  const s=$('#c12');s.innerHTML='';const L=130,R=1040,T=30,B=580;
  const X=k=>L+(R-L)*k,Y=r=>B-(B-T)*(r+.2)/3.0;
  el('line',{x1:L,x2:R,y1:Y(0),y2:Y(0),stroke:ASH,'stroke-width':2},s);el('line',{x1:L,x2:L,y1:T,y2:B,stroke:ASH,'stroke-width':2},s);
  [0,1,2].forEach(r=>el('text',{x:L-14,y:Y(r)+9,fill:ASH,'font-size':26,'text-anchor':'end'},s,r.toFixed(1)));
  [0,.5,1].forEach(k=>el('text',{x:X(k),y:B+38,fill:ASH,'font-size':26,'text-anchor':'middle'},s,Math.round(k*100)+'%'));
  el('text',{x:(L+R)/2,y:B+84,fill:BONE,'font-size':30,'text-anchor':'middle','font-style':'italic','font-family':'CG'},s,'share of the topic kept →');
  el('text',{x:L+12,y:T+6,fill:BONE,'font-size':30,'font-style':'italic','font-family':'CG'},s,'↑ skew removed');
  el('line',{x1:L,x2:R,y1:Y(.78),y2:Y(.78),stroke:SEP,'stroke-width':2,'stroke-dasharray':'8 8',class:'fade',style:'--d:1s'},s);
  el('text',{x:X(.5),y:Y(.78)-12,fill:SEP,'font-size':24,'font-style':'italic','font-family':'CG',class:'fade',style:'--d:1.1s'},s,'personal layer gone');
  const lab={S8:['personalisation off',ASH,24,-24,'start'],S9:['"show less of this topic"',ASH,24,30,'start'],S1:['scroll past',BONE,-26,10,'end'],S2:['"not interested"',ROSE,-26,10,'end'],S11:['classifier filter',ROSE,-26,10,'end']};
  Object.entries(ESC).forEach(([k,e],i)=>{if(k==='S0')return;const x=X(Math.min(e.kept,1)),y=Y(-e.dV),hl=k in lab;
    const c=el('circle',{cx:x,cy:y,r:hl?14:9,fill:hl?lab[k][1]:'rgba(236,229,211,.25)',class:'pop',style:`--d:${(hl?1.4:.8)+i*.06}s;transform-origin:${x}px ${y}px`},s);
    if(hl){const [t,col,dx,dy,an]=lab[k];el('text',{x:x+dx,y:y+dy,fill:col,'font-size':30,'text-anchor':an,'font-style':'italic','font-family':'CG',class:'fade',style:`--d:${1.8+i*.06}s`},s,t)}});
  el('text',{x:R,y:B+84,fill:ASH,'font-size':22,'text-anchor':'end','font-style':'italic','font-family':'CG'},s,'grey: six other strategies');
  const a=ESC.S1,b2=ESC.S2;
  el('path',{d:`M${X(b2.kept)+4} ${Y(-b2.dV)-16} Q ${X(b2.kept)+46} ${(Y(-b2.dV)+Y(-a.dV))/2} ${X(a.kept)+16} ${Y(-a.dV)+8}`,stroke:ROSE,'stroke-width':2.5,fill:'none','stroke-dasharray':'5 6',class:'fade',style:'--d:3.6s'},s);
};

/* 13: during the action and after it stops */
enter[13]=()=>{
  const s=$('#c13');s.innerHTML='';const L=110,R=1120,T=20,B=540,D0=-6,D1=38;
  const X=d=>L+(R-L)*(d-D0)/(D1-D0),Y=v=>B-(B-T)*(v+2)/3;
  el('rect',{x:X(0),y:T,width:X(16.7)-X(0),height:B-T,fill:'rgba(236,229,211,.06)'},s);
  el('text',{x:R,y:B+76,fill:ASH,'font-size':22,'text-anchor':'end','font-style':'italic','font-family':'CG'},s,'mean of 400 simulated topic fans');
  el('text',{x:(X(0)+X(16.7))/2,y:Y(-1.05),fill:ASH,'font-size':24,'text-anchor':'middle','font-family':'PM','letter-spacing':3},s,'ACTING · 17 DAYS');
  el('text',{x:(X(16.7)+R)/2,y:Y(-1.05),fill:ASH,'font-size':24,'text-anchor':'middle','font-family':'PM','letter-spacing':3},s,'STOPPED');
  el('line',{x1:L,x2:R,y1:Y(0),y2:Y(0),stroke:ASH,'stroke-width':1.5,'stroke-dasharray':'4 6'},s);
  el('line',{x1:L,x2:R,y1:B,y2:B,stroke:ASH,'stroke-width':2},s);el('line',{x1:L,x2:L,y1:T,y2:B,stroke:ASH,'stroke-width':2},s);
  [-2,-1,0,1].forEach(v=>el('text',{x:L-14,y:Y(v)+9,fill:ASH,'font-size':24,'text-anchor':'end'},s,(v>0?'+':'')+v.toFixed(1)));
  el('text',{x:L,y:T-24,fill:ASH,'font-size':20,'text-anchor':'middle','font-family':'PM'},s,'SKEW');
  [0,10,20,30].forEach(d=>el('text',{x:X(d),y:B+36,fill:ASH,'font-size':24,'text-anchor':'middle'},s,'day '+d));
  const path=k=>{const t=TRAJ[k];return 'M'+t.d.map((d,j)=>[d,t.V[j]]).filter(([d])=>d>=D0&&d<=D1).map(([d,v])=>X(d).toFixed(1)+' '+Y(v).toFixed(1)).join(' L')};
  const lines=[['S0',ASH,3,'carry on',null],['S1',BONE,4,'scroll past',null],['S2',SEP,4,'"not interested"','10 7'],['S11',ROSE,6,'classifier filter',null]];
  lines.forEach(([k,c,w,lab,dash],i)=>{
    const p=el('path',{d:path(k),stroke:c,'stroke-width':w,fill:'none',pathLength:1,class:'draw',style:`--d:${.8+i*.5}s`,'stroke-linejoin':'round'},s);
    if(dash){p.setAttribute('class','fade');p.setAttribute('stroke-dasharray',dash)}
    const lx=k==='S0'?28:8,t=TRAJ[k],j=t.d.findIndex(d=>d>=lx);
    el('text',{x:X(lx),y:Y(t.V[j])+(k==='S0'?-16:k==='S2'?-16:40),fill:c,'font-size':28,'font-style':'italic','font-family':'CG',class:'fade',style:`--d:${1.4+i*.5}s`},s,lab)});
};

enter[14]=()=>{};
