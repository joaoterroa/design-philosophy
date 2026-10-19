const fs=require('node:fs'),assert=require('node:assert/strict'),path=require('node:path');
const root=path.resolve(__dirname,'../app');
const tokens=fs.readFileSync(path.join(root,'tokens.css'),'utf8');
const css=fs.readFileSync(path.join(root,'app.css'),'utf8');
const vars=s=>Object.fromEntries([...s.matchAll(/--([\w-]+):\s*([^;]+);/g)].map(m=>[m[1],m[2].trim()]));
const split=tokens.indexOf(':root[data-theme="dark"]'),light=vars(tokens.slice(0,split)),dark=vars(tokens.slice(split));
assert.deepEqual(css.match(/#[0-9a-f]{3,8}\b|rgba?\(|hsla?\(/gi)||[],[],'Literal component colors');
assert.deepEqual(css.match(/-?\d*\.?\d+(?:px|ms)\b/g)||[],[],'Literal component dimensions or durations');
for(const key of Object.keys(light).filter(k=>/^#/.test(light[k])))assert.ok(key in dark,'Dark missing '+key);
for(const m of css.matchAll(/var\(--([\w-]+)\)/g))assert.ok(m[1] in light||m[1]==='elapsed','Undefined '+m[1]);
function lum(h){const c=[1,3,5].map(i=>parseInt(h.slice(i,i+2),16)/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4);return c[0]*.2126+c[1]*.7152+c[2]*.0722}
function contrast(a,b){let x=lum(a),y=lum(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)}
const report=[];
for(const [name,t] of [['light',light],['dark',{...light,...dark}]]){
 const pairs=[];
 for(const fg of ['fg','muted'])for(const bg of ['bg','surface','paper','tint'])pairs.push([fg,bg,4.5]);
 pairs.push(['accent','bg',4.5],['accent','paper',4.5],['on-accent','accent',4.5],['warning','warning-bg',4.5],['success','success-bg',4.5],['control-line','paper',3],['focus','bg',3],['accent','tint-line',3]);
 for(const [fg,bg,min] of pairs){const ratio=contrast(t[fg],t[bg]);report.push({theme:name,fg,bg,ratio:Number(ratio.toFixed(2)),minimum:min});assert.ok(ratio>=min,`${name}: ${fg} on ${bg} = ${ratio}`)}
}
const html=fs.readFileSync(path.join(root,'index.html'),'utf8');assert.ok(html.indexOf('tokens.css')<html.indexOf('app.css'),'Token load order');
assert.equal(fs.readFileSync(path.resolve(root,'../../fixtures.js'),'utf8'),fs.readFileSync(path.join(root,'fixtures.js'),'utf8'),'Fixture copy changed');
fs.writeFileSync(path.join(__dirname,'contrast.json'),JSON.stringify(report,null,2));
console.log(`PASS: tokens, theme parity, wiring, unchanged fixtures; ${report.length} contrast pairs. Minimum text contrast: ${Math.min(...report.filter(r=>r.minimum===4.5).map(r=>r.ratio))}:1.`);
