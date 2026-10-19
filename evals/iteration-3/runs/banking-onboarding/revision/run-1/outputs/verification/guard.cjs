const fs=require('fs'),assert=require('assert/strict'),path=require('path');
const app=path.resolve(__dirname,'../app');
const tokens=fs.readFileSync(path.join(app,'tokens.css'),'utf8');
const css=fs.readFileSync(path.join(app,'app.css'),'utf8');
const html=fs.readFileSync(path.join(app,'index.html'),'utf8');
const vars=s=>Object.fromEntries([...s.matchAll(/--([\w-]+):\s*([^;]+);/g)].map(m=>[m[1],m[2].trim()]));
const split=tokens.indexOf(':root[data-theme');
const light=vars(tokens.slice(0,split)),dark=vars(tokens.slice(split));
assert.equal((css.match(/#[0-9a-f]{3,8}\b|rgba?\(|hsla?\(/gi)||[]).length,0,'Literal color in component styles');
for(const property of ['font-size','border-radius','box-shadow']) {
 for(const match of css.matchAll(new RegExp(property+':([^;}]+)','g')))assert.ok(match[1].trim().startsWith('var('),`Untokenized ${property}`);
}
for(const token of Object.keys(light).filter(k=>/^#/.test(light[k])))assert.ok(token in dark,`Missing dark ${token}`);
for(const m of css.matchAll(/var\(--([\w-]+)\)/g))assert.ok(m[1] in light,`Missing token ${m[1]}`);
assert.ok(html.indexOf('tokens.css')<html.indexOf('app.css'),'Token stylesheet order');
function lum(hex){const c=[1,3,5].map(i=>parseInt(hex.slice(i,i+2),16)/255).map(x=>x<=.04045?x/12.92:((x+.055)/1.055)**2.4);return c[0]*.2126+c[1]*.7152+c[2]*.0722;}
function ratio(a,b){const x=[lum(a),lum(b)].sort((a,b)=>b-a);return (x[0]+.05)/(x[1]+.05);}
const pairs=[['fg','bg'],['fg','surface'],['fg','warning'],['muted','bg'],['muted','surface'],['error','bg'],['error','error-bg'],['success','success-bg'],['on-primary','primary']];
let rows=[];
for(const [name,t] of [['light',light],['dark',{...light,...dark}]]) {
 for(const [fg,bg] of pairs){const r=ratio(t[fg],t[bg]);assert.ok(r>=4.5,`${name}: ${fg}/${bg} ${r}`);rows.push({theme:name,foreground:fg,background:bg,ratio:+r.toFixed(2)});}
 for(const [fg,bg] of [['input-border','surface'],['focus','bg'],['focus','surface']]) {const r=ratio(t[fg],t[bg]);assert.ok(r>=3,`${fg}/${bg} <3`);rows.push({theme:name,foreground:fg,background:bg,ratio:+r.toFixed(2)});}
}
fs.writeFileSync(path.join(__dirname,'contrast.json'),JSON.stringify(rows,null,2));
console.log('PASS: token references, no literal component colors/font sizes/radii/shadows, theme parity, stylesheet order, 24 contrast checks.');
