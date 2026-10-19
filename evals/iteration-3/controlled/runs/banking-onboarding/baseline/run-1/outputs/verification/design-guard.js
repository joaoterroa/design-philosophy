const fs=require('node:fs');
const assert=require('node:assert/strict');
const path=require('node:path');
const root=path.resolve(__dirname,'../app');
const tokens=fs.readFileSync(path.join(root,'tokens.css'),'utf8');
const css=fs.readFileSync(path.join(root,'styles.css'),'utf8');
const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
const vars=s=>Object.fromEntries([...s.matchAll(/--([\w-]+):\s*([^;]+);/g)].map(m=>[m[1],m[2].trim()]));
const light=vars(tokens.split(':root[data-theme=dark]')[0]);
const dark=vars(tokens.split(':root[data-theme=dark]')[1]);
const colors=Object.keys(light).filter(k=>/^#[\da-f]{6,8}$/i.test(light[k]));
assert.deepEqual(colors.filter(k=>!dark[k]),[],'Dark theme must redefine every color');
assert(!/#[\da-f]{3,8}\b|rgba?\(|hsla?\(/i.test(css),'Literal color outside tokens');
for(const property of ['font-size','border-radius','box-shadow','letter-spacing']){
 for(const match of css.matchAll(new RegExp(property+':([^;}]+)','g')))assert(match[1].trim().startsWith('var('),`Token required: ${match[0]}`);
}
for(const m of css.matchAll(/var\(--([\w-]+)\)/g))assert(light[m[1]],`Undefined token ${m[1]}`);
assert(html.indexOf('tokens.css')<html.indexOf('styles.css'),'Tokens must load before components');
assert.equal(fs.readFileSync(path.join(root,'fixtures.js'),'utf8'),fs.readFileSync(path.join(root,'../../fixtures.js'),'utf8'),'Fixture must remain unchanged');
function lum(hex){const c=[1,3,5].map(i=>parseInt(hex.slice(i,i+2),16)/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4);return .2126*c[0]+.7152*c[1]+.0722*c[2]}
function contrast(a,b){const [hi,lo]=[lum(a),lum(b)].sort((a,b)=>b-a);return (hi+.05)/(lo+.05)}
const ratios=[];
for(const [theme,t] of [['light',light],['dark',{...light,...dark}]]){
 const pairs=[];
 for(const fg of ['ink','muted'])for(const bg of ['bg','surface','tint'])pairs.push([fg,bg,4.5]);
 pairs.push(['action','bg',4.5],['on-action','action',4.5],['error','bg',4.5],['error','error-bg',4.5],['input-line','surface',3],['input-line','bg',3],['input-line','tint',3],['focus','bg',3],['focus','surface',3]);
 for(const [fg,bg,min]of pairs){const ratio=contrast(t[fg],t[bg]);assert(ratio>=min,`${theme}: ${fg}/${bg} = ${ratio.toFixed(2)}, minimum ${min}`);ratios.push({theme,foreground:fg,background:bg,ratio:+ratio.toFixed(2),minimum:min})}
}
fs.writeFileSync(path.resolve(__dirname,'contrast-results.json'),JSON.stringify(ratios,null,2)+'\n');
console.log(`PASS: token wiring, no literal style colors/type/radii/shadows/tracking, theme parity, unchanged fixtures; ${ratios.length} contrast pairs.`);
