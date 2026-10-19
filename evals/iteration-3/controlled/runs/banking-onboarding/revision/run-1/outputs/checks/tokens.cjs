const fs=require('node:fs');
const assert=require('node:assert/strict');
const path=require('node:path');
const root=path.resolve(__dirname,'../app');
const tokens=fs.readFileSync(path.join(root,'tokens.css'),'utf8');
const css=fs.readFileSync(path.join(root,'app.css'),'utf8');
const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
const vars=s=>Object.fromEntries([...s.matchAll(/--([\w-]+):\s*([^;]+);/g)].map(m=>[m[1],m[2].trim()]));
const cut=tokens.indexOf(':root[data-theme');
const light=vars(tokens.slice(0,cut)),darkValues=vars(tokens.slice(cut)),dark={...light,...darkValues};
assert(!/#[0-9a-f]{3,8}\b|rgba?\(|hsla?\(/i.test(css),'Literal colour outside tokens');
for(const property of ['font-size','border-radius','box-shadow','transition-duration']){
 const values=[...css.matchAll(new RegExp(property+':([^;}]+)','g'))].map(m=>m[1].trim());
 assert(values.every(v=>v.startsWith('var(')),`Untokenized ${property}: ${values}`);
}
for(const name of Object.keys(light).filter(n=>/^#/.test(light[n])))assert(name in darkValues,`Missing dark token: ${name}`);
for(const used of [...css.matchAll(/var\(--([\w-]+)/g)].map(m=>m[1]))assert(used in light,`Undefined token ${used}`);
assert(html.indexOf('tokens.css')<html.indexOf('app.css'),'Tokens must be loaded first');
function lum(hex){const c=[1,3,5].map(i=>parseInt(hex.slice(i,i+2),16)/255).map(x=>x<=.04045?x/12.92:((x+.055)/1.055)**2.4);return .2126*c[0]+.7152*c[1]+.0722*c[2];}
const ratio=(a,b)=>{const [hi,lo]=[lum(a),lum(b)].sort((a,b)=>b-a);return(hi+.05)/(lo+.05)};
const pairs=[['ink','bg',4.5],['ink','surface',4.5],['ink','tint',4.5],['muted','bg',4.5],['muted','surface',4.5],['primary','bg',4.5],['primary','surface',4.5],['on-primary','primary',4.5],['danger','bg',4.5],['danger','danger-bg',4.5],['border','surface',3],['focus','bg',3],['focus','surface',3]];
let results=[];
for(const [theme,t]of Object.entries({light,dark}))for(const[a,b,min]of pairs){let r=ratio(t[a],t[b]);assert(r>=min,`${theme} ${a}/${b} = ${r}`);results.push({theme,foreground:a,background:b,ratio:+r.toFixed(2),minimum:min});}
assert.equal(fs.readFileSync(path.resolve(root,'fixtures.js'),'utf8'),fs.readFileSync(path.resolve(root,'../../fixtures.js'),'utf8'),'Fixture copy changed');
fs.writeFileSync(path.resolve(__dirname,'contrast.json'),JSON.stringify(results,null,2));
console.log(`PASS: token use, theme parity, wiring, fixture integrity, ${results.length} contrast pairs.`);
