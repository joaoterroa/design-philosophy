const fs=require('node:fs');const assert=require('node:assert/strict');
const root=require('node:path').join(__dirname,'../app');
const css=fs.readFileSync(root+'/app.css','utf8'),tokens=fs.readFileSync(root+'/tokens.css','utf8'),html=fs.readFileSync(root+'/index.html','utf8'),js=fs.readFileSync(root+'/app.js','utf8');
assert(!/#[\da-f]{3,8}\b|rgba?\(|hsla?\(/i.test(css),'Literal component colour');
assert(!/#[\da-f]{6}\b/.test(js),'Literal JS colour');
for(const prop of ['font-size','border-radius','box-shadow','transition-duration','animation-duration']){
 for(const match of css.matchAll(new RegExp('(?<![\\w-])'+prop+':([^;}]+)','g'))){assert(/var\(/.test(match[1])||/^(none|inherit|0)$/.test(match[1].trim()),`Untokened ${prop}: ${match[1]}`)}
}
assert(html.indexOf('tokens.css')<html.indexOf('app.css'),'Token loading order');
const vars=block=>Object.fromEntries([...block.matchAll(/--([\w-]+):\s*([^;]+);/g)].map(m=>[m[1],m[2].trim()]));
const light=vars(tokens.split(':root[data-theme')[0]),dark=vars(tokens.split(':root[data-theme')[1]);
for(const [k,v] of Object.entries(light))if(/^#/.test(v))assert(k in dark,`Missing dark token ${k}`);
const lum=h=>{const rgb=[1,3,5].map(i=>parseInt(h.slice(i,i+2),16)/255).map(c=>c<=.04045?c/12.92:((c+.055)/1.055)**2.4);return .2126*rgb[0]+.7152*rgb[1]+.0722*rgb[2]};
const ratio=(a,b)=>{let x=lum(a),y=lum(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)};
let report=[];
for(const [name,t] of [['light',light],['dark',{...light,...dark}]]){
 for(const fg of ['fg','muted','action'])for(const bg of ['bg','surface','soft']){let r=ratio(t[fg],t[bg]);assert(r>=4.5,`${name} ${fg}/${bg} ${r.toFixed(2)}`);report.push(`${name} ${fg}/${bg}: ${r.toFixed(2)}`)}
 for(const [fg,bg] of [['danger','danger-bg'],['warn','warn-bg'],['success','success-bg'],['on-brand','brand'],['on-action','action']]){let r=ratio(t[fg],t[bg]);assert(r>=4.5,`${name} ${fg}/${bg} ${r.toFixed(2)}`);report.push(`${name} ${fg}/${bg}: ${r.toFixed(2)}`)}
 assert(ratio(t.chart,t.bg)>=3,`${name} chart contrast`);
}
assert.equal(fs.readFileSync(root+'/fixtures.js','utf8'),fs.readFileSync(root+'/../../fixtures.js','utf8'),'Fixture copy differs');
fs.writeFileSync(__dirname+'/contrast.txt',report.join('\n')+'\n');console.log('PASS: token use, theme parity, colour contrast, token loading and unchanged fixture copy.');
