const fs = require('node:fs');
const assert = require('node:assert/strict');
const path = require('node:path');
const app=path.resolve(__dirname,'../app');
const tokens=fs.readFileSync(path.join(app,'tokens.css'),'utf8');
const styles=fs.readFileSync(path.join(app,'app.css'),'utf8');
const vars=s=>Object.fromEntries([...s.matchAll(/--([\w-]+):\s*([^;]+);/g)].map(m=>[m[1],m[2].trim()]));
const light=vars(tokens.slice(0,tokens.indexOf(':root[data-theme')));
const darkRaw=vars(tokens.slice(tokens.indexOf(':root[data-theme')));
const dark={...light,...darkRaw};
assert(!/#[0-9a-f]{3,8}\b|rgba?\(|hsla?\(/i.test(styles),'Literal colour outside tokens');
assert(!/\d+(px|rem|ms)\b/.test(styles),'Literal dimension or duration outside tokens');
for(const k of Object.keys(light).filter(k=>light[k].startsWith('#'))) assert(k in darkRaw,`Missing dark ${k}`);
const used=[...styles.matchAll(/var\(--([\w-]+)/g)].map(m=>m[1]);
for(const k of used)assert(k in light,`Undefined token ${k}`);
const lum=h=>[1,3,5].map(i=>parseInt(h.slice(i,i+2),16)/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4).reduce((a,v,i)=>a+v*[.2126,.7152,.0722][i],0);
const ratio=(a,b)=>{const x=[lum(a),lum(b)].sort((a,b)=>b-a);return (x[0]+.05)/(x[1]+.05)};
const results=[];
for(const [name,t] of [['light',light],['dark',dark]]){
 for(const fg of ['fg','muted'])for(const bg of ['bg','surface','field','tint','avatar-bg']){
  const r=ratio(t[fg],t[bg]); assert(r>=4.5,`${name} ${fg}/${bg}: ${r}`);results.push({theme:name,pair:`${fg}/${bg}`,ratio:+r.toFixed(2)});
 }
 for(const [fg,bg] of [['on-accent','accent'],['on-accent','accent-hover'],['caution','caution-bg'],['status','tint'],['focus','bg']]){
 const r=ratio(t[fg],t[bg]);assert(r>=4.5,`${name} ${fg}/${bg}: ${r}`);results.push({theme:name,pair:`${fg}/${bg}`,ratio:+r.toFixed(2)});
 }
}
for(const [name,t] of [['light',light],['dark',dark]])for(const bg of ['bg','field']){const r=ratio(t['control-edge'],t[bg]);assert(r>=3,`${name} control boundary/${bg}: ${r}`);results.push({theme:name,pair:`control-edge/${bg}`,ratio:+r.toFixed(2)});}
const html=fs.readFileSync(path.join(app,'index.html'),'utf8');assert(html.indexOf('tokens.css')<html.indexOf('app.css'),'Token load order');
assert.equal(fs.readFileSync(path.resolve(__dirname,'../../fixtures.js'),'utf8'),fs.readFileSync(path.join(app,'fixtures.js'),'utf8'),'Fixture was modified');
fs.writeFileSync(path.join(__dirname,'contrast.json'),JSON.stringify(results,null,2));
console.log(`PASS: tokens, theme parity, wiring, frozen fixture copy; ${results.length} contrast pairs (min ${Math.min(...results.map(x=>x.ratio))}:1)`);
